"""Pure-Python table tests: lists are tables, no api.* needed.

Const rule (same as scalars): a module list the bot WRITES is RAM, one it
only reads stays frozen constants. Static reads inline to zero nodes;
dynamic reads build the backend's own select-chain (miss => cell0);
writes need static indices at tick top level.

Run: python graphc/tests/test_tables.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_source

SOCCER = ("soccer", "v0.12")

DYN = "    api.set_var('c', 1.0)\n    dyn = api.var('c')\n"


def test_const_static_read_inlines():
    d = compile_source(
        "def tick(api):\n    cells = [1.0, 2.0, 4.0]\n"
        "    api.plot('A', cells[2])\n    api.move(cells[0], 0)\n",
        SOCCER)
    kinds = [o["op"] for o in d["ops"]]
    assert "select" not in kinds, kinds
    assert "array" not in kinds, kinds


def test_const_dynamic_read_chains_like_backend():
    d = compile_source(
        "def tick(api):\n" + DYN + "    cells = [1.0, 2.0, 4.0, 8.0]\n"
        "    b = cells[dyn]\n    api.plot('B', b)\n    api.move(b, 0)\n",
        SOCCER)
    sels = [o for o in d["ops"] if o["op"] == "select"]
    assert len(sels) == 3, len(sels)  # n cells => n-1 selects
    # miss falls through to cell0 (backend parity: acc starts at cell 0)
    assert d["ops"][sels[0]["f"]]["op"] == "const"


def test_negative_index_wraps_python_style():
    d = compile_source(
        "AIMZ = [-4.0, 4.0]\n"
        "def tick(api):\n    api.plot('Z', AIMZ[-1])\n    api.move(0, 0)\n",
        SOCCER)
    plots = [o for o in d["ops"] if o["op"] == "plot"]
    consts = [o for o in d["ops"] if o["op"] == "const"]
    assert any(o["value"] == 4.0 for o in consts)
    assert plots and d["ops"][plots[0]["v"]]["value"] == 4.0


def test_len_and_range_len_fill():
    d = compile_source(
        "mem = [0.0] * 4\n"
        "def tick(api):\n"
        "    for i in range(len(mem)):\n"
        "        mem[i] = i + 10.0\n"
        "    api.plot('X', mem[3] + len(mem))\n"
        "    api.move(0, 0)\n",
        SOCCER)
    kinds = [o["op"] for o in d["ops"]]
    assert "array" in kinds and kinds.count("array_set_static") == 4, kinds


def test_ram_write_read_and_augassign():
    d = compile_source(
        "mem = [0.0, 0.0, 0.0]\n"
        "def tick(api):\n"
        "    mem[0] = 1.0\n"
        "    mem[1] = mem[0] + 1.0\n"
        "    mem[2] += 5.0\n"
        "    api.plot('X', mem[1] + mem[2])\n"
        "    api.move(0, 0)\n",
        SOCCER)
    kinds = [o["op"] for o in d["ops"]]
    assert kinds.count("array_set_static") == 3, kinds
    assert "array_get_static" in kinds, kinds


def test_ram_dynamic_read():
    d = compile_source(
        "mem = [0.0, 0.0]\n"
        "def tick(api):\n" + DYN +
        "    mem[0] = 1.0\n    mem[1] = 2.0\n"
        "    api.plot('X', mem[dyn])\n    api.move(0, 0)\n",
        SOCCER)
    assert any(o["op"] == "array_get_dynamic" for o in d["ops"])


def test_module_const_stays_frozen():
    d = compile_source(
        "AIMZ = [-4.0, 4.0]\n"
        "def tick(api):\n    api.plot('Z', AIMZ[0])\n    api.move(0, 0)\n",
        SOCCER)
    assert not any(o["op"] == "array" for o in d["ops"])


LOUD = [
    ("dynamic write",
     "mem = [0.0, 0.0]\ndef tick(api):\n" + DYN + "    mem[dyn] = 5.0\n"
     "    api.move(0, 0)\n"),
    ("branch write",
     "mem = [0.0]\ndef tick(api):\n" + DYN + "    if dyn > 0.0:\n"
     "        mem[0] = 2.0\n    api.move(0, 0)\n"),
    ("helper write",
     "mem = [0.0]\ndef w(api):\n    mem[0] = 1.0\n"
     "def tick(api):\n    w(api)\n    api.move(0, 0)\n"),
    ("double write",
     "mem = [0.0]\ndef tick(api):\n    mem[0] = 1.0\n    mem[0] = 2.0\n"
     "    api.move(0, 0)\n"),
    ("float literal index",
     "def tick(api):\n    c = [1.0]\n    api.move(c[1.5], 0)\n"),
    ("out of range",
     "def tick(api):\n    c = [1.0]\n    api.move(c[7], 0)\n"),
    ("nested list",
     "def tick(api):\n    c = [[1.0]]\n    api.move(0, 0)\n"),
    ("empty list",
     "def tick(api):\n    c = []\n    api.move(0, 0)\n"),
    ("whole-list arithmetic",
     "def tick(api):\n    c = [1.0, 2.0]\n    api.move(c + 1, 0)\n"),
    ("table through helper",
     "def f(t):\n    return t[0]\n"
     "def tick(api):\n    c = [1.0]\n    api.move(f(c), 0)\n"),
    ("append method",
     "mem = [0.0]\ndef tick(api):\n    mem.append(1.0)\n    api.move(0, 0)\n"),
    ("rebind module table",
     "mem = [0.0]\ndef tick(api):\n    mem = [1.0]\n    api.move(0, 0)\n"),
    ("branch bind",
     "def tick(api):\n" + DYN + "    if dyn > 0.0:\n        c = [1.0]\n"
     "    else:\n        c = [2.0]\n    api.move(c[0], 0)\n"),
    ("non-zero ram init",
     "mem = [5.0]\ndef tick(api):\n    mem[0] = 1.0\n    api.move(0, 0)\n"),
    ("len of scalar",
     "def tick(api):\n    x = 1.0\n    api.move(len(x), 0)\n"),
    ("subscript of scalar",
     "def tick(api):\n    x = 1.0\n    api.move(x[0], 0)\n"),
]


def test_misuse_is_loud():
    failures = []
    for name, src in LOUD:
        try:
            compile_source(src, SOCCER)
        except SyntaxError:
            continue
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: loud but {type(e).__name__}: {e}")
            continue
        failures.append(f"{name}: COMPILED SILENTLY (must fail loudly)")
    assert not failures, "table misuse leaks:\n" + "\n".join(failures)


if __name__ == "__main__":
    test_const_static_read_inlines()
    test_const_dynamic_read_chains_like_backend()
    test_negative_index_wraps_python_style()
    test_len_and_range_len_fill()
    test_ram_write_read_and_augassign()
    test_ram_dynamic_read()
    test_module_const_stays_frozen()
    test_misuse_is_loud()
    print(f"table tests ok (7 patterns + {len(LOUD)} loud cases)")
