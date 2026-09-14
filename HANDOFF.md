# Handoff — next session: titanium66 polish + game-side verification

## State (2026-09-14, end of session — all committed/pushed)

### THE headline: sim double-bounce award was INVERTED (fixed this session)

`TennisWorld::on_rally_bounce` awarded the double bounce to **`striker.other()`
(the receiver)** — inverted tennis. Every unreturned shot scored for the
opponent; aces were impossible; "titanium54 loses to pusher in-sim" and the
entire 25W-64L ladder era were artifacts of this one line. Raw-trace proof:
our serve bounced IN the box, pusher never touched it, the 2nd bounce landed
at +26.7 — and pusher got the point.

Fix: `resolve_point(striker, DoubleBounce)` — striker wins, 2nd-bounce
location irrelevant ("second bounce can land anywhere, no location fault" —
game-truth note + user's rules). The 1st-bounce-out award (striker faults)
was already correct. 46/46 tennis tests pass; nothing had pinned the
inversion.

**Never compare sim results across this correction boundary** — every
pre-2026-09-14 tennis ladder/AB number is poisoned.

### Second finding: arena-bounds misread (mine, not the sim's)

The in-flight exit check is `|x| > COURT_LENGTH (28)` / `|z| > COURT_DOUBLES_
WIDTH (18)` — FULL court length, not half. So the 2nd bounce almost always
lands before any arena exit, and deep shots are VALID winners (unreturned
deep ball double-bounces the receiver out of court). My interim
"b2-must-stay-inside 13.9/8.9" legality was built on the misread — removed.
What remains legal in `_vscore`: 1st-bounce-out (beyond line + ball-edge
tol 0.169 + 0.25 pad → 14.25/6.25) = fault = score 0. The `ignore-ball`
rule keeps ONLY that case (guaranteed fault); deep balls and serves must be
returned (ignoring them handed stock 14 serve "aces").

### Full ladder result (corrected sim, seed 7, best-of-3, AIA_AIM_MODEL=separate)

**titanium66: 97W-4L vs everyone** (data/tennis/titanium_ladder.jsonl).
Losses: Apex 1-2 (13/31 pts), LeBlock_James 1-2 (15/33), slicer 0-2 (0/14 —
shutout loss, trace first), titanium2 0-2 (8/26).
Everything else 2-0/2-1 incl. Weaver, titanium54, Adam, Safe_Corner, stock.
(Note: 101 rows — includes a few dupes/our-own arms from A/B reruns; the
ladder script is resume-safe on home+away+seed.)

### Titanium build of record: titanium66 (deployed, Saves dir)

- prefer-perfect@25% walk order (walk perfect before walk direct when
  stamina > 25% — user directive, kept)
- comfort interception: ladder targets the ball's PERFECT-ring (1.0 m)
  entry, not the tier-ring entry — park where the ball will be, arrive
  early, release fires on the first perfect tick (late contacts
  74% -> ~50-56%, z_err sd ~0.1 m)
- attack grid: deep (13,±5) + mid (10,±5) + half (7,±5) + recorded
  hot-spot row (3.5,±3.2); near-net 1.0 row dropped (badly placed).
  `_vscore` zero-scores 1st-bounce-out candidates only.
- ignore-ball: ONLY on 1st-bounce-out beyond the 0.25 pad (his fault).
  NO 2nd-bounce ignore (that handed stock 14 aces).
- auto-swing mode = "Normal Only" + serve 0.7 charge gate removed
  (the gate was vestigial — both wire states were true). In-sim this is
  a no-op (mode approximated away); it matters in-game.
- 7909 nodes / ~17.7k transitions (grew from 6402: legality checks + grid;
  acceptable — the win rate tripled).

### Sim fidelity changes (aia_comp-sim, all this session)

1. Double-bounce award fix (above) — THE big one.
2. `TennisAutoSwing` approximation = `Is Ball Playable && !Must Wait`
   (approach-hold, game-measured) in BOTH lower.rs (O1 VM) and eval.rs
   (reference). Mode label ignored by the sim.
3. World release rule ("perfect when possible"): a held swing releases at
   the FIRST PERFECT tick; if the ball's velocity line will never enter
   the perfect radius (3D closest-approach > 1.0 m), strike the moment it
   enters the 2.6 m zone; toss strike exempt. The old `|| cmds[i].swing`
   explicit clause is GONE — the smart rule covers pulses uniformly
   (stock/others still connect; 46/46 tests).
4. Best-of-3 enforcement + `MatchRules` (score.rs): default official rules
   (4/2/2), `--rules file.json` override, loud validation. 2-2 impossible,
   3 sets max. Cross-set serve rotation via `total_games` (never resets —
   after an odd-game set the opener flips; pinned by tests).
5. Per-strike instrumentation: `StrikeEvent` (tier/serving/ball/racket/aim/
   charge), `--trace-strikes <file>` / `AIA_STRIKE_LOG=1`;
   `scripts/archive/strike_join.py` joins strikes to first-bounce landings
   (tier×IN/OUT tables, scoring-shot attribution). `AIA_FIRST_SERVER` pins
   the opener for calibration.

### CRITICAL empirical lesson: AIA_AIM_MODEL=separate

Compiler bots split walk/aim via t.aim(); the sim's legacy aim latch IGNORES
that wire (strike aims fall back to deep-middle 13.44). Every compiler-bot
sim run MUST set `AIA_AIM_MODEL=separate` — baked into
`scripts/run_titanium_ladder.py` now. Without it titanium lost to stock
0-2; with it the aim wire lives.

### Compiler track: `and`/`or` — implemented, proven isolated, LOUD-BLOCKED

- Implemented eager BoolOp fold to CompareBool (same node as
  api.bool_and/or). Desc verified correct; save wiring audited node-by-node.
- ISOLATED probe (or-chain bot vs nested-if bot): 3627 ticks, 0 channel
  diffs — bit-exact.
- FULL titanium context: the or-chain build (62/64) diverged from the
  nested-if build (61/63) — tick-exact 2x2 isolates the or+fall-through
  combination; root cause NOT found (chain probe, save audit, _REF_KEYS
  all clean).
- Per the no-silent-miscompile policy: `and`/`or` raises the loud error
  again (ast_fe.py, full investigation note in place);
  `graphc/tests/test_and_or.py` pins the loud rejection + documents the
  probe recipes. api.bool_and/bool_or remain fully supported.

### Open items (priority order)

0. **slicer 0-2 shutout + titanium2 0-2**: the only structural losses left —
   trace both (slicer's slice skid changes 2nd-bounce geometry; titanium2
   is an old-side bot — check what it exploits).

1. **Verify the GAME's double-bounce award** from existing captures
   (modhost game timeplots / restart_sweep.jsonl) before trusting
   game-vs-sim parity: the sim inversion is fixed, but the sim must match
   the GAME, not "tennis theory". If the game genuinely awards the
   receiver (contradicted by titanium54's champion record), revert.
2. **4 ladder losses** (Apex, LeBlock_James, slicer, titanium2): trace
   with --trace-strikes, classify point endings (all OUT faults seem gone:
   faults/DFs/aces all 0 across the ladder — DoubleBounce reason is not
   recorded as Ace, so serve-ace accounting is a TODO).
3. **Aces counter** never fires — map serve-double-bounce to
   PointReason::Ace or record aces at the box bounce.
4. **`and`/`or` root cause** (isolated bit-exact, full-context divergent).
5. **Depth-2 minimax** (user-approved spec): for the top-2 grid candidates
   compute his intercept of our winning shot (virtual-ball solve from his
   position, walk+stamina tiers) then his most devastating reply from the
   meet point (restricted 4-target × 6-shot `_vscore` scan); pick
   max(our score − his reply). Est. +45% transitions (~10.5k nodes) —
   fits the measured ceiling. Not started.
6. **Game probes P1-P4** (user pre-approved launches): out-tolerance
   (0.17 vs 0.25 pad), tier-precision in-game, manual-swing vs node,
   match attribution.
7. Late contacts ~50% remain (was 74%) — comfort ladder helped; swing
   release microtiming may explain the rest.

### Technique notes (proven this session)

- Tick-exact 2x2 isolation: build A/B variants differing in exactly one
  mechanism, compare match ticks — separates compiler-path vs control-flow
  questions in minutes.
- Strike-log + trace join (`strike_join.py`): tier histograms, contact
  geometry (x/z err vs racket), landing-by-tier, scoring-shot attribution.
- Raw-trace point walking (bounce/point deltas) is the ground truth when
  joins get confusing — the landing-join misses floor touches.
- The ladder JSONL is append+resume-safe (home+away+seed keys).

### Artifacts

- Saves: titanium58..66 + 58perf (experiment arms; 66 = build of record).
- aia_comp-sim data/tennis/: titanium_ladder.jsonl (the 97W-4L record),
  ladder_run.log, traces + strike logs for pusher/stock/Adam/Weaver/54.
- graphc: PROGRESS.md session 22, this handoff.
