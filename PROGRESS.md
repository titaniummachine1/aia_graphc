# PROGRESS — graphc (2026-09-11, session 3: compiler track)

## Session 21 (2026-09-13: two-stage interception + 2nd-bounce deadline)

- Shared evaluator now scores every (point, shot) with TRUE family flight
  times (sim ComputeShotVelocity, q=1) and shot-specific bounce physics
  (topspin kick 1.2x, slice skid, drop hop-clamp, spin floor), over TWO
  landings — victim takes min(first-bounce, second-bounce) coverage, each
  with stamina-gated walk/sprint/racket/swing tiers. Drop shots that die
  fast score correctly high when unreachable. Curve bend needs no term
  (landing-time evaluation; bend never moves the landing).
- Movement: two-stage ladder (live ball, then bounced state via ring
  inflation r+s*tb, same quadratic), walk-first selection (W0>W1, sprint
  only if stam>0.50 AND S0/S1 beats walking, else W2/fallback). S2 never
  selected. STAM_RESERVE=0.50 (Weaver's own gate ~0.10, no clean reserve
  const in its graph — 33%-vs-50% sweep still open, needs this build).
- Size fix without compiler change: per-opt ball-parameter helpers killed
  the dead dispatch arms — 10014->6401 nodes, 22640->14057 transitions
  (57% of ceiling). Literal-prune compiler attempt REVERTED (broke return
  protocol on nested inlining — parked with repro, not bypassed quiet).
- Verified: 0 numeric leaks, sim 7-0 vs stock, self-play 3-1, deployed.

## Session 20 (2026-09-13: one shared minimax, tier-scored)

