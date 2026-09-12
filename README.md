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

Compile it (one command — compiles to IR, runs the Rust backend, and drops the
save straight into the game's `Saves\Tennis\`):
```
python -m graphc mybot/entry.py -o mybot.txt --install
```
That is the whole pipeline. `graphc-rs` is auto-discovered next to this checkout
(`target/release/`, override with `--backend` or `GRAPHC_BACKEND`). Load `mybot`
in the node editor. Done — it serves, rallies, and swings.

Useful flags: `--target tennis:v0.14` (or `soccer:v0.12`) to compile for a
specific game/version, `-O o1`/`-O o2` to drop debug sinks / strip the editor
chrome (smaller save), `--desc out.desc.json` to inspect or hand-tune the IR.

<details><summary>Manual two-step (what the CLI does under the hood)</summary>

```python
from graphc import compile_project
import json, subprocess

desc = compile_project("mybot/entry.py", ("tennis", "v15f"))
json.dump(desc, open("mybot.desc.json", "w"))
subprocess.run(["graphc-rs", "mybot.desc.json", "mybot.txt"], check=True)
```
`cd <graphc checkout>` once — everything runs in place; `graphc-rs` is
`cargo build --release` in this repo (`target/release/graphc-rs`).
</details>


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

## Optimization modes (`optimize=`)

Performance is already maximal — the only graph cost is per-tick node
transitions — so the mode only decides **how much unnecessary material the
compiler may drop**. Behavior and play strength are invariant (verified in
the sim by `tests/compiler_mode_parity.rs`: the same bot at every mode
produces identical controller output, tick by tick).

| mode | frontend passes | emit |
|------|-----------------|------|
| `"raw"` | none | full chrome |
| `"o0"` (default) | identity fold (`x*1`, `x/1`, `x-0`, `x**1`, `not(not)`, `select(c,t,t)`) + DCE; keeps debug sinks | full layout + chrome |
| `"o1"` | o0 + drop debug sinks (`plot`, overflow canaries), re-run DCE | full layout + chrome |
| `"o2"` | o1 | **core**: nodes at 0,0, no colors / port rects / connection chrome, dense base62 ids — smallest file |

`compile_source` / `compile_project` take `optimize=`: `"o0"`/`"o1"`/`"o2"`
(also ints `0/1/2`, and aliases `normal`/`release`/`core`). Leave it out and
you get `o0`: fully optimised logic, and your `api.plot` debug channels still
work. Ship `o2` for the smallest file. `graphc-rs <desc> <out> [mode]`
overrides the description's mode.

### Compacting any existing save (no source needed)

Point `graphc-rs` at a save instead of a description and it auto-detects the
mode:
```
graphc-rs Titanium.txt Titanium.core.txt o2
```
It keeps the bot's strength by construction: nodes are dropped **only** when
nothing they produce can still reach a controller or a state sink. A value
that feeds both a `TimePlot` and the controller is kept — only debug-exclusive
chains vanish (this is the safe form of pylibry `stripDebugSinks`, which the
ladder flags as unsafe when applied blindly). `o2` also removes layout/chrome
(nodes at 0,0) and remaps ids to dense base62; `o0`/`o1` keep the editor
chrome. Measured: `Titanium.txt` 4.6 MB → 1.54 MB with identical sim
behavior for 60 ticks (`aia_comp-sim/tests/titanium_compact_parity.rs`).

## API reference

Every sensor is a typed, documented function — hover in any IDE:
`graphc/api/AIA_Comp_Libry/tennis/v15f.py` (108: bools, floats, vectors,
transforms), `soccer/v012.py` (175). Generated from the game's own
dropdown tables, so names can never drift: `t.ball_incoming()` reads
*Ball Incoming*; a typo fails with the full option list. `py.typed`
markers included — mypy/pylance work out of the box.

### Vector math, RLBot-style

The `api.*` surface has the vector building blocks RLBot bots lean on
(`Vec3`, `.length()`, `.dist()`, normalize). Each one is a single game node:

```python
ball   = t.ball_position()
bounce = t.predicted_bounce()

toward = api.normalize(api.vec_sub(bounce, ball))   # unit dir ball -> bounce
lead   = api.vec_add(ball, api.vec_scale(toward, 2.0))
reach  = api.distance(ball, t.center_of_back())     # |ball - back centre|
api.plot("reach", reach)
t.move_vec(lead, t.ball_in_swing_range(), 2.0)
```

| helper | meaning | node |
|---|---|---|
| `api.make_vector(x, y, z)` | `Vec3(x, y, z)` | ConstructVector3 |
| `api.split_vector(v, i)` | component `i` (0=x,1=y,2=z) | Vector3Split |
| `api.vec_add(a, b)` / `api.vec_sub(a, b)` | `a + b` / `a - b` | AddVector3 / SubtractVector3 |
| `api.vec_scale(v, s)` | `v * s` | ScaleVector3 |
| `api.normalize(v)` | unit vector | Normalize |
| `api.magnitude(v)` | `length(v)` | Magnitude |
| `api.distance(a, b)` | `|a - b|` | Distance |

Types are checked at compile time: a transform (`Self`/`Opponent`/`Ball`) or a
float where a vector is expected fails loudly, never silently coerces.
See `examples/bots/vec_geometry.py`.

**What we deliberately do NOT copy from RLBot:** its runtime (packets, sockets,
a long-lived process). graphc compiles to a static graph the game loads
directly; `python -m graphc` is the whole pipeline, and the same save replays in
the sim/VM for verification. The ergonomics are borrowed; the runtime is not.

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
  `if/else`, inlining, whitelist, `optimize=` passes — identity fold + DCE
  behind a mode; no arithmetic/const folding, float bit-identity kept).
- `graphc/desc.py`: language-neutral IR, (game, version) gates, and the
  `OPTIMIZE_MODES` resolver.
- `graphc-rs` (Rust): IR -> game save JSON, port tables pinned from
  AIGamePyLibrary, cost = **per-tick node transitions** (C# traversal
  overhead, not FLOPs), layered grid-snapped editor layout so the graph
  reads left-to-right like the code (o0/o1); o2 strips layout and chrome
  for the smallest save.
- `aia_comp-sim` (sibling repo): headless VM replays every compiled save
  in CI before it ever touches the game.

Targets: `("tennis", "v15f")` (latest), `("tennis", "v0.14")`,
`("soccer", "v0.12")`, `("universal", version)` raw-only. v15f nodes are
assumed v0.14-identical until measured.

## Dev setup

- `GRAPHC_PYLIB` points at the AIGamePyLibrary checkout (sensor ABI);
  defaults to `C:\gitProjects\AIA_tennis\AIGamePyLibrary`.
- Regenerate stubs: `python graphc/api/gen_api.py`.
- Tests: `cargo test --lib` (backend, 17 green);
  `python graphc/tests/test_misuse.py` (misuse battery),
  `test_calls.py` (call/closure semantics), `test_const_join.py`
  (float bit-identity), `test_modes.py` (optimization modes) — all
  runnable directly, no pytest needed.
- Example rival bot: `examples/serve_latch_proj/` -> `graphc_rival.txt`
  (19 nodes, 41 transitions, beats aia3 7-0 in sim).
- Example underdog: `examples/underdog/` (walk-to-incoming-bounce,
  mirrored deep aim, AutoSwing — 26 ops, 25 nodes, 60 transitions).
  In `Saves\Tennis\underdog.txt`, loadable in the node editor.
