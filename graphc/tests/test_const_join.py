"""Frontend const-join tests: same fp32 bits => same node.

Rule: literals whose f32 bit patterns are identical share one const op
(`1`, `1.0` — and `True`, which lowers to f32 1.0 — are one node in the
save; the backend dedupes by bits, see
`same_fp32_bits_share_one_float_node` in src/lib.rs).

Run: python -m pytest graphc/tests/  (or: python graphc/tests/test_const_join.py)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_source

BOT = """def tick(api):
    a = 1 + 1.0
    b = 1.0 + 1
    t = True
    if t:
        b = b + a
    api.plot('X', a + b)
    api.move(0, 0)
"""


def _const_ops(desc):
    return [o for o in desc["ops"] if o["op"] == "const"]


def test_int_float_spellings_share_one_const():
    desc = compile_source(BOT, ("soccer", "v0.12"))
    ones = [o for o in _const_ops(desc) if o["value"] == 1.0]
    # `1` x2 + `1.0` x2 in source, one const op in the desc.
    assert len(ones) == 1, f"1/1.0 must share one const op, got {ones}"


def test_bool_true_keeps_bool_type():
    # True keeps bool type at trace time (so `x + True` below stays
    # loud), and `if True:` prunes to the taken arm (no select node).
    desc = compile_source(
        "def tick(api):\n"
        "    t = True\n"
        "    x = api.var('v')\n"
        "    if t:\n"
        "        x = x + 1\n"
        "    api.plot('X', x)\n"
        "    api.move(0, 0)\n",
        ("soccer", "v0.12"),
    )
    assert not any(o["op"] == "select" for o in desc["ops"]), \
        "static-True arm must prune, not select"


def test_bool_into_arithmetic_is_loud():
    try:
        compile_source(
            "def tick(api):\n    api.plot('X', True + 1)\n    api.move(0, 0)\n",
            ("soccer", "v0.12"),
        )
    except SyntaxError as e:
        assert "bool" in str(e), e
    else:
        raise AssertionError("True + 1 compiled silently")


if __name__ == "__main__":
    test_int_float_spellings_share_one_const()
    test_bool_true_keeps_bool_type()
    test_bool_into_arithmetic_is_loud()
    print("const-join frontend tests ok")