- Attack and danger scans unified on `_vscore` (intercept.py): victim vs a
  virtual ball from the launch — score = ladder tier * 1000 + required
  speed, both directions, no duplicate logic. Shot search runs from our
  position (attack) and from his interception point (danger); his win-tier
  (`_his_tier`, same ladder) tells us if he sprints. Source-level blocks
  (loop bodies can't call helpers) share everything in-graph via CSE.
- Verified: 3159 nodes / 6732 transitions / 0 numeric leaks, sim 7-0 vs
  stock, self-play splits by server side, deployed as `titaniumpy`.

## Session 19 (2026-09-13: `while` banned — finite-state, not Turing-complete)

- `while` is now a loud compile error pointing at bounded `for`
  (`MAX_WHILE_TRIPS` removed): unrolling is target-forced (measured
  single-pass-per-tick, ModHost v0.15f — see
  `AIA_tennis/modhost/LOOP_SEMANTICS.md`), so a `while` has no guaranteed
  trip count and no bound is sound. Only `for range(literal)` + depth-128
  recursion remain. Misuse battery 33->34 cases (all suites green, titanium
  recompiles byte-identical counts).

## Session 18 (2026-09-13: v54-technique rewrite + loop semantics measured)

- Titanium rewritten to the recovered v54 algorithm (`AIA_tennis/titanium/
  python/build_titanium54.py`): stateless quadratic footrace ladder
  (walk 8.5 / sprint 13 / racket-ring 1.0 / swing-ring 2.6, strict priority),
  game ballistics (g=28, bounce keeps 0.78, ground 0.28, takeable y<=2.7),
  0.55 m racket-lead solve, chase without Ball Incoming (2nd-bounce
  ownership + live-ball fallback), sprint out (stamina>0.10), serve release
  at 0.7 charge, reverse-minimax attack scan (8 fixed points, req fitness,
  fastest-option shot travels with its point, fatigue shrink), virtual-ball
  positioning (his ladder -> 6-point danger scan -> bisection ->
  deep-center split + hold). Serve kept diagonal Flat (game-proven).
- Verified: 1961 nodes / 4181 transitions / 0 numeric modifiers, sim 4-0 vs
  stock, deployed as `titaniumpy`.
- Loop semantics MEASURED in the real game (ModHost v0.15f, notebook:
  `AIA_tennis/modhost/LOOP_SEMANTICS.md`): combinational cycles evaluate
  once per tick, back-edge delivers previous value (P1 ramp ->10, P2 ->11/10,
  never 10-at-0). Unrolling is target-forced; CSE audit on the 1959-op build:
  0.0% residual duplication — compiler exact, no change needed.
- Compiler rules learned (enforced, not documented before): helper names must
  be unique across project modules; no helper calls inside loop bodies
  (their returns trip the loop guard) — inline the math, hoist invariants.

## Session 17 (2026-09-13: commit label fix + serve-receive stance)

- Committed the Session 16 label-vs-index fix (emitter writes Unity TEXT,
  label-less sensor = hard error) with its regression tests (graphc 26/26).
- Titanium serve receive: interception before the serve bounce is impossible
  (game enforces Must Wait For Bounce), so `intercept.receive_x/z` holds a
  predictive stance — 1.05u behind bounce 1 towards bounce 2 — with fallback
  to in-game Receive Stance until `Ball Time To Ground` shows the aim is
  known. `plan_x/z` gate on `must_wait_for_bounce`; `entry.py` routes
  must-wait + serve-phase receivers to receive instead of the minimax chase.
- Verified: titanium v15f compiles (308 nodes, 20 tennis sensors, 0 numeric
  modifiers, new sensors Must Wait/Receive Stance/2nd Bounce present) and the
  save runs in the sim (tennis_tournament vs stock, 4 points, 4-0, no
  unimplemented nodes).

## Session 16 (2026-09-13: tennis sensor modifier = Unity TEXT, not index)

**Bug (root cause of "titanium57 sweeps the sim, cannot hit the ball in the
real game"):** the backend emitted `Op::TennisGet` as
`em.node(node_kind, index.to_string())`, but `TennisGetBool/Float/Vector3/
Transform` and `TennisAutoSwing` are `DROPDOWN_MODIFIER_AS_LABEL` nodes
(`AIGamePyLibrary/data.py`): Unity matches the dropdown on the option **text**,
so `modifier = "0"` names no option — the gate holds its default and every ball
sensor reads dead (`Ball Position == (0,0,0)`) for the whole match. Saves proved
it: working bots (`titanium54`, `Adam`, `Apex`,
`PerfectController_baseline`) store `"Ball Position"`; graphc saves stored `"0"`.

- Emitter now writes the IR's `label`; a label-less sensor is a **hard compile
  error** (an index is not a fallback — nothing game-side can resolve it).
  `TennisAutoSwing` already wrote labels and still validates its mode.
- Sim made strict so it cannot mask this class again:
  `graph::dropdowns::is_dead_label_modifier` (`label_matched` =
  the vendor set) blocks the index->label upgrade in
  `resolve_for_version` *and* on the version-unknown `load` path;
  `ApiSlotTable::intern` mirrors the game (dead `UNKNOWN_ID` slot) for a bare
  index, and still refuses **loudly** for a live-but-unpinned label (its catalog
  is builder-ordered, so guessing there is the phantom-entry bug).
- Regression tests pinning it: `tennis_sensors_emit_unity_labels_not_indices`
  + `tennis_sensor_without_label_is_a_loud_error` (graphc, 24->26),
  `numeric_modifier_on_label_matched_sensor_is_dead` +
  `label_matched_is_the_vendor_label_modifier_set` +
  `numeric_modifier_on_ordinary_node_is_untouched` +
  `dead_label_modifier_predicate` (sim dropdowns),
  `numeric_tennis_modifier_interns_dead_and_unpinned_label_refuses` (sim
  lower). Sim lib 176->182, graphc 24->26, integration suites all green.
- Measured after the fix: titanium (`v15f`, 266 nodes) has 15 tennis sensor
  nodes, **0 numeric modifiers**, vocabulary matching the in-game
  `titanium54.txt`.
- Write-up + evidence + which sim mode can simulate what:
  `aia_comp-sim/docs/TENNIS_MODIFIER_ENCODING.md` (cross-linked from
  `aia_comp-sim/docs/GRAPH_COMPILER.md` section 7).


## Session 15 (2026-09-13: verification round, all pushed)

- Pushed: graphc `159edc9` (session 14), sim `344cb48` (lower.rs only),
  modhost `d9728a2` + probe commit (ladder driver, results, serve probe).
- helperdemo (abs/sqrt/sign/clamp/dot/bool_and/bool_or + vector and bool
  selects in one bot) played a full v15f point: `H.c` live 42.5→62.4,
  DONE, no crash. New nodes are game-proven, not just sim-proven.
- Serve-aim strategy DECIDED: `Center Of Legal Serve Area` and `Receive
  Stance` read stub constants ((1,?,0) and (0,?,1)) in v0.14 AND v15f —
  probed both sides, both roles, 10k+ samples (probe_servearea, 43 nodes).
  Not a mirror bug: no role/side dependence at all. Serve Stance (index 6)
  is alive and correct-sided. Port rule: hardcode diagonal-box aims from
  court geometry (serves already land via world fallback — 0 faults).
  Alias `t.center_of_legal_serve_area()` kept (byte-identical, index 8).
- Sim `docs/GRAPH_COMPILER.md` corrected where it described the PoC
  sketch instead of the built compiler (mixed-radix arrays, cross-tick
  loop machines, every-variable-a-latch).
- Compiler preparation declared DONE: every blowup path is loud, misuse
  33+16+6, game ceiling measured, all suites green. No more capacity work
  scheduled before the titanium port.

## Session 14 (2026-09-13: titanium gap helpers + typed selects)

Exhaustive titanium54 cross-check (latest save): abs(59)/sqrt(45)/sign(3)
= Operation 0/10/11, and(85)/or(39) = CompareBool 0/1, ClampFloat(170),
DotProduct(14) — none had a one-node spelling. Closed with 7 `api.*`
helpers (abs/sqrt/sign/bool_and/bool_or/clamp/dot): new desc ops
(unary/bool_op/clamp/dot) + backend arms with the exact port tables +
`_REF_KEYS` extended (lo/hi) so DCE/chain stay sound.

Same session closed a REAL soundness hole the census exposed: vector and
bool `if/else` arms compiled to float selects (game drops/garbles those
wires — silent miscompile; titanium has 63 vector + 2 bool selects).
Selects are typed now (float/bool/vector -> the matching ConditionalSet
node, arm order pinned from the sim reference; transforms/arrays fail
loudly). Old descs without `typ` still load (default float).

Tests: `test_helpers.py` (4 + 6 loud), backend 24/24 (incl. legacy-desc
compat), all suites green, sim 176/0 + corpus sound, old bots rebuild at
identical op counts. Demo save census: Operation:0/10/11, CompareBool:0/1,
ClampFloat, DotProduct, ConditionalSetVector3 all present.

## Session 13 (2026-09-12: pure-Python tables)

User rule (binding): pure Python over `api.*` wherever possible. Lists
are tables now — no new API surface, the old `api.array` keeps working
underneath:

- `cells = [1.0, 2.0]` binds a frozen constant table (locals) or a module
  constant (never written in tick). Static reads inline to ZERO nodes
  (`cells[2]`, `tab[-1]`, `x = 5; tab[x]` via the SCCP static tag);
  dynamic reads (`tab[dyn]`) build the backend's own select-chain
  (`acc = cell0; select(idx==k, cell_k, acc)` — miss => cell0, verified
  structurally in tests). `[0.0] * n` sugar included.
- A module list the bot writes becomes RAM (packed-Vector3 array ops, the
  stock backend — no backend change): `mem[i] = v` needs a static index
  (literal, negative-wrapped, loop var, or pinned int) at tick top level;
  dynamic/branch/helper/recursion writes fail loudly, same for double
  cell writes. All-zero init enforced, same as scalar latches.
- `len(tab)` works (statically tagged, so `for i in range(len(mem))`
  fills a table — `_range_trips` accepts it). Tables never pass through
  helpers/arithmetic whole, never straddle a branch, `for`-targets cannot
  reuse table names, `tab.append` gets a pointing error (fixed-size HW).
- Caught by inspection mid-build: `tab[-1]` first miscompiled (unary
  minus bypassed the static path and the dynamic chain answered cell0) —
  now normalized Python-style. SCCP pruning is load-bearing here (static
  conditions legitimately hoist branch writes out of `_in_branch`).
- Tests: `graphc/tests/test_tables.py` (7 patterns + 16 loud cases);
  misuse battery's `subscript` case retired (now valid code — replaced by
  subscript-of-scalar); example `examples/bots/table_aim.py` (54 nodes /
  82 traversals, sim corpus parity green). Full suites green, old bots
  rebuild bit-identical costs.

## Session 12 (2026-09-13: RLBot-style vector math)

Ergonomics pass prompted by an RLBot comparison. RLBot bots lean on `Vec3`
(`sub`, `.length()`, `.dist()`, normalize); the compiler had only `make_vector`
/`split_vector`. Added the missing geometry as **plain `api.*` helpers**, each
one a single game node (no VM/graph changes — the sim already implements all of
them):

    api.make_vector(x,y,z)  ConstructVector3      api.normalize(v)   Normalize
    api.split_vector(v,i)   Vector3Split          api.magnitude(v)   Magnitude
    api.vec_add(a,b)        AddVector3            api.distance(a,b)  Distance
    api.vec_sub(a,b)        SubtractVector3       api.vec_scale(v,s) ScaleVector3

- `graphc/desc.py`: six `Sym` methods + op docstrings (`s` added to `_REF_KEYS`).
- `graphc/ast_fe.py`: the helpers in the `api.*` dispatch, with transform/float
  misuse errors matching the existing split_vector/make_vector messages.
- `src/lib.rs`: six `Op` variants, the game's exact port tables (from
  AIGamePyLibrary `data.py`), emit arms, and a `vec_val` helper (const→vector is
  a loud error).
