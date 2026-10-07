# Project notes

I keep this as a small finite crash-recovery teaching demo, not a new search method or a native application tester. `tools/demo.py` prints the modeled failure; `tools/build_site.py` turns the same model into a browser lesson.

## Build and read the page

```sh
nice -n 19 python3 tools/build_site.py --output _site
nice -n 19 python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`, or open `_site/index.html` directly without a server. Stop the server when finished. The page embeds its generated data, so the interactions also work offline without fetching JSON. `scenario.json` is a downloadable copy with hashes of the model, cases, and explorer sources. The generator has no timestamps or environment paths, and identical sources produce identical files.

The unsafe timeline comes from the explorer's first failing witness, replayed through the consumer's next flush as in `tools/demo.py`, then completed with enabled model instructions. The fixed timeline is the explorer's first complete schedule. At every boundary, the generator runs `crash_versions`, `disk_image`, and `recover` to show all admitted crash images. The comparison table reruns both single-trace searches and joint exploration; it is not a browser-side simulation or a probability estimate.

The controls support keyboard navigation, and the complete crash tables remain readable without JavaScript. The page source is a template under `site/`; open the generated `_site/index.html`, not the template.

## GitHub Pages

The [Pages workflow](../.github/workflows/pages.yml) builds and uploads the page on pull requests and main-branch pushes. Those runs do not require Pages to be enabled. It uses the official checkout, Python setup, Pages artifact, and Pages deployment actions.

After the owner enables Pages with **GitHub Actions** as the publishing source, run **Teaching page** manually on `main` with `deploy` checked. For automatic deployment on later main pushes, the owner can set the repository Actions variable `PAGES_ENABLED` to `true`. Deployment never runs for pull requests, and no workflow enables Pages or changes repository settings. A requested deployment still requires Pages and the `github-pages` environment to be configured; failures are not suppressed.

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
- Historical decisions: [loop log](research/LOOP_LOG.md) and [workflow graph](workflow/graph.json).
- Unchanged result bundles: [launch](../results/launch/) and [earlier run](../results/pre-seed-reversal/).

The research charter is historical, not current instructions to build a native backend or spend its proposed budgets. `research/` and `workflow/` paths in those records refer to files now under `docs/`; code, tools, tests, and results remain at the repository root. I removed the obsolete `docs/AGENTS.md` and `docs/NEXT_STEPS.md` prompts. The archived graph retains their names as historical outputs; `tools/check_baseline.py` explicitly excludes only those retired prompts from file-existence checks and still checks every other completed output. Original result bundles and source hashes are unchanged.

Historical manifests bind the original environment. A refusal to reuse a saved bundle on another host is expected; read it as historical data and create a fresh local probe.

## Interpretation

The consumer-first single-trace baseline already finds the motivating failure. I have not demonstrated superiority over existing methods, native capability, or a new research contribution. The archived proposal describes work that was not carried out; the page teaches the executable finite example instead.
