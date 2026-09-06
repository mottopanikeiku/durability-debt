# Threats, refusal rules, and interpretation

**Current evidence boundary:** only an executable finite whole-record model/oracle is delivered. No native Linux/SQLite failure, ext4 fidelity, new reduction theorem, practical speedup, upstream defect, prevalence, or significance is established by that artifact. Read the actual canonical run before repeating finite counts. Planned checks in PROTOCOL are not completed results.

## Threat register and consequences

| Threat | Why it can invalidate a conclusion | Required discriminator/action |
|---|---|---|
| Prior-art collision | [PerSeVerE](https://plv.mpi-sws.org/persevere/paper-full.pdf) already combines concurrency/persistency/DPOR/recovery observation; [PMRace](https://csyhua.github.io/csyhua/hua-asplos22-PMRace.pdf) and [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf) already target the motivating phenomenon | Kill claims of new phenomenon/joint DPOR; compare the product mechanism against actual predecessor semantics and strongest composition |
| Weak baseline | A safe nominated seed or Cartesian enumeration can make a simple search look powerful | Reverse seed, credit bad-seed one-trace success, strengthen B4, equalize costs/coverage; finite extrema is a baseline, not novelty |
| Circular storage model | Adding “source required by sink” to persists-before forbids the intended counterexample | Keep `rf`, storage `pb_M`, and semantic `requires` separate; justify legality without the desired invariant |
| Atomic-record abstraction | Whole records omit torn writes, size, metadata, journaling, namespaces, and actual recovery | Confine every finite claim to records; explicit native refinement gate before any Linux/SQLite statement |
| Native observation gap | Cached reads, mmap, short I/O, offsets, or missed IPC can invalidate provenance/schedules | Supported-event inventory, independent supervisor, trace-loss/divergence refusal; no silent approximation |
| Backend mismatch | A controlled data-cache loss is not all possible ext4 crash images | Name backend/model; preserve actual images and fault acknowledgments; no ext4/physical-frequency claim |
| Checker overreach | Integrity or build equality may not be the user's promised cross-resource semantics | Preregister allowed observations and acknowledgments; validate benign logger/cache and legitimate nondeterminism |
| Checker underreach | Structural integrity can pass while a source/derived-state promise fails | Separate structural and semantic predicates; explicit version/digest or allowed-history checks |
| Conservative taint | An unrelated write after a dirty read can look dependent | Candidate-only label until semantic rejection and triage; report checker cost and false candidates |
| Unsound pruning | Recovery may branch, inspect new resources, or be non-monotone in persisted updates | Full declared observation set or sound conservative treatment; finite differential counterexamples; no min/max extrapolation |
| Replay disturbance | Instrumentation changes timing/cache, and controller adds ordering | Preserve feasible actual trace and topology, report divergence, compare normal overhead, native mapping proof |
| Corpus/selection bias | Convenience workflows and post-hoc cherry-picking cannot support prevalence | Freeze six-class then twenty-workflow roster; publish exclusions and all null/censored rows |
| Misattribution | A deliberately unsafe wrapper is not a bug in SQLite, Git, or LevelDB | Separate planted model, planted native litmus, real composition failure, upstream-confirmed defect |
| Practical null | Durability-before-handoff/immutable epochs may fix all real cases cheaply | Run B6 and include adoption cost; do not rescue weak impact with benchmark counts |
| Sole-author/host dependence | One environment and correlated workflows do not establish generality | Report exact host/bounds; seek independent reproduction, label unavailable confirmation honestly |

## Native supported-event contract: planned, fail closed

Each backend revision must publish an allowlist defining semantics, observation method, scheduling point, provenance rule, storage rule, and recovery rule for every event it admits. The initial finite model admits no actual syscall at all. A future native allowlist starts narrowly; any broader vocabulary in planning is a proof obligation, not automatic coverage.

Reject a run as `unsupported` before counting a semantic verdict if a relevant operation cannot be modeled, observed, controlled where required, or safely materialized. Where the operation is discoverable only after execution, stop/contain that branch and invalidate all completeness claims for it. A preflight refusal is preferable to attempting the fault. Unrelated read-only loader files may be outside the modeled mount only under a hashed immutable runtime/input policy; external writable descriptors or mutable inputs must be explicitly modeled or rejected.

Required refusal cases until individually implemented and validated:

- shared writable mappings and unobserved mapped reads affecting decisions, `msync`, shared memory/futex communication, unsupervised threads/processes, inherited external writable descriptors;
- direct I/O, DAX/persistent-memory accesses, `io_uring`, asynchronous I/O, raw/block/device access, network I/O, network filesystems, multiple persistence domains/mounts;
- namespace or metadata changes unsupported by the selected crash backend, hard-link/inode-reuse ambiguity, unknown descriptor provenance, shared-offset operations without open-file-description modeling;
- short/mixed-version reads or writes, overlapping ranges, append/truncate, errors, signals or negative lookups if the current event semantics omit them; do not replace a failed or partial operation with success;
- mount/symlink/path escape, daemonization beyond containment, unexpected executable, trace loss, unrecognized event, unresolved event/request correlation, replay divergence, crash-ack timeout, or stale cache at recovery.

A refused workload is not safe, buggy, or evidence of complete exploration. Report numerator/denominator of qualifying, attempted, unsupported, timed-out, and completed workloads. Excluding a failing target after inspecting its outcome requires a public protocol change and preserves the old row.

### FUSE and LazyFS limits

[Linux FUSE I/O documentation](https://docs.kernel.org/filesystems/fuse/fuse-io.html) distinguishes direct I/O, cached write-through, and writeback-cache modes. Reads may be served from kernel cache; one syscall may generate multiple requests; background writes may arrive later. Thus a FUSE request gate is not a syscall scheduler or exact application read-from oracle. Record mode and prove the supported mapping rather than change it opportunistically for a desired result. A separate process/lifecycle/IPC supervisor is required. Blocking and cancellation also require containment ([FUSE overview](https://docs.kernel.org/filesystems/fuse/fuse.html)).

[LazyFS's paper](https://www.vldb.org/pvldb/vol17/p3017-ramos.pdf) describes controlled data-loss/torn-data injection and a data cache; metadata durability injection is not its established coverage. Neither clearing its cache nor observing a file flush proves arbitrary legal-image realization. SQLite journal create/delete/rename and directory persistence must be separately justified. A restricted experiment may hold metadata behavior fixed and prove only a controlled data-loss scenario, but must say so. This is weaker than an ext4 result, not an ext4 emulation. [Linux fsync documentation](https://man7.org/linux/man-pages/man2/fsync.2.html) explicitly distinguishes file flushing from directory-entry durability.

SQLite `mmap_size=0` is not a blanket guarantee that WAL shared-memory coordination vanishes. Consult [WAL documentation](https://sqlite.org/wal.html) and actual traces; support or refuse relevant shm behavior. Keep rollback/WAL, synchronous settings, VFS/device assumptions and recovery files explicit. SQLite's [atomic-commit contract](https://sqlite.org/atomiccommit.html) protects database transactions under stated assumptions, not arbitrary sibling files. An internally healthy database containing a stale external digest is not evidence that SQLite broke its transaction contract.

## Semantic checker contract

Before fault outcomes are viewed, every workload must state:

1. **Promise source:** exact documentation/test/maintainer contract or explicit composition specification and its author. “I would prefer these files to agree” is not an upstream promise.
2. **Initial state and history:** allowed inputs, starting durable image, completed/acknowledged operations, success marker and its timing. No-crash output is not automatically a promise of power-loss durability.
3. **Allowed recovery:** set of permitted observations, including old/new/no-publication, recoverable absence, stale caches, rollback and benign nondeterminism. Do not impose serializability unless promised.
4. **Recovery and observation:** exact executable/argv/env, files read/written, timeout, structural checker, semantic projection and normalization. Recovery gets its normal documented chance to rebuild/reject state before checking the final contract; do not manually repair it first.
5. **Verdict schema:** pass, semantic violation, unsupported, divergence, timeout, infrastructure error. Distinguish inability to open due to harness damage from contract rejection.
6. **Calibration:** known valid initial/recovered states pass, a deliberately constructed contract violation fails, no-crash paths pass, and logger/cache controls pass. A planted calibration failure is not a discovered real defect.
7. **Cost/provenance:** checker source/hash/license, reused oracle source, bespoke nonblank lines, authoring/triage hours, and reasons for each assertion. Freeze before search; apply any necessary correction identically to every method and rerun affected comparisons.

`PRAGMA integrity_check` alone is insufficient for source/row correspondence; clean-build byte equality alone is too strong for timestamps, random IDs, or permitted nondeterministic outputs. Normalize only fields justified by the contract, with normalization fixed in advance. A runtime log of pre-crash reads may establish which input B saw but does not itself establish a requirement that the input remain recoverable.

### Conservative taint versus confirmed failure

Keep statuses distinct:

- **Candidate:** a possibly dirty read can precede a possibly dependent durable effect. Whole-actor taint is intentionally imprecise.
- **Checker rejection:** declared recovery observation is outside allowed set, but image legality, checker error, and replay remain under investigation.
- **Confirmed model-relative composition failure:** admitted supported image, actual recovery rejection, >=9/10 recorded clean-image replays, minimized explanation and control agreement; scope is the exact backend/model.
- **Confirmed upstream defect:** additionally a violated upstream contract and attributable evidence, with maintainer acknowledgment or independent confirmation reported precisely. Pending/unconfirmed reports are never promoted by silence.

Do not clear taint merely on a flush if the relevant version/obligation was overwritten or its dependencies remain unresolved. Conversely, taint is not an unconditional semantic obligation. Logger control permits an independent durable record after a dirty read. Cache control permits sink-survives/source-lost when recovery validates the digest and invalidates or rebuilds stale output. Both must yield zero semantic false positives even if selected as candidates. Report candidate count and triage cost rather than suppressing these controls to improve apparent precision.

## Resources, containment, and stop behavior

No paid API/model/GPU work, new spending, privileged service, custom kernel, physical crash, device fault, real user data, credentials, remote side effect, or unrelated repository mutation is authorized. Native tests run only in a new disposable dedicated root with verified ownership/path boundaries and immutable baseline. Acquire public dependencies separately, inspect/pin licenses and executable inputs, then run offline. Never fault-inject the canonical repository or host filesystem.

Use process containment available without changing host policy; kill only verified supervised descendants. Set hard wall/CPU/memory/disk/output limits from PROTOCOL. Maintain a watchdog for blocked supervisor/FUSE requests. If existing containment cannot prevent escape, refuse native execution. Do not use broad process-name killing. Leave no persistent mounts/services after a run; teardown may operate only on resources identified in that run's manifest. Preserve failure evidence outside the injected storage before deleting only its disposable workspace.

Missing `fuse3` headers or rootless mount permission is a recorded environment blocker. Do not sudo, modify `/etc/fuse.conf`, enable `allow_other`, relax ptrace/SELinux, install a kernel, or treat environment constraints as authorization. An already available user-space dependency build may be evaluated only within the stated safety/resource envelope and pinned terms; it does not authorize changing security settings. If native execution remains unavailable, finish finite work and preserve a candid blocked native gate.

One exact transient rerun and one cause-directed adjustment are the maximum recovery loop for a failing branch. Soundness/safety errors immediately invalidate downstream findings. A budget expiry is incomplete, not “no failure.” A method that requires more actors/preemptions or undocumented effects than the registered bound is a proposed extension, not an in-bound success.

## Responsible disclosure and public artifacts

For a potential real defect, first separate backend/model/checker fault from a target promise violation. Minimize within a disposable environment, record exact upstream version, documented promise, model and replay evidence, likely impact, controls, and any mitigation. Do not label a litmus or an unsafe wrapper a vulnerability in its dependencies.

Use the project's published security contact/policy for potentially security-sensitive findings; otherwise use the maintainer's normal private reporting route where available. Do not publish an exploit, private data, or sensitive reproducer in a public run bundle while coordination is pending. Retain a redacted public status and a restricted witness; seek human authorization before external disclosure/publication actions. A proposed default is a coordinated 90-day review window with maintainer-agreed extensions or earlier safe release, not a binding promise or automatic publication deadline. If no contact exists, document attempted channels and obtain a human decision. Severity, CVE assignment, acknowledgment, and fix status require actual evidence.

After safe disclosure, publish exact environment/pins, reproduction/control commands, legal-image justification, root-cause analysis, affected/fixed revisions where confirmed, and limitations. Preserve unconfirmed and rejected findings honestly. Do not fabricate maintainer endorsement or count multiple crash frontiers as multiple bugs. Third-party artifact redistribution must follow pinned licenses; public GitHub access alone grants no assumed reuse rights.

## Publication and negative results

Novelty review is adversarial, not a search-absence certificate. Recheck nearby work before submission and state the closest composition prominently. Generic graph management, complete-support bookkeeping, DPOR, visible-before-durable, and extrema selection are not new methods. No mechanism-sanity result supports a journal-level efficacy claim.

Useful negative outputs include exact finite counterexamples to an independence rule, equality with the strongest composition, the condition under which simple extrema works and fails, a reproducible unsupported-native boundary, failed checker portability, no incremental findings in the frozen corpus, and prevention dominating exploration. Release these as accurately scoped artifacts/technical reports where licenses/disclosure permit; journal suitability depends on actual insight, evidence, scope, and independent review. Do not manufacture a positive story or broaden the problem after a kill gate.

The sole human author is mottopanikeiku (alp). Do not invent agent/bot coauthors or contributors. Retain source/dependency attribution and comply with applicable venue assistance-disclosure rules. MIT project licensing does not erase third-party terms. A submission or repository publication is not acceptance, priority, significance, independent confirmation, or proof of correctness.
