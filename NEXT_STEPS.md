# Successor handoff

## Decision first

**The launch baseline is complete. The thesis is unproven and near-KILL on novelty.** Your next scientific task is **G2 / Protocol Gate 1**, not native implementation, another literature-only brainstorming cycle, or a positive paper. Decide whether a substantive product-aware reduction survives the strongest composition and PerSeVerE. A justified negative is completion, not failure to please the project owner.

Canonical checkout: `/home/alp/Projects/github/durability-debt`. Remote: `https://github.com/mottopanikeiku/durability-debt`, public `main`, MIT. Sole human author/commit identity: `mottopanikeiku <176798723+mottopanikeiku@users.noreply.github.com>`. No coauthor trailers. Preserve meaningful increments and push them; never inflate history.

## Bootstrap without chat history

Read in order: `AGENTS.md`; `research/CLAIMS.md`; `research/LOOP_LOG.md`; `research/SELECTION.md`; `research/PRIOR_ART.md`; `research/MODEL.md`; `research/THESIS.md`; `research/BASELINES.md`; `research/PROTOCOL.md`; `research/THREATS.md`; `workflow/graph.json`.

Then, from the checkout root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_baseline.py
python3 -m durability_debt probe --output /tmp/durability-debt-successor-probe
python3 -m durability_debt verify /tmp/durability-debt-successor-probe
```

Use a fresh output path if that path already exists. Python >=3.11, standard library only; no dependency installation is needed for these commands. `verify results/launch` is valid only on the recorded source/settings/environment. On another Python/kernel/platform it should refuse checkpoint reuse; inspect it as historical evidence and produce a fresh local bundle. That refusal is not a scientific regression.

The canonical launch run has **13 passing gates, eight cases, five baseline/order configurations, and 13 passing regressions**. Producer-first one-trace misses the unsafe-handoff failure; consumer-first one-trace finds it and gets full credit. Joint projected outcome sets match under reversed traversal. Safe handoff, old-version, no-sink, logger and validating-cache controls pass. Extrema is an elementary exact-existence null, not the new method. `results/pre-seed-reversal/` preserves the earlier six-case run with its older source hashes; it is intentionally not a current checkpoint.

## First work package: G2, sole writer research-lead

1. Pin the exact PerSeVerE paper/appendix/evaluated artifact and available implementation/license/toolchain. Read the recovery-observer/p-snapshot/DPOR arguments, then Pathfinder's concurrency/pruning boundary and PMRace/DURINN. Use the bibliography; do not count an unavailable artifact as a passed comparison. Save pins in `research/dependency-pins.json`.
2. Write `research/REDUCTION_DECISION.md` **before building a native backend**. State the proposed preserved property, precise candidate relation/algorithm, exact predecessor translation, and strongest null. If no distinct candidate can be stated, record that honestly and close the methods claim; do not fill the document with a promised future algorithm.
3. Implement the strongest B4 composition and explicit-observer null against the finite reference. Ordinary resource-aware POR, exact image deduplication and per-trace pruning are allowed in B4. The delivered extrema shortcut is not a substitute for B4 or an applicable PerSeVerE run.
4. Freeze the finite grammar before enumerating it: at most eight events, two actors, two preemptions, values `{0,1}`, with explicit exclusions. Gate 1 needs a nonmonotone checker extension before it can claim that coverage; the current `Claim` language is only integer order/discardable cache. Do not silently apply extrema to the extension.
5. Compare exact outcome sets, not only counts or first witnesses. Produce minimal counterexamples for necessary-rule mutants. Keep execution/read-from, storage legality, and semantic obligations separate. Never insert desired source survival into storage order to make the failure disappear.
6. Establish a defended product-specific separation from strong composition, or kill the proposed method. The cap is 40 author-hours and 4 CPU-hours finite enumeration, with the memory/output limits in PROTOCOL. No open-ended rescue loops.
7. Save source/input/model/checker hashes, complete/incomplete status, counterexamples and decision. Update graph status, claim ledger and loop log. Commit actual increments with the sole-author identity. A failed G2 blocks G3–G6; use G7 for an honest negative closeout.

## If—and only if—G2 advances

- **G3 / Gate 2:** implement a restricted safe native supervisor and crash backend. FUSE requests are not syscalls; supervise process/IPC separately. The host has a FUSE device and C++ toolchain, but `pkg-config fuse3` lacked development metadata during launch. No rootless mount/native injection was attempted. Missing headers/permissions are blockers, not permission to sudo, alter `/etc/fuse.conf`, enable `allow_other`, or weaken SELinux/ptrace/security.
- **G4 / Gate 3:** acquire exactly one qualifying pinned/licensed workflow from each of six classes; freeze actual upstream promises/checkers before faults. No planted changes to targets. Require the strong B4 and prevention comparisons, not merely a Cartesian speedup.
- **G5 / Gate 4:** expand to the preregistered twenty workflows only after the six-class pilot passes. Preserve null, unsupported and censored rows. The convenience corpus cannot estimate ecosystem prevalence.
- **G6:** write a positive thesis only with supported mechanism/native/practical claims, renewed hostile review and safe disclosure. Venue fit and acceptance remain decisions, not promises.
- **G7:** if a gate dies, publish a precise negative/blocked record and reusable evidence where appropriate. A material pivot needs an explicit new decision; do not quietly start the wheel or trajectory alternative.

## Persistent discipline

`workflow/graph.json` is the DAG authority; `research/LOOP_LOG.md` records goal/action/observation/adjustment. Each output has one logical owner. Parallelize independent ownership only; integrate shared code/schema changes serially. Preserve every run directory; hash-bound completed checkpoints only. One exact transient rerun plus one cause-directed adjustment is the maximum failing-branch recovery loop.

No model/API spending, GPU work, custom kernel, physical power loss, host-data fault injection, unrelated repository edits, fabricated findings or hidden negative results. Do not contact maintainers about a synthetic litmus as though it were an upstream vulnerability. Follow the disclosure contract for genuine findings.
