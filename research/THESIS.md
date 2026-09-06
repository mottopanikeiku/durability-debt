# Provisional thesis and claim boundaries

## Decision and question

**Conditionally selected for falsification, not established as novel or significant.**

> Can persistence-sensitive joint schedule/crash exploration expose reproducible cross-process recovery failures in unmodified local Linux workflows substantially more efficiently than strong one-trace and composed schedule/crash baselines?

The current executable artifact is a **finite whole-record reference model and oracle**, not a POSIX implementation, syscall supervisor, SQLite tester, ext4 model, or native crash backend. Only the repository's recorded reference run establishes what the implementation actually exercised. Every native capability and reduction theorem below is a research obligation. [PROTOCOL.md](PROTOCOL.md) specifies stop gates; [BASELINES.md](BASELINES.md) defines the strongest nulls; [THREATS.md](THREATS.md) governs interpretation.

The motivating shape is a producer making new input visible before durable, a second actor reading that input and durably publishing a dependent result, and a crash retaining the result but losing the input. A user-visible promise can then fail after recovery. This is not intrinsically a bug: a rebuildable cache, historical log, or allowed stale result may be correct.

## What prior work already owns

- [PerSeVerE, POPL 2021](https://plv.mpi-sws.org/persevere/paper-full.pdf) combines ext4 persistency semantics with concurrent C/C++ execution and model checking. Joint concurrency/persistence exploration is not new. Its [artifact](https://doi.org/10.5281/zenodo.4067991) must be evaluated as a semantic oracle, not dismissed because it is not a drop-in process-tree supervisor.
- [PMRace](https://csyhua.github.io/csyhua/hua-asplos22-PMRace.pdf) and [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf) already target persistent-memory visibility/durability inconsistencies, including visible-but-not-durable patterns. Naming this pattern “durability debt” is terminology, not discovery.
- [ALICE](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-pillai.pdf) already traces applications/subprocesses, constructs crash states, and uses semantic checkers. [Pathfinder](https://arxiv.org/html/2503.01390) already supplies persistence graphs, representative testing, and DPOR within observed traces. [RACEPRO](https://www.cs.columbia.edu/~junfeng/papers/racepro-sosp11.pdf) already reorders/replays multi-process system-call races.
- Generic DPOR, graph representations, complete-support graph bookkeeping, workflow DAGs, and bounded goal/action/observation loops are not contributions of this project. Neither is choosing minimum/maximum persistence prefixes for a monotone predicate.

[INFERENCE] A potentially useful remaining capability is bounded, schedule-changing, recovery-checked exploration of **unmodified mixed-resource process compositions**, with a defensible advantage over composing existing techniques. That is a hypothesis about a narrow gap, not a literature-exhaustiveness or priority claim. Routine integration alone does not satisfy the proposed methods thesis.

## Finite objects: the delivered model's domain

Let `R` be a fixed finite set of pre-existing named records. Each record has an initial value, indexed version 0. There are one or two sequential actors and finite event programs. A run consists of actor-local program counters, visible record values, volatile local read results/handoff state, ordered whole-record write histories, and per-record durable lower bounds.

Supported abstract event roles are whole-record write, read, record flush, and volatile handoff/await. These names describe semantics, not a promise that the executable exposes a general input language. An enabled-event schedule preserves each actor's program order and handoff enabling. Reads observe the latest completed write in that schedule. A write changes visibility atomically. A flush of record `r` raises its durable lower bound through the latest completed version of `r`; it imposes no cross-record transaction. Handoff orders visibility but does not persist anything.

At crash frontier `c`, let `n_r(c)` be the number of completed writes to record `r` and `f_r(c)` its flushed lower bound. An admitted crash chooses independently for every record:

`f_r(c) <= k_r <= n_r(c)`.

The durable image contains version `k_r` of each record; volatile state disappears. Equivalently, the persisted updates form a per-record prefix containing all flushed updates. Distinct prefix choices may produce the same image when values repeat. Count separately: full schedules, crash frontiers, prefix-choice samples, unique images, checker-observable outcomes, and root causes. Deduplication keys must include the checker-relevant promise/history where those affect meaning; bytes alone need not define an equivalent outcome.

Assumptions are explicit: atomic whole-record writes, fixed identity and size, independent persistence prefixes across records, honored record flush, one fail-stop, finite execution, and a declared terminating recovery predicate. There are **no** sectors, byte ranges, namespace operations, partial writes, metadata, journaling, file descriptors, real IPC, mmap, SQLite transactions, or opaque process execution in this model. Its record named “source” or “sink” is not a Linux file or database.

### Schedule bound

Initial research bounds are **two actors and at most two preemptions**. A preemption is switching away from an actor that remains enabled and has a next event; a switch after blocking or termination is not a preemption. Record scheduling granularity and whether crash frontiers include the initial state and every completed event. Any executable using a different convention must report that convention explicitly rather than borrowing this bound. A two-actor abstraction of a many-process workload requires a justified grouping; hiding independently runnable threads inside an actor invalidates the bound.

## Native target objects: not yet implemented

For a supported native trace let `E` be events, `po` actor program order, `sw` supported synchronization, `rf` version/byte-range read-from, and `pb_M` persistence constraints under a named backend/storage model `M`. Resource identity needs inode generation and descriptor provenance, not path strings alone. A persisted set `P` at frontier `c` must be admitted by `M`, including mandatory completed barriers and any namespace/data dependencies. Downward closure under `pb_M` is useful only if that graph has been proved to characterize the model; it is not automatically sufficient for ext4 legality.

A conservative relation `dep` propagates possible dependence from a foreign dirty read to later output and supported IPC recipients. A structural candidate is `(u,r,v,c,P)` where a different actor reads update `u`, `u rf r dep v`, `v` survives, and `u` does not. This is a prioritization signal, not semantic information-flow proof. Old overwritten values and version identities must not be conflated with present resource bytes.

For each workload, a checker contract defines initial state `I`, acknowledged promises/history `H`, permitted recovered observations `Allowed(I,H)`, recovery procedure `Recover`, and observable projection `Obs`. A failure is:

`Obs(Recover(P)) not in Allowed(I,H)`.

A **confirmed native model-relative failure** additionally requires supported trace coverage, an admitted and materialized crash image, repeated replay, and triage excluding a checker/backend error. “Confirmed upstream bug” additionally needs an actual upstream promise, attribution, and confirmation evidence; a deliberately unsafe wrapper is only a composition litmus. Semantic causality is not established merely by process taint or temporal order.

Keep a third relation `requires_O(v,u)` for an application-specific recovery obligation separate from execution `rf` and storage `pb_M`. In particular, **never add `u -> v` to storage persists-before merely because the consumer semantically requires the source**: that would incorrectly forbid the very sink-survives/source-lost image being tested. Conservative `dep` does not establish `requires_O`; only the declared specification and recovery check do.

## Candidate reduction obligation, not an algorithm claim

Proposed research direction: reason jointly about visibility/read-from alternatives and persistence frontiers to avoid enumerating irrelevant schedule/crash products. Before calling it a reduction, specify an effective independence/equivalence relation, its state, exploration/backtracking rules, termination, and the exact preserved property. It must account for changes in enabling, `rf`, flush coverage, allowed crash images, acknowledged promises, and recovery observations. Ordinary visibility commutation is insufficient when swapping operations changes what a flush forces.

The desired bounded theorem is: for every admitted in-bound execution/crash with a violation in a declared checker/property class, exploration retains at least one admitted execution/crash with the same violation class. A stronger equality of outcome sets may be attempted, but cannot be inferred from a small corpus. State any restriction on checkers or dependence; an arbitrary semantic predicate need not be monotone in persistence. Prove both image legality and witness preservation, or label the procedure a heuristic and measure missed witnesses against the complete finite oracle.

Required hostile examples: read moves across producer flush; consumer flush moves across producer flush; successive overwrites of one record; a barrier covering another actor's writes; benign logger; validating cache; non-monotone parity/version check; blocking handoff; a namespace/descriptor identity change in any native extension. Simple extrema pruning succeeds on the delivered monotone order predicates but does not generalize to arbitrary predicates. Generic schedule reduction followed by crash pruning must be implemented first as a serious null. No theorem or new persistence-sensitive algorithm is established by the initial artifact.

Recovery-observer pruning must also survive control-flow changes: observing one recovery run's read set does not prove other images cannot make recovery branch and read new locations. Use a declared complete observation interface, conservatively retain all modeled state, or prove a sound alternative. This obligation is especially important because PerSeVerE already exploits explicit recovery observers; relabeling that optimization is not a contribution.

## Finite-to-native refinement boundary

A future backend must provide an explicit abstraction map from native trace and recovered state to the formal objects, then discharge:

1. **Observation:** no relevant reads/writes, synchronization, barriers, or unsupported access escape tracing; observed reads have justified provenance, including partial/mixed-version reads.
2. **Scheduling:** requested order is feasible and replayed; syscall entry/exit is not assumed to make a whole syscall indivisible on Linux. Blocking, internal threads, asynchronous effects, and read completion require a stated model.
3. **Persistence:** constructed images satisfy the selected byte/metadata/namespace model; backend cache clearing cannot silently be substituted for arbitrary allowed subset materialization.
4. **Recovery:** the real command observes the selected durable image, not stale page cache, a repaired copy, or a live process's buffers; recovery's own writes are recorded separately.
5. **Semantic transport:** native promise/checker meaning corresponds to the modeled property. A record assignment is not a refinement of a SQLite transaction without modeling its actual I/O and recovery.
6. **Refusal:** any unsupported relevant event makes that run unsupported, never safe or complete. Lost events or replay divergence invalidate the witness.

Rootless LazyFS is a candidate controlled substrate, not an ext4 equivalence theorem ([paper](https://www.vldb.org/pvldb/vol17/p3017-ramos.pdf), [source](https://github.com/dsrhaslab/lazyfs)). Native realization is a separate feasibility gate. No finite-model result transfers automatically to Linux, ext4, SQLite, or physical power loss.

## Claim ladder

| Level | Permitted assertion after evidence | Evidence required; present limitation |
|---|---|---|
| C0: question and protocol | A falsifiable conditional research plan exists | These documents; not empirical significance |
| C1: finite sanity | Exact named finite cases exhibit specified allowed/forbidden outcomes | Executed reference output and oracle comparisons; counts only from canonical run |
| C2: bounded mechanism | A precise reduction preserves its stated finite property and improves strong nulls | Proof or explicitly heuristic exhaustive differential evidence; currently unsupported |
| C3: native feasibility | A supported two-process litmus replays under a named controlled backend | Gate 2 native bundles and controls; currently unsupported |
| C4: practical advantage | Matched real workflows show meaningful efficiency/capability advantage | Preregistered baseline comparison, censoring, replay, checker costs; currently unsupported |
| C5: upstream impact | Named real defects violate documented promises and are independently confirmed | Disclosure/maintainer or independent reproduction evidence; currently unsupported |
| C6: publication contribution | Formal and/or systems contribution merits a particular venue | Independent novelty review and full artifact; no acceptance or significance guarantee |

A higher level never follows from the level below by relabeling. In particular, a finite seed-schedule reversal establishes sensitivity of a demonstration to schedule choice, not efficacy against Pathfinder or PerSeVerE. Negative outcomes are first-class: a precise counterexample, composition parity, unsupported native boundary, or absence of incremental real failures can close the project honestly.
