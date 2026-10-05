# Executable finite reference contract

This document specifies the implemented artifact, not the future native tester. `durability_debt/model.py`, `explore.py`, and `cases.py` are authoritative executable definitions. The research protocol has a larger **planned** scope; do not infer coverage from that plan.

## State and transitions

A program declares one or two finite actors, existing integer-valued records, and recovery claims. Each actor has a program counter and private registers. A state contains:

- each record's complete atomic write history, including its initial value;
- each record's forced-persistence prefix index;
- actor program counters and private registers;
- volatile named handoff signals.

`write(record, integer)` appends a visible atomic version. `read(record, register)` reads its latest visible version. `copy(record, register)` appends the actor-local observed integer. `flush(record)` forces all versions through that record's current latest index. `signal(name)` enables waiting actors; `wait(name)` cannot execute before the signal. A signal is not a persistence barrier. Program construction rejects unknown operations and undefined register copies.

There is no clock, randomness, metadata, byte range, syscall failure, background actor, filesystem, database transaction, or native binary in this model. In particular, a record named `manifest` is not a simulated SQLite database.

## Crash images

At every visited instruction-boundary prefix, including the initial and terminal prefixes, independently choose each record's persisted history index between its forced index and latest index, inclusive. The selected value survives; all volatile state disappears. This is the union of allowed per-record prefix outcomes, not a model of how frequently a storage device chooses them.

A successful flush forbids rollback before its forced index but does not force a later write. Intermediate versions remain eligible; considering only the initial and latest values would be wrong. Atomic whole-record writes and independent record histories exclude torn writes and cross-record storage-order constraints. New names, rename, unlink, directory fsync, mmap and SQLite internals require different semantics, not additional labels on these records.

## Recovery contract

A `Claim(source, dependent)` requires `dependent <= source` after recovery. This models a consumer that must never advertise a future source version; an older derived value is permitted. It does not impose byte equality on every cache or claim every stale output is a bug.

A claim with `discard_invalid=True` discards a dependent value that refers to a future source, representing a declared self-validating cache policy. It is an executable abstract recovery rule, not a tested production cache implementation. An independent logger has no cross-resource claim. Empty claims mean the declared checker imposes no cross-resource obligations—not that arbitrary logging is universally safe.

Recovery observations project onto records named by claims. Independent noise is excluded from this projection but remains in raw crash-image counts. The report separately counts traversal prefixes, repeated crash evaluations, unique raw images, unique projected recovery observations, and unique violating observations. Different traces producing the same projected bad state are not different bugs.

## Scheduling and bounds

The default search allows two preemptions. A switch away from an actor that remains enabled counts as a preemption; switching after blocking or termination does not. The explorer visits every feasible prefix inside that bound. It does not claim all unbounded schedules. Resource caps raise `ExplorationLimit`; they never return a completed exhaustive result. A blocked unfinished program is reported as a deadlock, not a completed schedule.

The producer-first seed chooses the lowest-numbered enabled actor; consumer-first reverses that priority. For `publish_before_flush`, producer-first lets the producer finish its flush before the consumer proceeds. Its one-trace crash enumeration is safe; consumer-first exposes the known failure and receives full baseline credit. Joint search runs with both priorities and compares complete projected outcome sets, not just counts. The comparison shows schedule sensitivity, not algorithmic novelty.

## Strong elementary extrema baseline

For one claim `dependent <= source`, let the eligible persisted values at a prefix be independent finite sets D and S. A violation exists exactly when:

`max(D) > min(S)`.

Necessity follows because every d <= max(D) and every s >= min(S). Sufficiency follows because the two extrema are jointly selectable under independent record persistence. For a conjunction of claims, a violation exists if one claim has such a pair. The implementation constructs one extremal candidate per claim. Discardable invalid caches cannot create a violation under their declared recovery rule.

This is an elementary monotonicity/existence argument, **not a new research theorem or the proposed product-aware reduction**. Extrema may omit valid observations and other bad observations; its guarantee is existential detection for this precise claim language, not full observation preservation. It cannot be generalized to arbitrary recovery programs, nonmonotone predicates, coupled persistence, or a real filesystem. The test with an intermediate source value guards against an incorrect endpoint-only shortcut.

## Witness and checkpoint contract

A witness records feasible actor choices, persisted prefix indices, disk/recovered values, violated claims and preemption count. Replay re-executes the actor choices and verifies the persistence constraints and claimed outcome. It is replay of the finite interpreter, not native process replay.

`probe` exclusively creates a fresh run directory. `inputs.json` binds all programs and settings. `manifest.json` binds source hashes, Python/platform, artifact hashes and completion status. Failed runs retain a failure manifest. `verify` rejects changed code, inputs/settings, environment, incomplete runs or artifact corruption. These are unsigned integrity/reuse checks, not authenticated provenance or a hostile-writer security boundary. Historical bundles remain readable on another environment; a new local run is needed for reusable evidence there.
