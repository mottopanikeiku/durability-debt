# Project notes

The current deliverable is a small finite crash-recovery demo. It does not establish a new search method or run native applications. `tools/demo.py` makes the existing modeled failure and its ordinary prevention visible without producing a large experiment bundle.

## Run the full reference experiment

From the repository root, with Python 3.11 or newer:

```sh
nice -n 19 python3 -m durability_debt probe --output /tmp/durability-debt-local-probe
nice -n 19 python3 -m durability_debt verify /tmp/durability-debt-local-probe
nice -n 19 python3 tools/check_baseline.py
```

Choose a new output directory for each probe; existing directories are never overwritten. The first command runs the synthetic cases and both single-trace baselines, compares joint exploration in both traversal orders, and checks the elementary extrema comparator. The second checks that the new bundle matches its source, settings, environment, and artifact hashes. The last checks the preserved research graph, Markdown links, and original source/artifact hashes; it is not a scientific acceptance test.

No packages, GPU, paid services, or native fault injection are needed. Use a local CPU. The implementation bounds exploration at 50,000 prefixes and 250,000 crash evaluations per search; these limits are recorded in [probe.py](../durability_debt/probe.py). It raises an error rather than calling a capped search complete.

## Preserved records

- [Model assumptions](research/MODEL.md), [original claims](research/CLAIMS.md), and [prior work](research/PRIOR_ART.md).
- Original research proposal: [thesis](research/THESIS.md), [selection](research/SELECTION.md), [protocol](research/PROTOCOL.md), [baselines](research/BASELINES.md), [threats](research/THREATS.md), and [source catalog](research/SOURCES.json).
- Historical instructions and decisions: [agent contract](AGENTS.md), [successor handoff](NEXT_STEPS.md), [loop log](research/LOOP_LOG.md), and [workflow graph](workflow/graph.json).
- Unchanged result bundles: [launch](../results/launch/) and [earlier run](../results/pre-seed-reversal/).

The charter and handoff are historical, not current instructions to build a native backend or spend their proposed budgets. Their `research/`, `workflow/`, `AGENTS.md`, and `NEXT_STEPS.md` paths refer to files now under `docs/`; code, tools, tests, and results remain at the repository root. The archived graph retains its original paths, which `tools/check_baseline.py` resolves to the moved files. Absolute checkout paths in old instructions are not a request to modify another checkout.

Historical manifests bind the original environment. A refusal to reuse a saved bundle on another host is expected; read it as historical data and create a fresh local probe.

## Recommendation

Keep this as a small teaching demo: it has an executable race, a replayable crash image, negative controls, and a fix that is easy to understand. The consumer-first single-trace baseline already finds the motivating failure, and no superiority over existing methods or native capability has been demonstrated. Do not present the archived thesis as an achieved research contribution.

The owner should decide whether a teaching artifact is worth maintaining. If the repository was intended only as a new research contribution, archiving is more honest than leaving a large proposed experiment plan as its public promise. No repository settings were changed.
