# Claim ledger

Status date: 2026-09-05. Evidence authority: `results/launch/inputs.json`, `report.json`, `manifest.json`; code source hashes are bound in that manifest. The repository commit containing the bundle is the publication unit; source hashes avoid a self-referential commit field.

## Established in the delivered finite artifact

| Claim | Evidence | Boundary |
|---|---|---|
| The nominated safe seed hides the unsafe-handoff failure; alternate scheduling exposes it. | `publish_before_flush`: seed has 0 violating observations; bounded joint search has 1, across 5 complete schedules. | Known phenomenon, authored model, two preemptions; not a new real bug. |
| Durability before publication removes this modeled failure. | `flush_before_publish`: 1 schedule, 0 violating observations. | Per-record flush semantics, not directory or SQLite guarantees. |
| A dirty read need not imply a recovery violation. | Independent logger and self-validating cache both have 0 violating observations. | Explicit declared recovery policies, not measured production systems. |
| Ordinary missing-flush loss is already found by one-trace crash enumeration. | Single-process control: seed and joint both find a violating observation. | Must not be credited as joint-search novelty. |
| Elementary extrema matches failure existence on all eight controls. | Thirteen probe gates pass; extrema retains existence while evaluating fewer images. | Strong known null; no novel reduction or full-observation guarantee. |
| Saved witnesses replay in the finite interpreter. | Every emitted first witness is checked by `replay_witness`; regressions reject tampering. | Not native replay rate. |
| Probe report is deterministic on the launch environment. | Canonical and final fresh replay `report.json` compared byte-identical with `cmp`. | Two runs, same source/inputs/host; no cross-host claim. |
| Model/evidence boundary regressions pass. | `python3 -m unittest discover -s tests -v`: 13 tests passed. | Specific contract tests, not a native workload evaluation. |
| Seed reversal does not manufacture superiority. | Consumer-first one-trace baseline finds the failure; joint outcome sets are identical under both search orders. | Credit baseline success; no universal advantage over one-trace search. |
| Old-version consumption and no sink are valid controls. | Both have 0 violating observations. | Declared monotone version contract, not universal application correctness. |

### Canonical joint-search measurements

| Case | Complete schedules | Repeated Cartesian crash evaluations | Unique projected observations | Unique violating observations | Extrema evaluations |
|---|---:|---:|---:|---:|---:|
| publish_before_flush | 5 | 34 | 4 | 1 | 22 |
| flush_before_publish | 1 | 10 | 3 | 0 | 8 |
| old_version_consumer | 4 | 29 | 2 | 0 | 19 |
| no_relevant_sink | 3 | 15 | 2 | 0 | 11 |
| independent_logger | 5 | 34 | 1 | 0 | 22 |
| self_validating_cache | 5 | 34 | 4 | 0 | 22 |
| single_process_missing_flush | 1 | 9 | 4 | 1 | 4 |
| independent_noise | 9 | 193 | 4 | 1 | 42 |

The noise savings are not a research result: the elementary comparator already exploits this model's separable integer claims. Raw duplicate counts are not unique failures. No timing or speedup claim is made from this tiny experiment.

## Open, load-bearing claims

- A product-aware reduction distinct from conventional POR, observer pruning and independent crash enumeration exists and has a bounded preservation argument.
- That method provides an advantage over the strongest composition, not just the seed or Cartesian straw baseline.
- A restricted native supervisor faithfully realizes supported schedules and admitted crash images without source changes or a custom kernel.
- Unmodified realistic workflows contain consequential failures beyond ordinary single-trace missing-fsync bugs.
- A valid semantic checker and reproducible witness can be obtained at acceptable cost.
- Benefits survive matched budgets, conservative taint, conventional prevention and independent confirmation.

None is established. The independent novelty verdict is **conditional, near-KILL**. The next action is the product/composition gate, not a large native implementation or paper claiming success.

## Rejected or forbidden claims

No invention of visible-before-durable races, generic DPOR, persistence graphs, process tracing, Graph/Loop Engineering, or complete-support caching. No ext4/SQLite correctness result, physical crash experiment, prevalence estimate, production vulnerability, general POSIX coverage, machine-checked proof, authenticated manifest, or guaranteed significant thesis.
