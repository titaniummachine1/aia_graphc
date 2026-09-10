"""Demo bot compiled with graphc: counter latch + packed array roundtrip.

Output: game save format, replayable in the aia_comp-sim VM.
"""
from pathlib import Path

from graphc import GraphCtx, compile_graph


def demo(ctx: GraphCtx) -> None:
    # Cross-tick counter latch (verified primitive).
    cnt = ctx.var_get("cnt")
    nxt = cnt + 1
    ctx.var_set("cnt", nxt)

    # Packed array: slots 3-5 hold 7.5/8.5/9.5. Three static writes to the
    # same packed vector MERGE into one read-modify-write per tick.
    arr = ctx.array("buf", 6)
    arr.set_static(3, 7.5)
    arr.set_static(4, 8.5)
    arr.set_static(5, 9.5)
    val = arr.get_dynamic(3 + cnt % 3)

    # Dynamic if: both arms evaluated per tick (game semantics).
    flag = ctx.select(cnt > 12, 1.0, 2.0)

    ctx.soccer_move(val + flag, nxt)


if __name__ == "__main__":
    out = str(Path(__file__).parent / "graphc_demo_soccer.txt")
    compile_graph(("soccer", "v0.12"), demo, out)