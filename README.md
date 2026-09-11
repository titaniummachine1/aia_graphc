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

Drop `mybot.txt` into `%USERPROFILE%\AppData\LocalLow\Unicorn One\AIComp\Saves\Tennis\`,
load `mybot` in the node editor. Done — it serves, rallies, and swings.

Three commands, total (no install — run from the repo checkout):
```
cd <graphc checkout>                                  # once (everything runs in place)
compile_project("mybot/entry.py", ("tennis", "v15f"))   # bot -> graph IR
graphc-rs mybot.desc.json mybot.txt                     # graph IR -> game save
```
`graphc-rs` is `cargo build --release` in this repo
(`target/release/graphc-rs`); sensors resolve via `GRAPHC_PYLIB`
(defaults to the sibling AIGamePyLibrary checkout, see below).

## How it works (the 1-minute version)

- `tick(api)` runs once per game tick. Read the game through `t.*`
  sensors (`t.ball_speed()`), answer through `t.move(...)` (walk target)
  + `t.aim(...)` (strike target — the game switches aim without touching
  how you walk) + `t.auto_swing(...)` (hold builds charge, release
  strikes).
  `api.plot("channel", value)` records a TimePlot debug value — readable
  in game (TimePlot export), sim, and pure VM. It is the compiler-
  verification surface: examples/compiler_probe keeps golden values.
- `import AIA_Comp_Libry.tennis as t` = latest tennis(nodes). Pin an
  exact version with `import AIA_Comp_Libry.tennis.v014 as t` instead.
  Wrong version for your target fails at compile time, loudly.
- Plain Python otherwise: helpers in any file (`import aim` just works),
  arithmetic, `if/else`, and cross-tick memory as a **plain module
  variable** — if the bot writes it, it persists; if it only reads it, it
  is inlined as a constant. `api.array` + `set_array_cell` /
  `get_array_cell` for indexed RAM. One controller call (`t.move`) per tick.
- Memory, the Python way:
  ```python
  shots_seen = 0.0            # module variable the bot writes -> latch
  def tick(api):
      if t.ball_incoming():
          shots_seen = shots_seen + 1.0
      ...
  ```
  No `api.var`/`api.set_var`, no annotation. State must start at 0 (game
  variables start at 0). A variable written but never read is optimized
  away.
- Anything the compiler cannot turn into nodes fails HERE with a pointing
  error — never a silently different bot. If your AI misbehaves in game,
  it is doing exactly what you coded.

## The guarantee (idiot-proofing)

29-case misuse battery (`graphc/tests/test_misuse.py`, run it directly —
all loud, zero silent miscompiles): shadowed `api`, double controllers /
double latch writes (same cell twice), stdlib/star/missing imports, wrong
game or version, unknown sensors, tuple unpacking, `and`/`or`, ternaries,
subscripts, walrus, chained comparisons, `break` outside loops,
non-literal `range`, sinks inside loop bodies, missing returns, bad arity,
undefined names, top-level statements, plus project rules (one `tick`,
no conflicting constants). Bounded `for range(literal)` / `while` (64) /
recursion (depth 32) are real and unroll inline — over-cap, sink-in-body,
and depth-guard trips fail loudly with overflow canaries, never silently.
Behaviour in game == behaviour coded.

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
at top level. Bounded loops are fine (`for i in range(19)`, `while` cap
64, recursion depth 32 — all unroll to flat graphs with `!!` overflow
canaries); cross-tick state lives in latches (`api.var`/`set_var`), and
sinks (`move`/`plot`/`set_var`) hoist out of loop bodies.

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
- Tests: `cargo test --lib` (backend, 11 green);
  `python graphc/tests/test_misuse.py` (misuse battery),
  `test_calls.py` (call/closure semantics), `test_const_join.py`
  (float bit-identity) — all runnable directly, no pytest needed.
- Example rival bot: `examples/serve_latch_proj/` -> `graphc_rival.txt`
  (19 nodes, 41 transitions, beats aia3 7-0 in sim).
- Example underdog: `examples/underdog/` (walk-to-incoming-bounce,
  mirrored deep aim, AutoSwing — 26 ops, 25 nodes, 60 transitions).
  In `Saves\Tennis\underdog.txt`, loadable in the node editor.
