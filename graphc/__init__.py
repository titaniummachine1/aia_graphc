"""graphc — compile plain code (Python now, Rust later) into AIA graph bots.

Separate from the simulator by design: the simulator replays graphs; this
library turns SOURCE CODE into graphs.

Usage:

    from graphc import GraphCtx, compile_graph, PackedArray

    def demo(ctx):
        cnt = ctx.var_get("cnt")
        nxt = cnt + 1
        ctx.var_set("cnt", nxt)
        ctx.soccer_move(cnt + 1, 0)

    compile_graph(("soccer", "v0.12"), demo, "bot.txt")

Rules (enforced at trace time — the supported-API whitelist):
  - Only this API + arithmetic on traced values; anything untraceable
    fails loudly with a pointing error, never silently misbehaves.
  - Dynamic `if`/`while` are rejected by construction; use ctx.select()
    (both arms evaluate per tick — semantics match the game).
  - Targets are explicit: compile for (game, version) from the pinned
    target tables (sensors/controllers differ per version). A "universal"
    target exists for unknown games: raw node emission only, no game API.
  - Cross-tick memory: Var (named Set/Get latch) and PackedArray (Vector3
    mixed-radix cells — 3 float slots per vector variable).
Cost model: per-tick node transitions (nodes + edges) — the C# per-tick
overhead metric. compile_graph() returns the report.
"""
from __future__ import annotations

import os
import sys

# AIGamePyLibrary is the game-save emitter (node JSON writer). Until it is
# published as a package, point GRAPHC_PYLIB at its checkout.
PYLIB = os.environ.get(
    "GRAPHC_PYLIB",
    r"C:\gitProjects\AIA_tennis\AIGamePyLibrary",
)
if PYLIB not in sys.path:
    sys.path.insert(0, PYLIB)

from AIGamePyLibrary import AddNode, ConnectPorts, SaveData  # noqa: E402

from .core import GraphCtx, PackedArray, Sym, compile_graph  # noqa: E402/F401

__all__ = ["GraphCtx", "PackedArray", "Sym", "compile_graph"]