# Strong baselines and comparison contract

**Status:** a design/preregistration, not a report that external tools have run. The delivered finite reference explorers are model analogues only. An “ALICE-style” loop is not an execution of ALICE; a “PerSeVerE-like” rule is not an independent semantic oracle. Results must distinguish native tool runs, faithful ports, simplified analogues, and unavailable comparisons.

## Baseline matrix

| ID | Required configuration | What it controls | Status/limitation |
|---|---|---|---|
| B0 | Bounded Cartesian: every feasible in-bound schedule, every completed-event crash frontier, every legal persistence choice; semantic recovery for each distinct checker input | Reference outcome language and completeness inside the bound | Finite oracle can implement this; not native completeness |
| B1 | One-trace exhaustive crash exploration on each separately nominated seed | Whether changed execution order adds anything beyond crash choice | Use both producer-first and consumer-first seeds; do not cherry-pick the safe trace |
| B2 | Actual Pathfinder and ALICE where feasible, with published recommended pruning and strongest supported checker | Strong existing application crash exploration | [Pathfinder paper](https://arxiv.org/html/2503.01390), [artifact](https://github.com/efeslab/Pathfinder); [ALICE paper](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-pillai.pdf), [artifact](https://github.com/madthanu/alice). Unsupported tool/model intersections must be stated |
| B3 | Fixed-seed random enabled-actor scheduling plus random legal crash frontier/image; restart from identical image each attempt | Cheap unguided discovery | Uniform actor choices are not uniform schedules; record exact distribution and seeds |
| B4 | Generic resource/conflict schedule reduction **composed with** strong per-trace crash pruning and cross-trace exact checker-input deduplication | The strongest boring integration | RACEPRO-style scheduling plus ALICE/Pathfinder crash exploration; no artificial prohibition on standard caching or read-from tracking |
| B5 | PerSeVerE translated finite C litmuses, explicit recovery observer, selected model and compiler/runtime pins | Independent semantics and the nearest joint exploration predecessor | [Full paper](https://plv.mpi-sws.org/persevere/paper-full.pdf), [evaluated artifact](https://doi.org/10.5281/zenodo.4067991). Translation must state differences from whole-record model |
| B6 | Producer flush-before-handoff and immutable-epoch publication | Whether ordinary prevention makes the research case unnecessary | A modified protocol comparator, never counted as an unmodified target |

B4 is indispensable. Beating B0 by 10x while tying B4 does **not** satisfy the methods thesis. B4's schedule relation must preserve crash-relevant outcomes; calling barriers on separate files independent solely because they commute in volatile state is not a fair baseline. If its relation is deliberately conservative, disclose it and strengthen it before claiming advantage. Include a recovery-observer pruning variant inspired by B5; ignoring locations a declared observer cannot read is not a new reduction.

### Precisely constructing B4

1. Use the same native supervisor, event vocabulary, scheduling granularity, two-actor/two-preemption bound, initial images, recovery commands, and checker as the candidate.
2. Enumerate feasible resource-conflict schedules using conventional POR/backtracking; preserve read-from, IPC/lifecycle, descriptor/offset, and flush-coverage dependencies required by the selected model. If no licensed reusable scheduler is available, implement the stated bounded algorithm and label it an analogue rather than “RACEPRO results.” [RACEPRO](https://www.cs.columbia.edu/~junfeng/papers/racepro-sosp11.pdf) is the conceptual scheduling predecessor, not an automatically portable dependency.
3. For each realized trace, independently derive model-legal crash states with ALICE/Pathfinder-style persistence constraints. Use exact canonical image/checker-input deduplication and standard per-trace pruning. Also run the strongest practical representative heuristic as an explicitly incomplete variant where supported.
4. Restart and check all retained cases through the same backend. Account for tracing, scheduling, graph construction, image materialization, recovery, checking, and minimization costs.
5. Share implementation of model legality and checker interfaces, not candidate-specific search priorities. Fix all baseline errors before accepting speed claims.

The distinguishing candidate would reduce across the schedule/crash product in a way this composition cannot, while retaining the stated violation class. Dual graphs, an antichain representation of persistence ideals, dirty-read priorities, or generic DPOR do not by themselves establish that distinction.

## Seed reversal and attribution

Before any crash search, freeze two schedules for the source/sink litmus:

- **S-good:** producer writes, completes its flush, then consumer performs the relevant read and publication (respecting actual program order/handoff).
- **S-bad:** producer's new version becomes visible and is handed off; consumer reads/publishes before producer's flush.

Run complete one-trace crash exploration on **both**, then run alternate-schedule search starting from each. In the finite model, the expected discriminating pattern is no source-old/sink-new violation from S-good and an admitted violation from S-bad. This is an expectation until recorded by the executable. Show the initial seed's recovery-outcome set, union across explored schedules, and incremental bad outcomes. If a baseline starts with S-bad, credit it fully for finding the failure. Report sensitivity across seeds rather than announcing a fixed superiority ratio from S-good alone.

Credit a schedule-conditioned result only if identical inputs and checker admit the alternate feasible trace, the changed read-from/handoff window is in the witness, the seed's exhaustive crash set lacks that failure, and delaying/removing the consumer removes it. A missing flush already exposed in a single trace is conventional crash inconsistency, even when two processes happen to exist. Planted wrappers are never real upstream failures.

## PerSeVerE semantic comparison

Acquire the exact archived artifact, hashes, license terms, toolchain, and documented example invocation before running. Translate a minimal subset of litmuses with an explicit recovery observer and fixed event bounds. Compare **allowed recovered observations**, not internal trace counts or execution speeds across different language levels. State initialization, write atomicity, flush model, and observation correspondence; the whole-record prefix model is not ext4, so equal languages cannot simply be assumed. A difference is first a model/translation investigation, not evidence that PerSeVerE missed a bug.

Independent translated cases should include unsafe/safe handoff, overwrite/read-from changes, interleaved barriers, no relevant sink, logger, cache recovery, and a non-monotone recovery predicate. Native namespace and shared-offset litmuses belong only to extensions that actually model those operations. Failure to run the external artifact is an unavailable baseline, not a passing prior-art gate. Preserve the reason and do not advertise a completed comparison.

## Prevention comparator B6

For fixed existing-record litmuses, flush the source before volatile handoff. For a future native composition:

1. All writers and consumers honor a common lock or otherwise obtain a stable immutable input snapshot.
2. Write a temporary source, flush it, rename into place, flush its parent directory, then publish/release. A file flush does not automatically make its directory entry durable ([Linux fsync documentation](https://man7.org/linux/man-pages/man2/fsync.2.html)).
3. Build derived outputs/database in an immutable epoch; record input digests. Use the database's documented durability settings, not an invented cross-resource transaction ([SQLite atomic commit](https://sqlite.org/atomiccommit.html), [WAL](https://sqlite.org/wal.html)).
4. Flush all required epoch data and namespace state; publish one manifest/pointer with a documented write/flush/rename/directory-flush protocol. Recovery uses only a valid published epoch, verifies digests, and discards incomplete unreferenced epochs.

This is an explicit prevention design to validate under the selected model, not a claimed universal POSIX transaction. Include the latency/throughput, extra bytes, adapter changes, operational assumptions, and recovery cost. If it removes every confirmed pilot failure with <=10% median end-to-end overhead, <=50 changed nonblank lines per workflow, and no change in required user-visible semantics, the significance case is weakened: stop the flagship claim unless the tester demonstrates a distinct diagnosis benefit in a preregistered comparison. These thresholds measure adoptability, not a law that 11% overhead is unacceptable. Transactional predecessors further constrain novelty: [TxFS](https://www.usenix.org/system/files/conference/atc18/atc18-hu.pdf), [TxOS](https://www.sigops.org/s/conferences/sosp/2009/papers/porter-sosp09.pdf), and [Valor](https://www.usenix.org/legacy/event/fast09/tech/full_papers/spillane/spillane.pdf).

## Fair measurement and reporting

- Same subject commit/configuration, input hashes, success promise, allowed outcomes, model, fault opportunities, resource caps, and native backend for candidate and matched baselines. Publish any intersection-only subset and excluded rows.
- For random and search-order experiments use seeds 0–19, fixed before runs. Deterministic exhaustive runs need one complete execution plus replay verification, not 20 identical timings as pseudo-independent samples. Randomize matched method execution order using a separately saved seed.
- Report time-to-first **root cause**, time-to-first witness, total CPU/wall time, schedules, frontiers, legal images, duplicate images avoided, checker executions, and outcome coverage. Separate search from checker/native reset overhead, but include both in end-to-end claims.
- Hash canonical checker inputs using durable image plus relevant acknowledged history/model/checker version. Keep prefix samples separate from unique images. Root causes are manually justified equivalence classes with linked minimized witnesses, not hashes or number of crash points.
- Record median and range across seeds; use paired per-workflow ratios only where both complete or discover the same event. Report timeouts as right-censored with successes/attempts and cap; never impute a timeout as an observed discovery time or drop the losing row. Report coverage alongside speed so a fast incomplete search cannot masquerade as a reduction.
- A zero-failure workload has no finite time-to-first ratio. Report executed budget, supported coverage, outcome equality where exhaustive, and negative controls instead. Do not divide by zero or turn “no bugs observed” into “safe.”
- Report candidate-to-semantic-failure precision, unsupported-run rate, replay rate, checker authoring/triage person-hours, checker nonblank lines, and supervision overhead. Exact taint accuracy is not observable without a stronger semantic oracle.
- Minimal ablations: candidate without product coupling; without dirty-read prioritization; with declared full recovery observation instead of any observer pruning. False-negative mutations are validation experiments, not efficacy baselines. Path-string identity is an intentionally wrong model once rename is supported, not a respectable weak baseline.

All performance and superiority claims remain unsupported until the corresponding matched runs exist. No currently documented finite count is evidence of native execution speed, real failure prevalence, or algorithmic novelty.
