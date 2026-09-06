# Research loop log

Append decisions; do not rewrite earlier gates after seeing results. Each entry binds goal, action, observation and adjustment. A transient branch gets at most one exact rerun and one cause-directed adjustment before stopping. Planned replications are separate preregistered experiments, not an excuse for open-ended rescue attempts.

## L0 — select a defensible new project — 2026-09-05

**Goal:** choose a potentially significant new sole-author research question under CPU-only constraints.

**Action:** six independent deep candidate investigations; two independent hostile challenges; primary-source and license verification. Compare authority, remote recovery, evidence liveness, release-cohort integrity, evaluation recoverability and local crash/concurrency systems. Source/selection records are in `SELECTION.md`, `PRIOR_ART.md`, `SOURCES.json`.

**Observation:** authority/recovery mechanisms have direct overlap; evidence liveness reduces to existing caching/selection/support machinery; generic evaluation provenance/identification is occupied. Wheel-cohort integrity remains an empirical alternative but may collapse to exact comparison. Crash/concurrency has a plausible native capability boundary but severe PerSeVerE/PMRace/DURINN/composition collision risk. The hostile verdict is conditional, near-KILL.

**Adjustment/decision:** launch Durability Debt as a kill-first research question, not as established novelty. Build a complete finite reference/oracle artifact and freeze the stronger continuation gates. Other candidates are not concurrent projects.

## L1 — finite mechanism and controls — 2026-09-05

**Goal:** establish a nominated seed miss, alternate-schedule witness, durability-before-handoff control and semantic false-positive controls under explicit finite semantics.

**Action:** first ran a disposable atomic-record selection script. It exposed the unsafe handoff and eliminated the failure with prior durability. An independent reviewer identified duplicate-count ambiguity and the need for a nominated safe seed and ordinary missing-fsync control. Implemented the canonical reference artifact with separate raw/projected counts, replay, six cases and the elementary extrema null.

**Exact smoke command:** `python3 -m durability_debt probe --output /tmp/durability-debt-launch-20260905`.

**Observation:** all nine gates passed. Unsafe handoff: seed 0 bad observations, joint 1 across 5 schedules. Safe handoff/logger/cache: 0. Single-process missing-flush: already found by seed. Extrema matched existence on every case. No branch failure was suppressed.

**Adjustment/decision:** accept finite mechanism sanity only. Do not promote the simple extrema baseline, duplicate removal or the known unsafe protocol as new science. Product-aware preservation/separation remains the next gate.

## L2 — freeze reproducible launch evidence — 2026-09-05

**Goal:** deliver a replayable, source-bound baseline and protect evidence reuse boundaries.

**Actions:**

```sh
python3 -m unittest discover -s tests -v
python3 -m durability_debt verify /tmp/durability-debt-launch-20260905
python3 -m durability_debt probe --output results/launch
python3 -m durability_debt verify results/launch
cmp results/launch/report.json /tmp/durability-debt-launch-20260905/report.json
```

**Observation:** 12 regression tests passed; both bundle checks passed; report bytes matched. Failure-cap and overwrite/tampering tests exercise refusal instead of misleading successful checkpoints. Canonical manifest binds source, inputs, settings, environment and artifact hashes.

**Adjustment/decision:** retain `results/launch/`; remove disposable smoke artifacts after final verification. Read `NEXT_STEPS.md` and run the product/composition gate. Native FUSE/SQLite experiments, substantive reduction, real-workflow evidence and paper conclusions remain unexecuted.

## L3 — satisfy hostile seed-reversal and control requirements — 2026-09-05

**Goal:** close the explicit Gate 0 gaps identified during protocol integration without weakening its acceptance criteria.

**Action:** added consumer-first seed and reversed joint traversal, emitted complete projected outcome sets, and added old-version/no-sink controls. Preserved the prior six-case evidence at `results/pre-seed-reversal/`; it is historical and intentionally fails current-source checkpoint reuse. No earlier result was overwritten or silently relabeled.

```sh
python3 -m durability_debt probe --output results/launch
python3 -m durability_debt verify results/launch
python3 -m unittest discover -s tests -v
python3 -m durability_debt probe --output /tmp/durability-debt-final-replay-20260905
cmp results/launch/report.json /tmp/durability-debt-final-replay-20260905/report.json
```

**Observation:** all 13 probe gates and 13 regressions passed. Eight cases and five baseline/search-order configurations ran. The bad-seed one-trace baseline finds the motivating failure and receives full credit; joint outcome sets match under reversed traversal. Old-version/no-sink controls have zero violations. Final canonical and fresh replay reports are byte-identical.

**Adjustment/decision:** Gate 0 is satisfied for the declared finite model. This does not change the near-KILL novelty assessment. Gate 1, the strongest-composition/product-preservation investigation, is the next scientific action. Do not build the native backend before that decision.

## L4 — public cross-version verification — 2026-09-05

**Goal:** verify the published artifact on independent CI runtimes and remove a newly observed workflow compatibility warning.

**Action/observation:** initial GitHub run `34002552071` passed all steps on Python 3.11 and 3.14. It warned that the initially pinned checkout/setup-python actions targeted deprecated Node 20 and were being forced onto Node 24.

**Adjustment:** resolved current official releases and pinned checkout v7.0.1 and setup-python v7.0.0 by immutable SHA. Checkout's pinned `action.yml` declares Node 24. This fixes the action runtime rather than suppressing the annotation. The updated workflow must pass before final delivery; its GitHub run is the CI result authority. Model source and canonical finite evidence are unchanged.
