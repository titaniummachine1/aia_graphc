# graphc — compile code into AIA graph bots

Separate from the simulator on purpose: the simulator replays graphs, this
library turns **source code** into graphs. Architecture follows the classic
compiler pipeline (gcc/LLVM/rustc shape, scaled down):

```
Python lib (now)   ─┐
                    ├─► bot description (language-neutral JSON IR)
Lua subset (maybe) ─┘          │
                               ▼
                 graphc backend (Rust, graphc-rs): optimize (const-fold,
                 CSE, write-merge, budget check on per-tick transitions)
                 + emit game save format for an explicit (game, version)
                 target
                               │
               ┌───────────────┴────────────────┐
               ▼                                ▼
         game save folder                 aia_comp-sim VM (CI)
         (play immediately)               (replay + assert before play)
```

Rust stays as the backend + sim language. A Rust *source* frontend
(compiling Rust code into graphs) is shelved — absurd cost/benefit while
the Python frontend is unfinished. A Lua source frontend is the preferred
second language if anyone wants it (same description IR, zero backend
changes).

## The writer's experience (the whole point)

```python
from graphc.ast_fe import compile_source
import json, subprocess

source = '''
def bot(api):
    cnt = api.var("cnt")          # cross-tick RAM
    nxt = cnt + 1                 # plain arithmetic
    api.set_var("cnt", nxt)       # latches
    buf = api.array("buf", 16)    # packed storage
    api.arr_set(buf, 5, 3.25)
    v = api.arr_get_dyn(buf, cnt % 16)  # dynamic index
    flag = 1.0
    if cnt > 12:                  # real if/else, SSA phi-merged to select
        flag = 2.0
    api.move(v + flag, nxt)
'''

desc = compile_source(source, ("soccer", "v0.12"))
json.dump(desc, open("bot.desc.json", "w"))  # language-neutral IR, diffable
subprocess.run(["graphc-rs", "bot.desc.json", "bot.txt"], check=True)
# -> game save folder directly, plus a per-tick transition cost report
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
pinned set lives in `graphc/desc.py` (`SUPPORTED_TARGETS`/`check_target`,
enforced at trace time AND in the backend). Tennis sensor dropdown indices
resolve at trace time against AIGamePyLibrary's `DROPDOWN_OPTIONS`.

## Cost model

Per-tick node transitions (nodes + edges) — each traversal is C# overhead
the game pays every tick. Optimizations minimize THIS, not code size or
FLOPs. Every compile returns the report; CI fails on regressions.

## Status

- Python AST frontend (`graphc/ast_fe.py`): working — real `if/else` via
  SSA phi-merge, packed arrays, selects, CSE, tennis sensors + controllers,
  `vec_split`/`vec_make` for component math on vectors.
- Rust backend (`graphc-rs`): description → game save, 7 golden-desc unit
  tests green (`cargo test --lib`).
- CI: compiled graphs replay in the aia_comp-sim VM with pinned assertions
  (`graphc_poc_demo_replays`, `graphc_tennis_demo_replays`).
- Parity: serve-latch bot (13 nodes / 27 transitions) duplicates the sim's
  ServeAimHint latch — see `examples/demo_serve_latch.py`.
- Next: whatever the sim parity work demands. Rust *source* frontend is
  shelved; Lua is a documented option, unbuilt.

## Dev setup

- `GRAPHC_PYLIB` env var points at the AIGamePyLibrary checkout (the
  game-save emitter); defaults to `C:\gitProjects\AIA_tennis\AIGamePyLibrary`.
- Run the demo: `python examples/demo_soccer.py` (PYTHONPATH=repo root).