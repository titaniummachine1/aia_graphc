# Handoff — next session: titanium strength ladder + compiler fixes

## State (2026-09-13, all pushed)

- `aia_graphc@b655ffd` (master): titanium = two-stage ladder + walk-first/
  sprint-gated selection (STAM_RESERVE 0.50) + shared per-(point,shot)
  evaluator with 2nd-bounce deadline and shot-specific bounce physics.
  Build: **6401 nodes / 14057 transitions / 0 numeric leaks**, deployed as
  `titaniumpy` (Saves dir). Sim: 7-0 vs stock, self-play splits by server.
  Telemetry (`T.mti`/`T.oti`, `AIA_TRACE_CHANNELS=1`): walk-first holds
  (540/540 feasible ticks walked, 0 sprint picks), W2-heavy (strict rings),
  his-tier pinned 4.0 (watch item — likely dead/high ball, fallback graceful).
- `aia_comp-sim@2e671e7` (main), `AIA_tennis@871b74e` (titanium-v35):
  loop probes + `LOOP_SEMANTICS.md` (single-pass-per-tick measured).
- Parked (NOT fixed): literal-dispatch pruning — reverted byte-clean after
  it broke `titanium/entry` compile ("not all paths return in `_mT`").
  Repro = compile titanium. Hypothesis: static-taken `if` arm doesn't drain
  deferred `fn_pend` returns the way the dynamic path does
  (`ast_fe.py` static arm vs `_inline_call:835`).

## Task 1 — strength ladder (sim first, game confirms)

Opponents (all loadable by name in sim `tennis_tournament` and game `modctl`):
styles `pusher/slicer/cross_court/alternator`, `Safe_Corner_v0.3`, `bat`,
`nqvxf22`, `martico2432v7`, `Zudan6`, `Adam`, `Apex`, `LeBlock_James`,
`Unlucky`, `sim_titanium28/31/32`, lineage `titanium45/50/53/54` (54 = champ),
`_Court-Weaver_8a4b6c1584e7` (nemesis). Plus `stock` baseline.
Exclude: `stress_*`, `loop_p*`, `semantics_battery`, `probe_servearea`,
`sim_probe`, `diagbot`, `titanium*.txt` stubs, `titanium_recv`/`titaniumpy`
(ours).

- **Phase A (sim, fast):** write `aia_comp-sim/scripts/run_titanium_ladder.py`
  (batch `tennis_tournament --home titaniumpy --away <opp> --seed <s> --points 8`,
  seeds 7/11/13, JSONL) + `score_titanium_ladder.py` (wins, points, aces/faults,
  ticks/point, `T.mti` tier hist + stamina min via `AIA_TRACE_CHANNELS=1`).
  Bar: sweep styles + ≤titanium50, competitive vs 54/Weaver/Apex.
- **Phase B (game, slow, user slots):** `modctl.py launch --home titaniumpy
  --away <top-3> --seed 7 --points 4` + wait/quit/summary; judge contact
  quality (`T.mti` perfect rate) and drop-shot scoring in timeplots.
- **Nested: STAM_RESERVE 33% vs 50%:** flip const in `titanium/intercept.py`,
  rebuild, rerun ladder subset (styles + Apex + 54). Decide the reserve.

## Task 2 — compiler fixes (graphc)

1. **Literal pruning (P0):** in `_stmt` ast.If static-taken path, drain
   deferred `fn_pend` returns like the dynamic path does (mirror the
   t_ret/f_ret merge). Re-add `test_literal_dispatch_prunes` (removed at
   revert). Verify: full suites + titanium recompiles SMALLER (~4–6k nodes
   expected) with identical sim behavior (mode-parity style check).
   f32 note: prune only literal-vs-literal bounds (ids/tiers/x.5 — exact).
2. **Dormant while-paths (P1, optional):** `_drive_loop` implicit_cond/canary
   params are dead since the ban — remove or keep with note. No behavior.
3. **No bot changes** for compiler work; titanium sources stay frozen except
   the stamina-sweep const.

## Open questions for user

- In-game A/B verdict (contact quality, drops) + 33/50 call after sweep.
- `opp_meet` single-stage approximation: accept, or mirror two-stage?
- His-tier-4.0 watch: investigate if it persists vs live opponents.
