# Contributor notes

This repository is a synthetic crash-recovery teaching demo. Start with `README.md`, `durability_debt/model.py`, `durability_debt/explore.py`, and `durability_debt/cases.py`. The larger research charter in `docs/` is historical; it is not a requirement to build a native tester.

Keep model boundaries explicit. Do not claim a real application bug, native filesystem correctness, new algorithm, or speedup from these examples. Credit the consumer-first single-trace baseline, which finds the same failure as joint exploration.

Run the demo and `python3 -m unittest discover -s tests -v` after behavior changes. Use local CPU only, with `nice -n 19`. Never fault-inject against real user data, change host privileges, or overwrite result bundles. Keep published data and prior-work attribution intact.

Author: Alp Cetin (`mottopanikeiku`). The MIT license covers this project's own material. Disclose AI assistance and preserve third-party attribution; do not invent authors or coauthor trailers.
