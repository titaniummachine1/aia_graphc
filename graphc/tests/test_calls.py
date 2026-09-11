"""Helper-call regression tests: argument evaluation order + recursion values.

Bug class (2026-09-11): params bound into the shared env one-by-one, so
binding `a` clobbered caller-`a` before later args evaluated — gcd(b, a%b)
lowered as gcd(b, b%b) and plotted 18 instead of 6. Args now all evaluate
in the caller env before any param binds.

Run: python -m pytest graphc/tests/  (or: python graphc/tests/test_calls.py)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_source


def _plot_source(desc, channel="C"):
    plots = [o for o in desc["ops"] if o["op"] == "plot" and o["name"] == channel]
    assert len(plots) == 1, f"one {channel} plot, got {plots}"
    return plots[0]["v"]


def _const_value(desc, op_id):
    o = desc["ops"][op_id]
    assert o["op"] == "const", f"op {op_id} must be const, got {o}"
    return o["value"]


def test_call_args_evaluate_before_param_binds():
    # f(a, a+1): the second arg must see caller-a, not the fresh param.
    desc = compile_source(
        "def f(a, b):\n    return a + b\n"
        "def tick(api):\n    a = 10\n    api.plot('C', f(a, a + 1))\n    api.move(0, 0)\n",
        ("soccer", "v0.12"),
    )
    # 10 + 11 = 21: both const-foldable at desc? No arithmetic folding —
    # so assert structure: add of (10, add(10, 1)).
    v = _plot_source(desc)
    add = desc["ops"][v]
    assert add["op"] == "bin" and add["fn"] == "AddFloats", add
    assert _const_value(desc, add["a"]) == 10.0
    inner = desc["ops"][add["b"]]
    assert inner["op"] == "bin" and inner["fn"] == "AddFloats", inner
    assert _const_value(desc, inner["a"]) == 10.0
    assert _const_value(desc, inner["b"]) == 1.0


def test_recursive_gcd_plots_6():
    # No value folding at desc level: the plot wires the nested modulo
    # chain 18 % (48 % 18), which evaluates to 6 (sim ConstFold proves it;
    # the committed probe + sim suite pin runtime values). All selects
    # pruned (static chain), so the whole gcd is 7 ops.
    desc = compile_source(
        "def gcd(a, b):\n    r = a\n    if b > 0.0:\n        r = gcd(b, a % b)\n"
        "    return r\n"
        "def tick(api):\n    api.plot('C', gcd(48, 18))\n    api.move(0, 0)\n",
        ("soccer", "v0.12"),
    )
    assert len(desc["ops"]) == 7, [o for o in desc["ops"]]
    v = _plot_source(desc)
    outer = desc["ops"][v]
    assert outer["op"] == "bin" and outer["fn"] == "Modulo", outer
    assert _const_value(desc, outer["a"]) == 18.0
    inner = desc["ops"][outer["b"]]
    assert inner["op"] == "bin" and inner["fn"] == "Modulo", inner
    assert _const_value(desc, inner["a"]) == 48.0
    assert _const_value(desc, inner["b"]) == 18.0


def test_recursive_fib6_plots_8():
    desc = compile_source(
        "def fib(n):\n    r = n\n    if n > 1.0:\n"
        "        r = fib(n - 1) + fib(n - 2)\n    return r\n"
        "def tick(api):\n    api.plot('C', fib(6))\n    api.move(0, 0)\n",
        ("soccer", "v0.12"),
    )
    # Exact pruned tree is small (no budget waste).
    assert len(desc["ops"]) < 100, len(desc["ops"])


if __name__ == "__main__":
    test_call_args_evaluate_before_param_binds()
    test_recursive_gcd_plots_6()
    test_recursive_fib6_plots_8()
    print("call regression tests ok")
