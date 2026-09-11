"""graphc — compile plain code (Python now, Rust later) into AIA graph bots.

Separate from the simulator by design: the simulator replays graphs; this
library turns SOURCE CODE into graphs.

Usage (authoring path: plain Python -> description IR -> graphc-rs backend):

    from graphc.ast_fe import compile_source
    import json, subprocess

    desc = compile_source(source, ("soccer", "v0.12"))
    json.dump(desc, open("bot.desc.json", "w"))
    subprocess.run(["graphc-rs", "bot.desc.json", "bot.txt"], check=True)

Rules (enforced at trace time — the supported-API whitelist):
  - Only the api.* surface + arithmetic on traced values; anything
    untraceable fails loudly with a pointing error, never silently
    misbehaves.
  - Dynamic `if` is real syntax (SSA phi-merge via select nodes); dynamic
    `while`/`for`/imports are rejected — express state across ticks with
    api.set_var (both arms evaluate per tick — semantics match the game).
  - Targets are explicit: compile for (game, version) from the pinned
    target tables (sensors/controllers differ per version). A "universal"
    target exists for unknown games: raw node emission only, no game API.
  - Cross-tick memory: api.var/api.set_var (named latch) and api.array +
    api.arr_set/arr_get/arr_get_dyn (packed Vector3 cells).
Cost model: per-tick node transitions (nodes + edges) — the C# per-tick
overhead metric. graphc-rs prints the report; CI fails on regressions.
"""
from __future__ import annotations

import os
import sys

# AIGamePyLibrary holds the dropdown-order tables (sensor ABI) the tennis
# frontend resolves at trace time. Until it is published as a package,
# point GRAPHC_PYLIB at its checkout.
PYLIB = os.environ.get(
    "GRAPHC_PYLIB",
    r"C:\gitProjects\AIA_tennis\AIGamePyLibrary",
)
if PYLIB not in sys.path:
    sys.path.insert(0, PYLIB)

from .ast_fe import compile_project, compile_source
from .desc import (
    SUPPORTED_TARGETS,
    check_target,
    describe,
    soccer_sensor_index,
    tennis_sensor_index,
)

__all__ = [
    "compile_project",
    "compile_source",
    "describe",
    "tennis_sensor_index",
    "soccer_sensor_index",
    "SUPPORTED_TARGETS",
    "check_target",
]
