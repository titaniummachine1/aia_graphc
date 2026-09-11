"""Misuse battery: every unsupported pattern fails LOUDLY at compile time.

The guarantee: if your AI misbehaves in game, it is doing exactly what you
coded — nothing is ever silently miscompiled. Each case below must raise
SyntaxError (the single catchable type for all authoring errors).

Run: python graphc/tests/test_misuse.py  (or: python -m pytest graphc/tests/)
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from graphc.ast_fe import compile_project, compile_source

SOCCER = ("soccer", "v0.12")

CASES: list[tuple[str, str, tuple[str, str] | None]] = [
    # Each case: (name, source, target override or None for SOCCER).
    # --- api rebinding (4): `api` is the compiler's handle, never a variable
    ("assign api", "def tick(api):\n    api = 5\n    api.move(0, 0)\n", None),
    ("augassign api", "def tick(api):\n    api += 1\n    api.move(0, 0)\n", None),
    ("param named api",
     "def f(api):\n    return api + 1\ndef tick(api):\n    api.move(f(1), 0)\n", None),
    ("const named api", "api = 5\ndef tick(api):\n    api.move(0, 0)\n", None),
    # --- controllers (2): one controller call per tick, period
    ("double move", "def tick(api):\n    api.move(0, 0)\n    api.move(1, 1)\n", None),
    ("move in branch + move after",
     "def tick(api):\n    x = 1\n    if x > 0:\n        api.move(0, 0)\n    api.move(1, 1)\n",
     None),
    # --- latch writes (2): one write per latch cell per tick (same index
    # twice collides; different indices pack into one RMW and are legal)
    ("double set_var",
     "def tick(api):\n    api.set_var('c', 1)\n    api.set_var('c', 2)\n    api.move(0, 0)\n",
     None),
    ("double arr_set same cell",
     "def tick(api):\n    a = api.array('a', 4)\n    api.arr_set(a, 0, 1)\n"
     "    api.arr_set(a, 0, 2)\n    api.move(0, 0)\n",
     None),
    # --- imports (3): project files only, no stdlib, no stars
    ("stdlib import", "import math\ndef tick(api):\n    api.move(0, 0)\n", None),
    ("star import", "from aim import *\ndef tick(api):\n    api.move(0, 0)\n", None),
    ("missing project file", "import nope_missing\ndef tick(api):\n    api.move(0, 0)\n", None),
    # --- sensors/versions (2)
    ("unknown sensor",
     "def tick(api):\n    x = api.tennis_get_float('No Such Sensor')\n"
     "    api.plot('C', x)\n    api.move(0, 0)\n",
     None),
    ("soccer-only call on tennis target",
     "def tick(api):\n    x = api.soccer_get_float('Ball Speed')\n"
     "    api.plot('C', x)\n    api.move(0, 0)\n",
     ("tennis", "v15f")),
    # --- expressions (5): plain values only, no syntax sugar
    ("boolop", "def tick(api):\n    x = 1\n    y = 2\n    z = x and y\n    api.move(z, 0)\n", None),
    ("ternary",
     "def tick(api):\n    x = 1\n    y = 1 if x > 0 else 2\n    api.move(y, 0)\n", None),
    ("subscript", "def tick(api):\n    x = [1, 2]\n    api.move(x[0], 0)\n", None),
    ("walrus", "def tick(api):\n    x = (y := 5)\n    api.move(x, 0)\n", None),
    ("tuple unpack", "def tick(api):\n    a, b = 1, 2\n    api.move(a, b)\n", None),
    ("chained comparison",
     "def tick(api):\n    x = 1\n    y = 1 if 0 < x < 2 else 2\n    api.move(y, 0)\n", None),
    # --- loops (3): bounded only; jumps need their loop; sinks hoist out
    ("break outside loop", "def tick(api):\n    x = 1\n    break\n    api.move(0, 0)\n", None),
    ("range over variable",
     "def tick(api):\n    n = 5\n    s = 0\n    for i in range(n):\n        s = s + 1\n"
     "    api.plot('C', s)\n    api.move(0, 0)\n",
     None),
    ("plot inside loop",
     "def tick(api):\n    s = 0\n    for i in range(4):\n        s = s + 1\n"
     "        api.plot('C', s)\n    api.move(0, 0)\n",
     None),
    ("move inside loop",
     "def tick(api):\n    s = 0\n    for i in range(4):\n        s = s + 1\n"
     "        api.move(s, 0)\n",
     None),
    # --- functions (4)
    ("missing return", "def f(a):\n    b = a + 1\ndef tick(api):\n    api.move(f(1), 0)\n", None),
    ("bad arity",
     "def f(a, b):\n    return a + b\ndef tick(api):\n    api.move(f(1), 0)\n", None),
    ("undefined name", "def tick(api):\n    api.move(nope(1), 0)\n", None),
    ("use before assign", "def tick(api):\n    api.move(x, 0)\n    x = 1\n", None),
    # --- project rules (2, single-file rejections)
    ("top-level statement", "print('hi')\ndef tick(api):\n    api.move(0, 0)\n", None),
    ("tick arity", "def tick():\n    pass\n", None),
    # --- split drive (4, tennis): aim pairs with move, autoswing is modal
    ("double tennis_aim",
     "def tick(api):\n    api.tennis_aim(1, 2)\n    api.tennis_aim(3, 4)\n"
     "    api.tennis_move(0, 0)\n",
     ("tennis", "v0.14")),
    ("tennis_aim without move",
     "def tick(api):\n    api.tennis_aim(1, 2)\n", ("tennis", "v0.14")),
    ("autoswing bad mode",
     "def tick(api):\n    s = api.tennis_auto_swing(2.0, 'Berserk')\n"
     "    api.tennis_move(0, 0, s, 2.0)\n",
     ("tennis", "v0.14")),
    ("autoswing on soccer",
     "def tick(api):\n    s = api.tennis_auto_swing(2.0)\n    api.move(0, 0)\n", None),
]


def test_misuse_battery() -> None:
    failures = []
    for name, src, target in CASES:
        try:
            compile_source(src, target or SOCCER)
        except SyntaxError:
            continue
        except Exception as e:  # noqa: BLE001 — any other error is also loud, but pin the type
            failures.append(f"{name}: loud but {type(e).__name__}, want SyntaxError: {e}")
            continue
        failures.append(f"{name}: COMPILED SILENTLY (must fail loudly)")
    assert not failures, "misuse battery leaks:\n" + "\n".join(failures)
    assert len(CASES) == 33, f"battery shrank: {len(CASES)} cases"


def test_project_rules() -> None:
    # Two tick functions across files + conflicting constants: need a project.
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "a.py").write_text(
            "import b\ndef tick(api):\n    api.move(b.K, 0)\n")
        (Path(d) / "b.py").write_text(
            "K = 1\ndef tick(api):\n    api.move(1, 1)\n")
        try:
            compile_project(str(Path(d) / "a.py"), SOCCER)
        except SyntaxError:
            pass
        else:
            raise AssertionError("two tick functions compiled silently")
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "a.py").write_text(
            "K = 1\ndef tick(api):\n    api.move(0, 0)\n")
        (Path(d) / "b.py").write_text("K = 2\n")
        # b.py is only loaded if imported; import it to trigger the conflict.
        (Path(d) / "a.py").write_text(
            "import b\nK = 1\ndef tick(api):\n    api.move(b.K + K, 0)\n")
        try:
            compile_project(str(Path(d) / "a.py"), SOCCER)
        except SyntaxError:
            pass
        else:
            raise AssertionError("conflicting constants compiled silently")


def test_full_names_match_shorts() -> None:
    # Canonical full spellings compile to byte-identical graphs as the
    # terse aliases (aliases are normalized at trace entry).
    short = (
        "def tick(api):\n    a = api.array('a', 4)\n"
        "    api.arr_set(a, 0, 1)\n    x = api.arr_get(a, 0)\n"
        "    api.plot('C', x + api.vec_split(api.vec_make(1, 2, 3), 0))\n"
        "    api.move(0, 0)\n"
    )
    full = (
        "def tick(api):\n    a = api.array('a', 4)\n"
        "    api.set_array_cell(a, 0, 1)\n    x = api.get_array_cell(a, 0)\n"
        "    api.plot('C', x + api.split_vector(api.make_vector(1, 2, 3), 0))\n"
        "    api.move(0, 0)\n"
    )
    assert compile_source(short, SOCCER) == compile_source(full, SOCCER)


def test_stale_sensor_warns_not_fails() -> None:
    # Estimated Opponent Shot Location is game-stale outside its window:
    # compiles fine, but the author gets a loud stderr pointer to
    # predicted_bounce. Both sensor spellings warn.
    import io
    from contextlib import redirect_stderr
    for src in (
        "import AIA_Comp_Libry.tennis.v014 as tennis\n"
        "def tick(api):\n"
        "    guess = tennis.estimated_opponent_shot_location()\n"
        "    tennis.move(0, 0, False, 2.0)\n",
        "def tick(api):\n"
        "    guess = api.tennis_get_vector3('Estimated Opponent Shot Location')\n"
        "    api.tennis_move(0, 0, False, 2.0)\n",
    ):
        buf = io.StringIO()
        with redirect_stderr(buf):
            compile_source(src, ("tennis", "v0.14"))
        assert "predicted_bounce" in buf.getvalue(), f"no stale warning for {src[:40]!r}"


def test_split_drive_compiles() -> None:    # Walk/aim/swing split across the native assist nodes (the basic-bot
    # shape): aim request + AutoSwing + one controller, all wired.
    desc = compile_source(
        "def tick(api):\n"
        "    api.tennis_aim(7.0, 0.0)\n"
        "    swing = api.tennis_auto_swing(2.0)\n"
        "    api.tennis_move(-14.0, 2.0, swing, 2.0)\n",
        ("tennis", "v0.14"),
    )
    ops = [o["op"] for o in desc["ops"]]
    assert "tennis_aim" in ops and "tennis_auto_swing" in ops, ops


def test_legit_patterns_stay_green() -> None:
    # Bounded loops, if/else, helpers, latches, arrays, recursion, plot.
    compile_source(
        "def f(n):\n    r = n\n    if n > 1.0:\n        r = f(n - 1) + 1\n    return r\n"
        "def tick(api):\n    s = 0\n    for i in range(4):\n        s = s + i\n"
        "    api.set_var('c', s)\n    a = api.array('a', 4)\n    api.arr_set(a, 0, s)\n"
        "    v = api.var('c') + api.arr_get(a, 0) + f(3)\n"
        "    api.plot('C', v)\n    api.move(v, 0)\n",
        SOCCER,
    )


if __name__ == "__main__":
    test_misuse_battery()
    test_project_rules()
    test_full_names_match_shorts()
    test_stale_sensor_warns_not_fails()
    test_split_drive_compiles()
    test_legit_patterns_stay_green()
    print(f"misuse battery ok ({len(CASES)} cases + project rules + full names + split drive + legit patterns)")
