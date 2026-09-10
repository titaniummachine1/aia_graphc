# graphc — compile code into AIA graph bots

Separate from the simulator on purpose: the simulator replays graphs, this
library turns **source code** into graphs. Architecture follows the classic
compiler pipeline (gcc/LLVM/rustc shape, scaled down):

```
Python lib (now)  ─┐
                   ├─► bot description (language-neutral JSON IR)
Rust crate (later)─┘          │
                              ▼
                graphc backend: optimize (const-fold, CSE, write-merge,
                budget check on per-tick transitions) + emit game save
                format for an explicit (game, version) target
                              │
              ┌───────────────┴────────────────┐
              ▼                                ▼
        game save folder                 aia_comp-sim VM (CI)
        (play immediately)               (replay + assert before play)
```

## The writer's experience (the whole point)

```python
from graphc import GraphCtx, compile_graph

def my_bot(ctx: GraphCtx):
    cnt = ctx.var_get("cnt")          # cross-tick RAM
    cnt2 = cnt + 1                    # plain arithmetic
    ctx.var_set("cnt", cnt2)          # latches
    arr = ctx.array("buf", 16)        # packed storage
    arr.set_static(5, 3.25)
    v = arr.get_dynamic(cnt % 16)     # dynamic index
    fast = ctx.select(cnt > 12, 1.0, 2.0)  # if/else, both arms per tick
    ctx.soccer_move(v + fast, cnt2)

compile_graph(("soccer", "v0.12"), my_bot)   # -> game save folder directly
```

No node ids, no ports, no Float1. Dynamic `if`/`while` are rejected at
trace time with a pointing error (`select()` instead — both arms evaluate
per tick anyway, so semantics match the game). Anything untraceable fails
loudly: the supported-API whitelist is enforced, not promised.

## Why a description layer (not Python-nodes directly)

1. **Two languages, one backend** — the Rust crate emits the same
   description; the optimizing backend and its cost model exist once.
2. **CI-friendly** — descriptions are diffable, cacheable, reviewable; the
   sim replays a description without needing the Python runtime.
3. **Version pinning** — the backend owns the (game, version) tables
   (sensor ABI, controller ports). Frontends stay target-agnostic.
4. Same trick as LLVM IR / GCC's GIMPLE: many sources, one optimizer.

## Targets

Explicit, always: `("soccer", "v0.12")`, `("tennis", "v0.14")`, or
`("universal", version)` for unsupported games (raw node emission only, no
game API). Sensor/controller helpers exist only for pinned targets; the
surface tables live in `graphc/targets.py`.

## Cost model

Per-tick node transitions (nodes + edges) — each traversal is C# overhead
the game pays every tick. Optimizations minimize THIS, not code size or
FLOPs. Every compile returns the report; CI fails on regressions.

## Status

- Python tracing frontend: working (counter latches, packed arrays with
  write-merge, dynamic decode via select-chain, selects, CSE, const-fold).
- CI: compiled graphs replay in the aia_comp-sim VM with pinned assertions.
- Next: tennis v0.14 target surface (sensor ABI from the sim's api.rs),
  Rust crate emitting the same description, controller surface per game.

## Dev setup

- `GRAPHC_PYLIB` env var points at the AIGamePyLibrary checkout (the
  game-save emitter); defaults to `C:\gitProjects\AIA_tennis\AIGamePyLibrary`.
- Run the demo: `python examples/demo_soccer.py` (PYTHONPATH=repo root).