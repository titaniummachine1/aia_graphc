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
   - Only the api.* surface + project code + arithmetic on traced values;
     anything untraceable fails loudly with a pointing error, never
     silently misbehaves. A 29-case misuse battery pins this
     (graphc/tests/test_misuse.py): shadowed api, double
     controllers/latches, stdlib imports, wrong game/version, unknown
     sensors, boolop/ternary/subscript/walrus, jumps outside loops,
     non-literal range, sinks in loop bodies, bad arity, top-level
     statements, conflicting constants — all loud.
    - Dynamic `if` is real syntax (SSA phi-merge via select nodes);
      bounded `for i in range(literal)` (cap 16384) / `while` (cap 512) /
      recursion (depth 128) unroll inline to flat graphs (overflow canaries,
      sinks hoisted out); cross-tick state lives in api.var/api.set_var
      latches and api.array cells (both arms evaluate per tick — semantics
      match the game). Cost model: connection traversals per tick first, size ties.
   - Multi-file projects via compile_project (imports resolved, functions
     inlined); per-(game,version) API: import AIA_Comp_Libry.tennis.v014
     (or unversioned .tennis = latest). Version mismatch fails loudly.
   - Targets are explicit: compile for (game, version) from the pinned
     target tables (sensors/controllers differ per version). A "universal"
     target exists for unknown games: raw node emission only, no game API.
    - Cross-tick memory: plain module variables (written => latch) and
      plain-Python tables — `cells = [...]` binds constants, a module list
      the bot writes becomes RAM (`tab[i] = v` static, reads static or
      dynamic, `len(tab)`, `range(len(tab))` fills). Legacy api.var/set_var
      and api.array cells still work. One controller call per tick.
   - Debug: api.plot(channel, value) (TimePlot sink, all targets) — the
     compiler-verification surface (game TimePlot export == sim == pure VM).
Cost model (lexicographic): connection traversals per tick first (one per
wired edge — node compute is free at this scale; the game fires every node
and edge each tick, so the count is static AND expected), graph size
(nodes + connections) breaks ties. graphc-rs prints the report.
Optimization modes (`compile_*`'s `optimize=` / graphc-rs's optional 3rd
arg) only control how much unnecessary material is dropped: "raw" (no
passes), "o0" (default, identity fold + DCE, keeps debug sinks), "o1"
(o0 + drop debug sinks), "o2" (o1 + strip visual chrome, dense ids).

Simple-use contract (humans + LLMs): write plain Python with the
AIA_Comp_Libry API (import AIA_Comp_Libry.tennis.v15f as t); every value
is typed (float/bool/vector/transform/array — see graphc.nodes), every
connection is checked, and illegal wiring fails at compile time with a
pointing error. You never name a node, port, or wire. Node input/output
reference lives in graphc.nodes (NODE_DOCS/IR_OPS); per-sensor docs with
return types live on the generated stubs (hover in any IDE).
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
    OPTIMIZE_MODES,
    SUPPORTED_TARGETS,
    check_target,
    describe,
    resolve_optimize,
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
    "OPTIMIZE_MODES",
    "resolve_optimize",
]
