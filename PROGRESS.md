# PROGRESS — graphc (2026-09-10, session 2 end)

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
prints it; CI fails on regressions. Current: soccer demo 83, tennis demo 33.
