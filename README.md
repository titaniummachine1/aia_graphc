# graphc — write Python, get a game AI

Turn a plain Python bot into a visual-script graph the game loads directly.
You never touch nodes, ports, or wires — the compiler does that optimally.

## Simplest possible bot (tennis, 30 seconds)

`mybot/entry.py`:
```python
import AIA_Comp_Libry.tennis as t

def tick(api):
    if t.is_self_actively_serving():
        mx = -1.6
        mz = 10.5
    else:
        mx = 0.0
        mz = 11.0
    t.move(mx, mz, t.ball_in_swing_range(), 2.0)
```

Compile it:
```python
from graphc import compile_project
import json, subprocess

desc = compile_project("mybot/entry.py", ("tennis", "v15f"))
json.dump(desc, open("mybot.desc.json", "w"))
subprocess.run(["graphc-rs", "mybot.desc.json", "mybot.txt"], check=True)
```

Drop `mybot.txt` into `[game]/AIComp_Data/Saves/Tennis/`, load `mybot`
in the node editor. Done — it serves, rallies, and swings.

Three commands, total:
```
python -m pip install <this repo>   # once (needs GRAPHC_PYLIB, see below)
compile_project("mybot/entry.py", ("tennis", "v15f"))   # bot -> graph IR
graphc-rs mybot.desc.json mybot.txt                     # graph IR -> game save
```

## How it works (the 1-minute version)

- `tick(api)` runs once per game tick. Read the game through `t.*`
  sensors (`t.ball_speed()`), answer through `t.move(...)`.
- `import AIA_Comp_Libry.tennis as t` = latest tennis(nodes). Pin an
  exact version with `import AIA_Comp_Libry.tennis.v014 as t` instead.
  Wrong version for your target fails at compile time, loudly.
- Plain Python otherwise: helpers in any file (`import aim` just works),
  arithmetic, `if/else`, named memory (`api.var` / `api.set_var`),
  arrays (`api.array` + `arr_set` / `arr_get`). One controller call
  (`t.move`) per tick.
- Anything the compiler cannot turn into nodes fails HERE with a pointing
  error — never a silently different bot. If your AI misbehaves in game,
  it is doing exactly what you coded.

## The guarantee (idiot-proofing)

30-misuse battery, all loud, zero silent miscompiles: shadowed `api`,
double controllers / double latch writes, stdlib imports, wrong game or
version, unknown sensors, tuple unpacking, `while`/`for`, `and`/`or`,
ternaries, subscripts, walrus, recursion, top-level statements,
conflicting constants across files. Behaviour in game == behaviour coded.

## API reference

Every sensor is a typed, documented function — hover in any IDE:
`graphc/api/AIA_Comp_Libry/tennis/v15f.py` (108: bools, floats, vectors,
transforms), `soccer/v012.py` (175). Generated from the game's own
dropdown tables, so names can never drift: `t.ball_incoming()` reads
*Ball Incoming*; a typo fails with the full option list. `py.typed`
markers included — mypy/pylance work out of the box.

## Organizing bigger bots

Split across files freely — every function inlines at its call sites, so
the output is identical to one flat script:
```
mybot/
  entry.py      # tick() + strategy
  aim.py        # def serve_aim_x(api): ...
  consts.py     # SECOND_SERVE_SHORTEN = 0.5
```
Rules: one `tick(api)`, helpers return one float each, numeric constants
at top level, no `while`/`for` (state lives across ticks in latches).

## Under the hood (only if you care)

- `graphc/ast_fe.py`: Python AST -> description IR (SSA phi-merge for
  `if/else`, inlining, whitelist, `-O` DCE/select-fold; no arithmetic
  folding, float bit-identity kept).
- `graphc/desc.py`: language-neutral IR + (game, version) gates.
- `graphc-rs` (Rust): IR -> game save JSON, port tables pinned from
  AIGamePyLibrary, cost = **per-tick node transitions** (C# traversal
  overhead, not FLOPs), layered grid-snapped editor layout so the graph
  reads left-to-right like the code.
- `aia_comp-sim` (sibling repo): headless VM replays every compiled save
  in CI before it ever touches the game.

Targets: `("tennis", "v15f")` (latest), `("tennis", "v0.14")`,
`("soccer", "v0.12")`, `("universal", version)` raw-only. v15f nodes are
assumed v0.14-identical until measured.

## Dev setup

- `GRAPHC_PYLIB` points at the AIGamePyLibrary checkout (sensor ABI);
  defaults to `C:\gitProjects\AIA_tennis\AIGamePyLibrary`.
- Regenerate stubs: `python graphc/api/gen_api.py`.
- Tests: `cargo test --lib` (backend, 8 green). Python batteries live in
  the sim session; the 30-misuse battery is `idiot.py` there.
- Example rival bot: `examples/serve_latch_proj/` -> `graphc_rival.txt`
  (17 nodes, 36 transitions, beats aia3 7-0 in sim).