- Tests: `vec_geometry_ops_emit_the_matching_nodes` (backend 21→22); Python
  misuse / const-join / modes suites green; `examples/bots/vec_geometry.py`
  compiles end-to-end (15 nodes). Sim `compiler_corpus_parity` still sound.

We deliberately do NOT copy RLBot's runtime (packets/sockets/long-lived
process): graphc still compiles to a static graph the game loads directly, and
the same save replays in the sim/VM. README "+ Vector math, RLBot-style".

## Session 11 (2026-09-12: one-command front door)

Usability pass (user directive: "make the compiler easier/more natural to use").
The pipeline was always two commands plus manual `graphc-rs` path wrangling; now
it is one.

1. ✅ **`python -m graphc`** (`graphc/cli.py` + `graphc/__main__.py`):
   `python -m graphc mybot/entry.py -o mybot.txt --install` compiles source →
   IR → save and copies the save into the game's `Saves\Tennis\` (or
   `Saves\Soccer\` for `--target soccer:v0.12`). Auto-discovers the backend at
   `target/release/graphc-rs[.exe]` (override `--backend` / `GRAPHC_BACKEND`),
   parses `game:version` targets (bare `tennis` → `v15f`, `soccer` → `v0.12`),
   accepts a project dir (uses its `entry.py`), and can also dump the IR
   (`--desc`), pick a mode (`-O o1`/`o2`) and stay quiet (`-q`).
   - Errors still fail loudly: unknown target, missing entry/backend and any
     backend non-zero exit are surfaced with the backend's own stderr.
2. ✅ README "Simplest possible bot" now leads with the one-liner; the manual
   two-step is kept in a collapsible block.

No backend/IR changes; `cargo test --lib` untouched.

## Session 10 (2026-09-11, compiler track: optimization modes + source-free compaction)

User directive: "optimisation modes O0/O1/O2 ... only tell the compiler how
much unnecessary stuff to drop; performance is already maximal (the only
graph cost is per-tick node transitions)". And: "run the compression on any
script even without Python — give you Titanium and you run o2/core ... without
affecting strength." Done:

1. ✅ **Modes** `raw` | `o0` (default) | `o1` | `o2` on
   `compile_source`/`compile_project` (`optimize=`; ints 0/1/2; aliases
   normal/release/core/debug/max). `graphc/desc.py`: `resolve_optimize` +
   mode-aware `optimize_ops`. `graphc/ast_fe.py` carries the mode into the
   desc (`"optimize"` field); `src/lib.rs` `Mode` parses it; `graphc-rs`
   3rd arg overrides.
   - `o0`: identity fold (`x*1`, `1*x`, `x/1`, `x**1`, `x-0`, `not(not)`,
     `select(c,t,t)`) + DCE; keeps debug sinks + layout. Bit-safe only —
     `x+0` is deliberately NOT folded (flips -0.0).
   - `o1`: o0 + debug sinks (`plot`, overflow canaries) are not DCE roots;
     everything that fed only debug disappears.
   - `o2`: o1 + emit core (`core_strip`: no rects/colors/port rects/conn
     chrome, nodes at 0,0; `remap_short_ids`: dense base62, now also remaps
     `ownerFunctionSID` so functions survive).
2. ✅ **Fixed a latent infinite loop** in `optimize_ops`: a folded op stayed
   in the list and re-triggered the fold forever (old select-fold had the
   same latent bug, never hit). Fix: rebuild to the live set each pass.
3. ✅ **Source-free compactor** `src/compact.rs` + `graphc-rs` auto-detect:
   give it any save (no Python/source) and it drops only what is provably
   unnecessary — backward reachability from actions (`*Controller`,
   `SetVariable`, array writes, `CreateFunction`) + non-debug terminals;
   debug sinks are roots only when keeping debug. A producer feeding BOTH a
   TimePlot and a controller is KEPT (the AIA/AIA3 failure pylibry's ladder
   warns about). `compact` defaults to `o2`.
   - `Titanium.txt` 4.64 MB → 1.54 MB (o2), 30 truly-dead nodes pruned,
     identical sim behavior for 60 ticks.
4. ✅ **Tests**: `graphc/tests/test_modes.py` (6); Rust 21/21 (mode parse,
   core shrink, unknown-mode loud, compact keeps shared producer, o0 keeps
   debug, o2 chrome+ids). Sim: `tests/compiler_mode_parity.rs` (same bot at
   o0/o1/o2 → identical controller output 40 ticks + o0 debug TimePlots
   work), `tests/titanium_compact_parity.rs` (any-save compaction, opt-in
   `TITANIUM_ORIG`/`TITANIUM_COMPACT`). Probe pins updated 94/91 → 93/90.
5. ✅ **Docs**: README "Optimization modes" + compact usage; `__init__` /
   `desc` docstrings; sim `AGENTS.md` probe pins + mode-parity note.

Compiler is now effectively **v1**: feature-complete for authoring + mode
selection + arbitrary-save compaction. Only optional gaps remain (vector
arithmetic ops; Lua frontend). Next real work is sim parity (see
`aia_comp-sim/docs/HANDOFF.md`).

## Session 9 (2026-09-11, compiler track: plain-variable state + QOL)

User directive: "replace api.set_var with just regular python variables —
we have a python parser." Done, with the one simple rule ("written =>
dynamic, never written => constant"):

1. ✅ Auto cross-tick state (`graphc/ast_fe.py`): a module-level numeric
   variable the bot ASSIGNS becomes a latch — first read pulls
   GetVariable, the single end-of-tick value emits SetVariable, branch
   writes merge to select. A module variable the bot only reads stays an
   inlined constant. No `api.var`/`api.set_var`, no annotation. State must
   init to 0 (game vars start at 0) — loud otherwise. State assigned from a
   loop/recursion/helper is loud (ambiguous write order). `global x` is
   accepted (declarative no-op).
2. ✅ Cross-tick DCE (`graphc/desc.py` optimize_ops): a latch written but
   never read is dead storage — demote the var_set and let liveness drop
   its whole value chain (transitions are the cost metric). Verified:
   write-only state compiles to ZERO var nodes; read+write stays.
3. ✅ Frontend QOL fixes (found writing 4 test bots): pure `api.*` reads
   (sensors, split_vector, position_of, var, array reads, auto_swing) are
   now allowed inside `if` branches (only sinks stay loud); a variable
   first assigned inside one arm is no longer mis-typed as float (treated
   as path-local; a later read fails as path-dependent). 4 example bots
   (`examples/bots/`: pusher, open_court, alternator, cross_court project)
   compile and play; alternator rewritten to plain variables and matches
   the api.var build bit-for-bit (same 7185/8483-tick outcomes).
4. ⏳ Parity methodology (user directive): exact 1:1 parity is SHELVED
   (matched first-server table was 8/78, ~3 min/seed to measure, plus RNG
   — an endgame task). Target is now STATISTICAL equivalence: same
   starting-condition distribution => same outcome distribution over many
   games. Note for later: the sim ignores `t.aim()`/AutoAim unless
   `AIA_AIM_MODEL=separate` (measured 18/78 separate vs 24/78 legacy on the
   mismatched-start set — both invalid pending matched starts).

## Session 7 (2026-09-11, compiler track: assist chain + underdog + battery)

User stress-testing the API: the first underdog held swing forever (charges,
never releases, never serves — hold-to-charge/release-to-strike was only
prose). Fixes, all verified:

1. ✅ Misuse battery materialized (`graphc/tests/test_misuse.py`, was
   vapor): 29 loud cases + project rules (two ticks, conflicting consts)
   + legit-pattern guards, runnable via plain `python`. First run caught
   a REAL hole: same-cell double `arr_set` compiled silently (backend
   last-wins). Frontend now rejects it (`_set_cells`, same pattern as
   `_set_vars`); legit multi-index packing untouched. 29/29 + rules green.
2. ✅ `tennis_move`/`tennis_move_vec` route through the native assist
   chain (request -> TennisAutoAim -> TennisAutoMove(V32) + request ->
   AutoMove(V31) -> controller), the titanium pattern. PORTS entries
   copied exact from AIGamePyLibrary `data.ports`. Swing stays direct
   (AutoSwing would replace the bot's charge gate). Backend 11/11
   (wire test now asserts the chain); sim replays bit-identical
   (pass-through) — both demo replays green on rebuilt saves.
3. ✅ Underdog (`examples/underdog/`, 20 lines): serve legal target,
   rally deep-middle, swing = `chg >= 0.7 ? release : in_range`.
   17 ops / 18 nodes / 39 transitions, deployed to Saves as
   `underdog.txt`. Sim: 7-0 vs titanium54 (both sides), 7-0 vs aia3,
   0 faults — serves land box-center, toss hangs game-style while
   charging. CAVEAT (recorded, not hidden): titanium sprays wide shots
   OUT in-sim (also 0-7 vs graphc_rival) — almost certainly a sim
   flight/assist gap (game AutoAim correction unmodeled), NOT proven
   strength. Game run needed for the honest verdict.
4. ✅ Costs re-pinned (assist +2 nodes/+5 transitions per controller):
   tennis demo 15n/35t (was 30t), serve-latch 15n/32t (was 27t),
   rival 19n/41t (was 17n/36t), soccer 83 unchanged. Rival still 7-0
   vs aia3 on the rebuilt save. README + `t.move` stub docs updated
   (assist routing, hold/release swing rule); pycache purged.

## Session 8 (2026-09-11, compiler track: split drive from pylibry reference)

User correction (right on all counts): the bot walked to its aim (off the
board), couldn't follow the ball, and never touched AutoSwitch/AutoSwing —
plus "watch upstream and our pylibry, what nodes it has, how they are
supposed to be used, as main reference". Did exactly that. Reference
findings (`nodes.py` docstrings, identical upstream/local):
- `TennisAutoSwitch(position, aim)` (= `TennisAutoMove` alias): "raw
  controller Vector31 is read as *either* a move destination (own half)
  *or* an aim landing (opponent half), **never both** — this node is how
  you steer feet and target independently." Single-vector `t.move` was
  wrong by construction; "Controller ports expect AutoMove/AutoSwing".
- `TennisAutoSwing(shot_type, mode)`: Normal Only | Prefer Charge |
  Random; Prefer Charge "holds once Is Ball Playable is true and releases
  at the contact window". Modifier stored as the LABEL (titanium54 save
  evidence: `'Prefer Charge'`, not an index).
- `TennisAutoAim(direction=None)`: "legal opponent-court landing" (the
  node itself constrains — supports the wide-aim correction hypothesis).
- Sensor side semantics (recovered native headers + old titanium bots):
  Center Of Half/Back read OWN half — rival/underdog aims were own-half
  wires (rejected by sim latch → fallback; in game they'd be move
  destinations). Aim at far half = negate x.
Fixes, all verified:
1. ✅ New author calls: `api.tennis_aim(x, z)` / `t.aim(x, z)` (aim
   request for the NEXT move; one per tick, aim-without-move loud,
   aim-after-move loud in backend) and `api.tennis_auto_swing(shot,
   mode='Prefer Charge')` / `t.auto_swing(...)` (bool out; mode
   validated loudly). Backend: AutoAim/AutoSwing nodes, pending-aim
   consumed by the next controller, legacy fallback (move vec feeds
   both) when no aim call — old bots compile byte-identical graphs.
   Backend 14/14 (aim-split, aim-ordering, autoswing tests).
2. ✅ Underdog v4 (`examples/underdog/`): walk = stance on serve,
   predicted bounce while `ball_incoming()`, own back-center otherwise
   (never chases its own shot across the net or a dead ball); aim =
   legal target on serve, mirrored deep-middle otherwise; swing =
   `auto_swing(2.0)`. 26 ops / 25 nodes / 60 transitions, deployed.
   Sim vs aia3: 5-3 points, game 1-0, 0 faults, stays own half
   (rally x in [-16.6, -5.08]), serves land box-center.
3. ✅ Full-name aliases landed (`set_array_cell`, `split_vector`,
   `position_of`, …): both spellings compile byte-identical (pinned by
   test); examples + docs migrated, shorts still accepted.

## Done this session (all verified)

1. ✅ Deleted `graphc/core.py`, trimmed `graphc/__init__.py` (now exports
   `compile_source` / `describe` / `tennis_sensor_index` /
   `SUPPORTED_TARGETS` / `check_target`), ported
   `examples/demo_soccer.py` onto ast_fe. Demos reproduce 83 / 33.
2. ✅ `vec_split` / `vec_make` / `tennis_move_vec` in desc IR + ast_fe
   (`api.vec_split(v, i)` / `api.vec_make(x, y, z)` /
   `api.tennis_move_vec(v, ...)`) + Rust backend (shared Vector3Split
   per source, loud errors on const/unknown sources). Fixed a latent
   `"=="`-instead-of-`"0"` modifier in the array-dynamic path.
3. ✅ Target gating both sides: (`soccer`,`v0.12`) / (`tennis`,`v0.14`) +
   (`universal`, any) raw-only; everything else `TypeError`/`Err` loudly.
4. ✅ Serve-latch parity bot `examples/demo_serve_latch.py`: 13 nodes /
   27 per-tick transitions (cheaper than the 33 demo). VERIFIED vs the
   sim's `9b8af82` ServeAimHint latch (seed 7, headless tournament):
   - Sim e2e replays green post-change (`graphc_poc_demo_replays`,
     `graphc_tennis_demo_replays`; tennis aims alternate neutral/serve).
   - Latch bot serving (vs aia3, away): ServeSetup Vector31 =
     (-3.5,∓3.0), alternating with ad court = the live Legal Serve
     Target sensor; first-bounce landings (-3.61,±3.00) = within 0.11 m
     of the aim → the world's latch HONORED our candidate (no fallback).
     0 faults / 0 double faults, held serve 4/4, broke once (6/8 pts).
   - Control (old demo, same seed): Setup aim (0,11) out-of-box →
     world FALLBACK saves it; identical landings (-3.61,±3.00). Same
     serves, different path — the compiler latch duplicates the native
     model instead of relying on the fallback.
   - No unimplemented/approximated nodes on the compiler side.
   - ANOMALY (sim-side, flagged not fixed): demo-vs-aia3 match reports
     Finished after 7 points with games 0-0 (trace shows a 28 m flypast
     landing). Needs sim-session eyes; compiler outputs were legal.
5. ✅ 7 Rust golden-desc unit tests (`cargo test --lib`): vals alignment,
   port-polarity endpoints, dropdown indices, vec sharing/wiring,
   vec errors, target gating.

## Shelved / optional (user directive 2026-09-11)

- **Rust *source* frontend shelved**: compiling Rust code into graphs is
  absurd cost/benefit while Python is unfinished. Rust stays as the
  backend (`graphc-rs`) + sim language. Do NOT start a `.ten`/Rust
  frontend until Python (+ maybe Lua) frontends are done.
- **Lua source frontend (optional)**: preferred second language if an
  author wants it. Design: `graphc/lua_fe.py` with a hand-rolled
  restricted-subset parser (locals, `+ - * / % ^`, `< > <= >= == ~=`,
  unary `-`/`not`, `if/then/else/end`, `api.*` calls mirroring ast_fe;
  1-indexed Lua numbers need no translation — only literal indices are
  accepted) emitting the SAME description IR, so zero backend changes
  and the same golden tests apply. Greenfield: no Lua anywhere in
  either repo today. Build only on explicit author request.

## Next moves (blocked on sim parity — nothing actionable here)

All 5 compiler items are done. What comes next depends on what the sim's
rally-aim work demands of bot expressiveness (new sensors? bool logic?
within-branch reads?). Until then: no compiler work is justified — do not
gold-plate. (Rust source frontend: shelved. Lua: documented, unbuilt.)

## What exists NOW

- **Rust backend** (`src/lib.rs`, bin `src/bin/graphc_rs.rs`) — CI-VERIFIED
  (the sim replays its saves; `cargo check` alone is NOT enough — see
  "bugs fixed this session"). Description IR (graphc-desc-v1) → array
  expansion (pack 3 cells/Vector3 var, same-vector write MERGE into one
  RMW) → version-pinned port tables → game save JSON. Cost report:
  nodes + connections = per-tick transitions.
- **PORTS table = ground truth**: copied EXACTLY (order + polarity) from
  AIGamePyLibrary `data.ports` (soccer + tennis nodes). Polarity != 0 marks
  output ports. Connection endpoints resolved by (name, polarity) — same
  rule as the sim loader and AIGamePyLibrary.
- **CompareFloats modifier = Unity Operation dropdown INDEX in the save**
  (0=="==" 1=="<" 2==">" 3=="<=" 4==">="; the sim eval parses it as i32,
  missing/unknown => equality). The desc IR keeps operator strings; the
  backend translates (cmp_modifier in lib.rs).
- **Description IR** (`graphc/desc.py`) — ops: const/var_get/var_set/bin/
  not/select/array + array ops + soccer_move + **tennis_get** (kind
  bool|float|vector3|transform, index resolved at trace time from
  AIGamePyLibrary DROPDOWN_OPTIONS, label kept for reviewable descs) +
  **tennis_move** (x,z → ConstructVector3 → TennisController; optional
  swing/shot/sprint). `_desc` now always returns int op ids (it used to
  leak Sym objects into op dicts).
- **AST frontend** (`graphc/ast_fe.py`) — the authoring path:
  api.var/set_var/array/arr_set/arr_get/arr_get_dyn/move (soccer-gated) +
  **api.tennis_get_bool/float/vector3/transform + api.tennis_move**
  (tennis-gated). Real `if/else` via SSA phi-merge of assigned names.
  api.* calls parse as ast.Attribute (obj.attr), not ast.Name.
- **Old tracing frontend** (`graphc/core.py`) — STILL PRESENT, still used
  by `graphc/__init__.py` (compile_graph) + `examples/demo_soccer.py`.
  NOT deleted (next-session step said "if unused" — it is used). Deleting
  it means rewriting demo_soccer onto ast_fe and trimming __init__.
- **Targets**: ("soccer","v0.12") and ("tennis","v0.14") both compile e2e.

## Verified end-to-end (sim CI, both green)

- `graph_vm::runtime_brain::tests::graphc_poc_demo_replays` — soccer demo,
  Rust-emitted save, counter latch + packed-array decode + select flag.
- `tennis::e2e_tests::graphc_tennis_demo_replays` — tennis demo (serve-latch
  shape: if/else aim merge on "Is Self Actively Serving", "Serve Number"
  shortens second serve, "Ball In Swing Range" → swing, shot=Flat).
  Distinct aims observed: (0,11) neutral vs (-1.6,10) serve branch — the
  phi-merge + sensors + controller all live through the sim VM.
- sim lib suite: 162 passed.

## Bugs fixed this session (all found by the e2e, cargo check was green)

1. ast_fe: api.* call detection (Attribute not Name) + leftover duplicate
   line + missing api.move in whitelist.
2. Backend: `vals` vec must stay index-aligned with op ids — non-value ops
   (var_set/array_set_static/soccer_move/tennis_move) now push placeholders.
3. Backend: dynamic array reads need splits for ALL packed vecs (flush_vec
   early-returns without creating them).
4. Backend: PORTS table order/polarity was WRONG for most nodes (AddFloats
   out first, CompareFloats Bool1 out first, etc.) → saves wired garbage;
   variables never persisted. Rebuilt from AIGamePyLibrary data.ports.
5. Backend: per-port instance sids (duplicate port names — in/out both
   named "Float1" — collapsed in a HashMap and connections resolved to the
   wrong port).
6. Backend: CompareFloats modifier now translated to dropdown index (was
   "==" string → sim parsed as 0 → every comparison silently became ==).

## Next-session first moves

1. Delete `graphc/core.py` + trim `graphc/__init__.py` to not re-export it;
   port `examples/demo_soccer.py` onto ast_fe (or drop it — demo_ast covers
   the same bot). Keep `desc.py` (the IR + tennis_sensor_index helper).
2. Vector plumbing in the desc IR if needed by real bots: tennis_get
   vector3/transform currently produce opaque single-value nodes — they
   feed tennis_move's Vector31 fine, but there is NO vec_split/vec_bin op,
   so component math on vectors is impossible. Add `{"op":"vec_split"}` /
   `{"op":"vec_make"}` (backend: Vector3Split / ConstructVector3) when a
   bot needs it (serve-latch on "Legal Serve Target" components needs it).
3. Tennis v0.14 gating beyond game name: ("tennis","v0.12") vs ("tennis",
   "v0.14") currently behave identically — the version string is recorded
   but nothing branches on it. Decide: reject unknown versions loudly.
4. Serve-latch parity bot (the payoff experiment): compile a bot whose
   serve aim latches legal-serve-target components (needs vec_split) and
   compare behavior against the sim's `9b8af82` ServeAimHint latch
   (aia_comp-sim). The sim session already fixed serve parity in Rust;
   the compiler route is now the duplication/verification path.
5. Rust-side unit tests for lib.rs (vals alignment, port resolution) —
   every bug this session was only catchable via the sim e2e; cheap
   golden-desc tests would have caught 2/3 of them locally.

## Verified facts the compiler relies on (pinned by tests)

- Variables persist across ticks; same-tick store is visible to later
  loads (accumulation test climbs 1,2,3,4).
- `ConditionalSetFloatV2` = select (Bool1 cond, Float1 true, Float2 false);
  unwired false port = native previous-tick HOLD register.
- Packed arrays: 3 float slots per Vector3 variable; backend merges
  same-vector static writes into one split+construct+store per tick.
- Save format: the game loads lean nodes (all ports with polarity, uuid
  sids, zero rects) + connections (port0SID/port1SID) — matches
  AIGamePyLibrary's own output shape.
- Port polarity: 1 = output, 0 = input (loader + AIGamePyLibrary agree).
- Dropdown modifiers are stored as builder-order indices.

## User's optimization directive (binding)

Compile-time target = **per-tick node transitions**, NOT code size or
FLOPs — every block traversal is C# overhead paid every tick. The report
prints it; CI fails on regressions. Current: soccer demo 83, tennis demo 33,
serve-latch parity bot 27.

## Session 4 (2026-09-11, compiler track: projects + API libs)

1. ✅ Multi-file projects: `compile_project(entry.py, target)` in
   `graphc/ast_fe.py` (exported). Crawls sibling imports (packages via
   `__init__.py`), inlines every project function at call sites (defaults,
   `api`-as-argument, nested calls; recursion/missing-return/arity fail
   loudly), numeric module constants, `tick`-or-single bot rule.
   Verified: flat project desc == `compile_source` desc; split 2-file
   project == same GRAPH (14 nodes, order-independent shape check).
   Rejections verified: recursion, star imports, stdlib imports, top-level
   statements, missing return, undefined names. `compile_source` shares the
   same assembler (helpers now allowed single-file too).
2. ✅ Per-(game,version) API libs: `graphc/api/gen_api.py` generates
   `tennis_v014.py` (108 sensors) + `soccer_v012.py` (175) from the fork's
   DROPDOWN_OPTIONS. `from tennis_v014 import ball_in_swing_range` compiles
   to the identical graph as the api.* form (verified, 11 nodes).
   Wrong-version import fails loudly (pinning); unknown names fail loudly.
   New desc op `soccer_get` (resolver `soccer_sensor_index` in desc.py) —
   backend lowering PENDING (Rust must fail loudly on it until lowered).
3. ✅ Const-fold: unary-minus literals fold (`-1.6` = one const, was Sub).
4. ⏳ Optimizer passes: `optimize_ops` in `graphc/desc.py` (`opt=0/1` on
   compile_source/compile_project) — DCE from side-effect sinks +
   select(c,t,t) fold, NO arithmetic folding (float bit-identity).
   Verified: waste bot 6 ops -> 3, backend lowers both, 31 -> 30
   transitions, sim headless replays bit-identical (1601 ticks, same
   winners). Default opt=1.
5. ⏳ `soccer_get` Rust backend lowering — next (PORTS entries exist).
6. ✅ Layered layout in the backend (`layout_positions`, same 1263/350 pitch
   as pylibry autoLayout): longest-path layers, x grows with depth
   (sensors/consts left, controller rightmost), barycenter crossing sweeps,
   sim-inert positions verified by bit-identical headless replay. 8 Rust
   tests green. Proof: 15-node bot fans 1263 -> 3013, zero pile-up. (Real
   bots like titanium54 ship all 5383 nodes at 0,0 — the game tolerates it;
   ours now show their work.)
7. ✅ Width-aware pitch (user eyeball feedback): layer gap = half-widths +
   120 from NODE_SIZES (320/256/192), so wide nodes never overlap
   horizontally. Open question back to user: per-kind grid measurements +
   whether modifier text stretches nodes (then size by text length).
8. ✅ AIA_Comp_Libry package hierarchy (user directive): generator emits
   `AIA_Comp_Libry.<game>.<ver>` (`tennis.v014`: 108, `soccer.v012`: 175).
   All 3 import forms compile (`import ... as t`, `from ...v014 import x`,
   `from ...tennis import v014`); version mismatch fails loudly. Rival
   example ported; same 17 nodes / 36 transitions, replay identical.
9. ✅ Latest-by-default + v15f (user directive 2026-09-11): `("tennis",
   "v15f")` accepted everywhere (Python + Rust gates), nodes assumed
   v0.14-identical; unversioned `AIA_Comp_Libry.tennis` (= latest v15f)
   in all import forms; mixing latest with a v0.14 target (or v014 with
   v15f) fails loudly. Stubs regenerated with per-sensor docstrings.
10. ✅ Idiot-proof audit (user directive: misbehaving AI is provably the
    author's fault): single controller per tick, single set_var/array per
    name per tick, no `api` rebinding anywhere (assign/augassign/param/
    const/function), conflicting cross-file constants loud, tailored
    errors for and/or/ternary/subscript/walrus, project-import whitelist
    in single scripts too. 30-case battery: 30/30 loud, legit patterns
    green, graph-equivalence intact.
11. ✅ Docs for humans + LLMs + IDEs: 391/391 sensors carry hand-written
    descriptions (tennis from parity forensics, soccer from game
    semantics) into stub docstrings; `py.typed` markers; README rewritten
    simplest-first (10-line bot -> 3 commands -> guarantee -> API ->
    projects -> internals).
6. ⏳ Sim side (aia_comp-sim, same session): measured serve-area box wired
   (`court.rs` SERVE_AREA_BACK=2.25, 163 tests green); setup-server table
   (`reset_sweep.jsonl`) wired into `run_sim_tournament_pairs.py`
   (per-row AIA_FIRST_SERVER + resume-safe skip). Full 78 replay with
   partial table: 27/78 = 34.6% (baseline 25/78). Table completion (~60
   rows, `table_build.py`) continues to be the honest-parity lever.

## Session 5 (2026-09-11, compiler track: simple-to-use hardening)

1. ✅ Type-checked connections: every SSA value typed
   (float/bool/vector/transform/array) in `graphc/ast_fe.py`; illegal
   node wiring fails loudly at compile time (bool into arithmetic,
   vector into float slots, transform into vec_split/move_vec, float
   as if-cond/swing/sprint, mixed if/else arm types, set_var/arr_set
   non-floats). Verified: 6/6 illegal probes loud, legal bots green.
2. ✅ Node input/output reference: new `graphc/nodes.py` (NODE_DOCS for
   all 18 emitted kinds + IR_OPS for all 16 desc ops) — LLM-readable,
   single source of truth; referenced from `graphc/__init__.py`.
3. ✅ Stub docs with types: `gen_api.py` emits Vector3/Transform marker
   classes, `-> bool/float/Vector3/Transform` annotations, and per-sensor
   Returns + game-node + label docstrings (tennis 108x2, soccer 175
   regenerated). move/move_vec document arg types + auto-wiring.
4. ✅ Auto-wiring guarantee kept + documented: authors write values only,
   never nodes/ports/wires. Verified: demos rebuild identical
   (soccer 83, tennis 30, serve-latch 27 transitions), project example
   18 ops, `cargo test --lib` 8 green.

## Session 6 (2026-09-11, compiler track: debug sinks, loops, recursion, soccer reads)

Cost model refined (user directive, binding): LEXICOGRAPHIC — minimize
per-tick transitions first (tick-invariant: every op fires once per think,
so the static count IS the average); only among transition-equal options
pick the smallest file. Unrolling never reduces transitions (N trips x body
either way — no rolled form exists in the graph language, and both select
arms evaluate, so inactive trips still fire); it preserves this-tick
semantics, and the optimizer then minimizes the flat form. Across-ticks
latch machines are the transitions-cheap alternative (author's choice).

1. ✅ `api.plot(channel, value)` (TimePlot sink, all targets incl.
   universal): frontend + desc (`plot` op, DCE sink) + nodes.py docs +
   backend (String + 6-port TimePlot). Misuse battery 6/6 loud;
   DCE keeps plotted / drops dead verified. Backend suite 9 green.
2. ✅ Bounded control flow (all in ast_fe.py, flat graph out, no backend
   change): `for i in range(literal)` unrolled (break/continue via
   select-gating, exact-trip loops emit zero overhead); `while cond`
   unrolled to 128 + `!!while_overflow` canary (burns the cap every tick
   — documented, prefer latches); recursion inlines to depth 32 +
   `!!recursion_overflow` canary (house style with conditional calls AND
   guard-clause early returns via _FnReturn protocol). Sinks in loop /
   recursive bodies fail loudly (hoist). Caps: 4096 trips, 100k ops,
   lowering-depth guard trips x depth <= 1000 (Windows 1MB main-thread
   stack overflows past it — measured STATUS_STACK_OVERFLOW, then
   calibrated).
3. ✅ SCCP-lite static domain (ints abs < 2**24, bools): branch pruning
   ONLY, values still lower as floats (bit-identity untouched). Effects
   measured: gcd(48,18) 171 -> 4 ops, fib(6) tree 42 ops exact both
   shapes, fib(20) exact 32841 ops, for-break loop 123 -> 10 ops.
   Fixed latent bug: bool consts shared _desc ops with floats (type tags
   flipped with emission order) — dedicated ops now.
4. ✅ fp32-bits join rule (user directive): same bits => same node.
   Verified `1`/`1.0` share one Float node; backend test
   `same_fp32_bits_share_one_float_node`; frontend
   `graphc/tests/test_const_join.py`. Backend suite 11 green.
5. ✅ `soccer_get` backend lowering DONE (Session 4 item 5 closed):
   bool/float/vector3/transform + `api.pos_of` (RelativePosition World,
   modifier 13). Index order verified equal both sides
   (Team Player 1 == 1). Frontend `api.soccer_get_*(label)` +
   `api.pos_of(t)`, misuse-loud. Backend test
   `soccer_get_and_transform_pos_emit`.
6. ✅ Live probe `fib(position.x) -> debug` (sim side
   data/compiler_probes/live_position_fib.txt): Team Player 1 transform
   -> pos -> x -> fib table 0..19 -> LIVE.x/mi/fib plots. Sim-verified
   (x=-0.9506 -> mi=19 -> 4181 exact). Property is self-consistency per
   tick (holds in any world) — the game-vs-sim check.
7. ✅ Sim-side handoff (aia_comp-sim): scripts/run_compiler_probe.py
   builds both fixtures; tests/compiler_probe.rs pins goldens + costs
   (probe 94 nodes / O0 91 / O1 80; live 94 / 94 / 85) + 40-tick live
   self-consistency; scripts/compare_compiler_probe.py scores a game
   TimePlot export (static exact + order canaries + LIVE relations).
   Game procedure: load .txt as team, record TimePlot, export, compare.
8. ✅ Call-eval-order bug (found by values run: V.gcd read 18, want 6):
   params bound into the shared env one-by-one, clobbering caller locals
   later args still read (gcd(b, a%b) lowered as gcd(b, b%b)). Args now
   all evaluate in caller env before any param binds. Pinned by
   graphc/tests/test_calls.py (arg order + recursive gcd/fib shapes).
9. ✅ Lowering-chain guard (measured, not guessed): desc demand-chain
   depths vs sim on Windows 1MB main thread — 129/321/513/641 pass,
   1540 kills the process (STATUS_STACK_OVERFLOW, uncatchable). Guard at
   800 in _assemble (loud + actionable). Consequence: while cap 128 -> 64
   (128 x typical bodies exceed the guard; 64 x 12 = 768 fits). Values
   run green end-to-end: breaksum 6, contsum 3, while 0.78125 + clean
   canary, fib6 8, gcd 6.
   Sim-side principled fix (handed off, not done here): explicit heap
   work-stack in the sim lowerer instead of call-stack recursion.
