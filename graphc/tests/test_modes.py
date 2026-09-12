"""Optimization-mode tests: modes may only drop unnecessary material.

Rule (user directive): performance is already maximal — the only graph cost
is per-tick node transitions, and the optimization modes only say how much
unnecessary material the compiler may drop. Behavior and play strength are
invariant; o0 (default) keeps debug sinks, o1 drops them, o2 also strips
visual chrome at emit, `raw` runs no passes at all.

Run: python graphc/tests/test_modes.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_source
from graphc.desc import OPTIMIZE_MODES, resolve_optimize

# Identity-heavy arithmetic + a debug sink. `x*1`, `x/1`, `x-0` are all
# bit-safe folds; `x+0` is deliberately NOT folded (sign of -0.0).
BOT = """def tick(api):
    n = 5.0
    a = n * 1.0
    b = a / 1.0
    c = b - 0.0
    api.plot('C', c)
    api.move(c, 0)
"""

TARGET = ("soccer", "v0.12")


def _raises(exc, fn):
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__} from {fn!r}")


def _ops(desc):
    return desc["ops"]


def _count(desc, op, **match):
    return sum(1 for o in _ops(desc)
               if o["op"] == op and all(o.get(k) == v for k, v in match.items()))


def test_resolve_accepts_spellings_and_aliases():
    assert [resolve_optimize(m) for m in ("raw", "o0", "O1", "o2")] == list(OPTIMIZE_MODES)
    assert resolve_optimize("normal") == "o0"
    assert resolve_optimize("debug") == "o0"
    assert resolve_optimize("release") == "o1"
    assert resolve_optimize("core") == "o2"
    assert resolve_optimize(0) == "o0"
    assert resolve_optimize(1) == "o1"
    assert resolve_optimize(2) == "o2"
    assert resolve_optimize(-1) == "raw"
    _raises(ValueError, lambda: resolve_optimize("o9"))
    _raises(TypeError, lambda: resolve_optimize(True))


def test_default_mode_is_o0_and_keeps_debug():
    desc = compile_source(BOT, TARGET)
    assert desc["optimize"] == "o0"
    assert _count(desc, "plot") == 1, "default o0 must keep debug sinks"
    # identities folded: no MultiplyFloats / DivideFloats / SubtractFloats
    assert _count(desc, "bin", fn="MultiplyFloats") == 0
    assert _count(desc, "bin", fn="DivideFloats") == 0
    assert _count(desc, "bin", fn="SubtractFloats") == 0


def test_o1_drops_debug_sinks():
    desc = compile_source(BOT, TARGET, "o1")
    assert desc["optimize"] == "o1"
    assert _count(desc, "plot") == 0, "o1 must strip debug sinks"


def test_raw_runs_no_passes():
    desc = compile_source(BOT, TARGET, "raw")
    assert desc["optimize"] == "raw"
    assert _count(desc, "plot") == 1
    # the identity nodes are still present (nothing folded)
    assert _count(desc, "bin", fn="MultiplyFloats") == 1
    assert _count(desc, "bin", fn="DivideFloats") == 1
    assert _count(desc, "bin", fn="SubtractFloats") == 1


def test_o2_is_carried_to_the_backend():
    desc = compile_source(BOT, TARGET, "o2")
    assert desc["optimize"] == "o2"
    assert _count(desc, "plot") == 0


def test_modes_keep_the_controller_and_shrink_monotonically():
    o0 = compile_source(BOT, TARGET, "o0")
    o1 = compile_source(BOT, TARGET, "o1")
    assert any(o["op"] == "soccer_move" for o in _ops(o0))
    assert any(o["op"] == "soccer_move" for o in _ops(o1))
    # o1 removes the debug chain, so it is strictly smaller than o0.
    assert len(_ops(o1)) < len(_ops(o0))


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"optimize-mode tests ok ({len(tests)} cases)")
