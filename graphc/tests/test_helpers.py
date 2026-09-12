"""Scalar/bool helper tests: abs/sqrt/sign/bool_and/bool_or/clamp/dot.

Each is one game node (titanium's exact ops: Operation 0/10/11,
CompareBool 0/1, ClampFloat, DotProduct). Pure values — branch-safe.

Run: python graphc/tests/test_helpers.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_source

SOCCER = ("soccer", "v0.12")
TENNIS = ("tennis", "v15f")


def test_helpers_emit_their_ops():
    d = compile_source(
        "def tick(api):\n"
        "    a = api.abs(0.0 - 3.0)\n"
        "    s = api.sqrt(9.0)\n"
        "    g = api.sign(a)\n"
        "    c = api.clamp(a, 0.0, 5.0)\n"
        "    api.plot('H', a + s + g + c)\n"
        "    api.move(a, 0)\n",
        SOCCER)
    kinds = [o["op"] for o in d["ops"]]
    assert kinds.count("unary") == 3, kinds
    assert "clamp" in kinds, kinds
    fns = sorted(o["fn"] for o in d["ops"] if o["op"] == "unary")
    assert fns == ["Abs", "Sign", "Sqrt"], fns


def test_bool_helpers_need_bools():
    d = compile_source(
        "def tick(api):\n"
        "    x = 1.0\n"
        "    b = api.bool_and(x > 0.0, x > 2.0)\n"
        "    c = api.bool_or(b, x > 5.0)\n"
        "    v = 0.0\n"
        "    if c:\n"
        "        v = 1.0\n"
        "    api.plot('B', v)\n"
        "    api.move(v, 0)\n",
        SOCCER)
    kinds = [o["op"] for o in d["ops"]]
    assert kinds.count("bool_op") == 2, kinds


def test_dot_and_branches_in_game():
    d = compile_source(
        "import AIA_Comp_Libry.tennis.v15f as t\n"
        "def tick(api):\n"
        "    if t.ball_incoming():\n"
        "        v = t.ball_position()\n"
        "    else:\n"
        "        v = t.predicted_bounce()\n"
        "    w = t.center_of_back()\n"
        "    d = api.dot(v, w)\n"
        "    m = api.distance(v, w)\n"
        "    api.plot('D', d + m)\n"
        "    t.aim(0.0, 11.0)\n"
        "    t.move_vec(v, t.auto_swing(2.0), 2.0)\n",
        TENNIS)
    kinds = [o["op"] for o in d["ops"]]
    assert "dot" in kinds, kinds
    sels = [o for o in d["ops"] if o["op"] == "select"]
    assert sels and all(o.get("typ") == "vector" for o in sels), sels


def test_every_select_carries_its_type():
    for src, target in [
        ("def tick(api):\n    x = 1.0\n    if x > 0.0:\n        y = 2.0\n"
         "    else:\n        y = 3.0\n    api.move(y, 0)\n", SOCCER),
        ("def tick(api):\n    s = 0.0\n    for i in range(4):\n"
         "        s = s + i\n    api.move(s, 0)\n", SOCCER),
    ]:
        d = compile_source(src, target)
        for o in d["ops"]:
            if o["op"] == "select":
                assert o.get("typ") in ("float", "bool", "vector"), o


LOUD = [
    ("bool into sqrt",
     "def tick(api):\n    x = 1.0\n    api.move(api.sqrt(x > 0.0), 0)\n"),
    ("vector into abs",
     "def tick(api):\n    v = api.make_vector(1, 2, 3)\n"
     "    api.move(api.abs(v), 0)\n"),
    ("float into bool_and",
     "def tick(api):\n    api.move(0, api.bool_and(1.0, 2.0))\n"),
    ("transform into dot",
     "import AIA_Comp_Libry.tennis.v15f as t\n"
     "def tick(api):\n    api.plot('D', api.dot(t.self(), t.ball()))\n"
     "    t.move(0.0, 11.0, False, 2.0)\n"),
    ("clamp arity",
     "def tick(api):\n    api.move(api.clamp(1.0, 2.0), 0)\n"),
    ("transform branch arms",
     "import AIA_Comp_Libry.tennis.v15f as t\n"
     "def tick(api):\n    api.set_var('c', 1.0)\n    dyn = api.var('c')\n"
     "    if dyn > 0.0:\n        v = t.self()\n"
     "    else:\n        v = t.ball()\n"
     "    api.plot('C', 0.0)\n    t.move(0.0, 11.0, False, 2.0)\n"),
]


def test_misuse_is_loud():
    failures = []
    for name, src in LOUD:
        target = TENNIS if "tennis" in src else SOCCER
        try:
            compile_source(src, target)
        except SyntaxError:
            continue
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name}: loud but {type(e).__name__}: {e}")
            continue
        failures.append(f"{name}: COMPILED SILENTLY (must fail loudly)")
    assert not failures, "helper misuse leaks:\n" + "\n".join(failures)


if __name__ == "__main__":
    test_helpers_emit_their_ops()
    test_bool_helpers_need_bools()
    test_dot_and_branches_in_game()
    test_every_select_carries_its_type()
    test_misuse_is_loud()
    print(f"helper tests ok (4 patterns + {len(LOUD)} loud cases)")
