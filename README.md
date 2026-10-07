# Durability Debt

I built a small crash-recovery teaching demo about a write that becomes visible before it becomes durable.

**Question:** how can a schedule that looks correct without a crash leave a saved result without its input?

The browser lesson steps through an unsafe producer/consumer handoff and its fix. At each instruction boundary it shows every disk state the finite model allows, and whether recovery accepts it. I generate the events, crash states, and comparison counts from [the model](durability_debt/model.py) and [the explorer](durability_debt/explore.py), not from a hand-written animation.

Build the page below, then open `_site/index.html`. It works offline, needs no JavaScript framework, and includes the full boundary tables even with JavaScript disabled. The [page generator](tools/build_site.py) also exports `scenario.json` with source hashes.

## What the demo teaches

In [the modeled cases](durability_debt/cases.py), both `source` and `manifest` start at version `0`. Recovery requires `manifest <= source`: a saved result must not refer to an input version that disappeared.

```text
Producer                       Consumer
write source = 1
signal ready ----------------> wait ready
                               read source = 1
                               copy manifest from read
                               flush manifest
                 CRASH before producer flushes source
```

The explorer finds a witness allowing **`source=0, manifest=1`** ([saved witness](results/launch/report.json)). I replay that witness through the consumer's flush, then finish the schedule. At the failing boundary, the consumer's result must survive but the source may not. At the final boundary, both records are flushed and recovery is valid again. A correct ending does not make every earlier crash safe.

**Fix:** `write source; flush source; signal ready`. The consumer cannot read the new version until it is forced to survive a modeled crash. The page lets you compare both orderings and inspect the allowed crash images rather than just watching the failure.

## Result

The [saved explorer report](results/launch/report.json) records these counts. The page regenerates them with the same search settings. Crash checks include repeated images at different execution prefixes; bad observations are distinct recovery outcomes, not separate bugs.

| Case / search | Complete schedules | Crash checks | Bad observations |
|---|---:|---:|---:|
| Publish first, producer-first trace | 1 | 11 | 0 |
| Publish first, consumer-first trace | 1 | 16 | 1 |
| Publish first, joint exploration | 5 | 34 | 1 |
| Flush first, joint exploration | 1 | 10 | 0 |

The producer-first trace misses the race. **A consumer-first single-trace baseline finds it too.** I demonstrate schedule sensitivity, not a new detection algorithm or a speedup.

## Reproduce

From a checkout, with Python 3.11 or newer and its standard library:

```sh
nice -n 19 python3 tools/build_site.py --output _site
nice -n 19 python3 tools/demo.py
nice -n 19 python3 -m unittest discover -s tests -v
```

Open `_site/index.html` for the lesson. A local CPU is enough; no GPU, downloads, paid services, or application data are used. The [project notes](docs/README.md) cover the full probe, historical records, and owner-controlled Pages deployment. No Pages URL is promised before deployment is enabled.

## Limitations

- Synthetic examples, not bugs discovered in real applications.
- Atomic whole-record writes and independent persistence; no torn writes or filesystem metadata.
- Exploration allows at most two preemptions ([search default](durability_debt/explore.py)), not all possible schedules.
- No native processes, ext4, SQLite, mmap, or physical power-loss experiments.
- Flush-before-publication fixes this model, not every real storage protocol.

## Prior work and authorship

The visibility-before-durability problem is established in [PMRace](https://github.com/yhuacode/pmrace) and [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf). [PerSeVerE](https://plv.mpi-sws.org/persevere/) explores concurrency and persistence together; [ALICE](https://github.com/madthanu/alice) constructs application crash states. I wrote this teaching model independently; it is not a reproduction of their implementations.

Alp Cetin (`mottopanikeiku`), MIT license.

Written with AI coding assistance.
