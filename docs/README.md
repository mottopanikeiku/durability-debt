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

I publish the [lesson](https://mottopanikeiku.github.io/durability-debt/) with GitHub Actions. To deploy manually, run **Teaching page** on `main` with `deploy` checked. Automatic deployment on main pushes uses the repository Actions variable `PAGES_ENABLED=true`; pull requests do not deploy.

## Run the full reference experiment

From the repository root, with Python 3.11 or newer:

```sh
nice -n 19 python3 -m durability_debt probe --output /tmp/durability-debt-local-probe
nice -n 19 python3 -m durability_debt verify /tmp/durability-debt-local-probe
nice -n 19 python3 tools/check_baseline.py
```

Choose a new output directory for each probe; existing directories are never overwritten. The first command runs the synthetic cases and both single-trace baselines, compares joint exploration in both traversal orders, and checks the elementary extrema comparator. The second checks the new bundle against its source, settings, environment, and artifact hashes. The last checks local Markdown links and original source/artifact hashes.

I run `python3 tools/demo.py` and `python3 -m unittest discover -s tests -v` after behavior changes, using a local CPU with `nice -n 19`. I do not fault-inject against real user data, change host privileges, or overwrite result bundles. I keep published data, prior-work attribution, and the AI-assistance disclosure intact. The implementation bounds exploration at 50,000 prefixes and 250,000 crash evaluations per search; these limits are recorded in [probe.py](../durability_debt/probe.py). It raises an error rather than calling a capped search complete.

## Preserved records

- [Historical native-research proposal](research/THESIS.md).
- Unchanged result bundles: [launch](../results/launch/) and [earlier run](../results/pre-seed-reversal/).

Historical manifests bind the original environment. A refusal to reuse a saved bundle on another host is expected; read it as historical data and create a fresh local probe.

## Interpretation

The consumer-first single-trace baseline already finds the motivating failure. I have not demonstrated superiority over existing methods, native capability, or a new research contribution. The archived proposal describes work that was not carried out; the page teaches the executable finite example instead.
