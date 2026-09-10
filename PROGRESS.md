# PROGRESS — graphc (2026-09-10, session end)

## What exists NOW

- **Rust backend** (`src/lib.rs`, bin `src/bin/graphc_rs.rs`) — COMPILCLEAN
  (`cargo check` green). Description IR (graphc-desc-v1) → array expansion
  (pack 3 cells/Vector3 var, same-vector write MERGE into one RMW) →
  version-pinned port tables → game save JSON (lean nodes + connections,
  uuid sids). Cost report: nodes + connections = per-tick transitions.
- **Description IR** (`graphc/desc.py`) — tracing frontend emits it:
  const/var_get/var_set/bin/not/select/array + array ops + soccer_move.
- **AST frontend** (`graphc/ast_fe.py`) — Martico's suggestion ADOPTED:
  parse plain Python with the built-in `ast` module, walk to the SAME IR.
  Real `if/else` support (SSA phi-merge of assigned names via select).
  api surface: var/set_var/array/arr_set/arr_get/arr_get_dyn/move.
  One bug found+fixed (api.var parses as ast.Attribute, not Name).
- **Old tracing frontend** (`graphc/core.py`) still present — superseded by
  the AST frontend for authoring; kept as reference.
- **Sim CI**: `aia_comp-sim` test
  `graph_vm::runtime_brain::tests::graphc_poc_demo_replays` replays the
  compiled demo bot. It currently points at
  `examples/graphc_demo_soccer.txt` (last emitted by the OLD tracing path)
  and passes (`f02fd82`).

## Where the pipeline stopped (exact point)

`examples/demo_ast.py` — end-to-end: AST → description → graphc-rs → save.
- `compile_source(BOT_SOURCE, ("soccer","v0.12"))` failed once on the
  api.var Attribute bug → FIXED in ast_fe.py, **e2e run NOT yet retried**.
- graphc-rs binary not yet built in release (build happens automatically
  in demo_ast.build() if missing).

## Next-session first moves (compiler)

1. `PYTHONPATH=C:\gitProjects\aia_graphc python examples\demo_ast.py`
   → expect `graphc_demo.desc.json` + `graphc_demo_soccer.txt` + a report
   line (nodes/connections/transitions). Fix any AST-frontend surprises.
2. Re-run the sim CI: `cargo test --lib graphc_poc_demo_replays` in
   `aia_comp-sim`. The Rust-emitted save must replay identically. UPDATE
   the assertions: the demo's flag is now `+1.0` while cnt<=12 (select
   merged from if without else), so x cycle = [9.5, 10.5, 11.5]
   (val 7.5/8.5/9.5 + 1.0), y = i+2 (same-tick store semantics, pinned).
3. Commit; then delete `graphc/core.py` (old tracing path) if unused.
4. **Tennis v0.14 target**: extend description ops + backend port tables
   with `TennisController` (Vector31/Bool1/Float1/Bool2) and the sensor
   surface from `aia_comp-sim\src\tennis\api.rs` (v0.14 labels). Target
   tuple ("tennis", "v0.14") must gate which api.* helpers exist.
5. Then the payoff experiment: compile a serve-latching bot with the
   compiler and compare against the serve blocker diagnosis (sim handoff
   §4B) — the compiler's latched-serve-aim is exactly the missing sim
   semantics.

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
- `CompareFloats` modifier = comparison operator string ("==","<",...).

## User's optimization directive (binding)

Compile-time target = **per-tick node transitions**, NOT code size or
FLOPs — every block traversal is C# overhead paid every tick. The report
prints it; CI fails on regressions.
