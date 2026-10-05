# Durability Debt

A small Python demo of a producer publishing data before it is durable, leaving a consumer's saved result without its input after a crash.

**Question:** how can a schedule that looks correct without a crash break recovery?

[model.py](durability_debt/model.py) interprets atomic integer records, volatile signals, and per-record flushes. [explore.py](durability_debt/explore.py) enumerates bounded schedules and allowed crash images, then replays a failing witness. [cases.py](durability_debt/cases.py) defines the unsafe handoff, its fix, and synthetic controls.

## The race and the fix

Initially, both `source` and `manifest` contain the old version. The recovery rule is `manifest <= source`: a saved result must not refer to a source version that was lost.

```text
Producer                       Consumer
write source = 1
signal ready ----------------> wait ready
                               read source = 1
                               write manifest = 1
                               flush manifest
                 CRASH before producer flushes source
```

The allowed crash image is **`source=0, manifest=1`**. Recovery keeps these values, violating the rule: the consumer's result survived but its input did not. The signal made the write visible, not durable.

**Fix:** change the producer to `write source; flush source; signal ready`. The consumer cannot see the new version until it is forced to survive a modeled crash.

## Result

The [saved explorer report](results/launch/report.json) gives these counts. Crash checks include repeated images at different execution prefixes; bad observations are distinct recovery outcomes, not separate bugs.

| Case / search | Complete schedules | Crash checks | Bad observations |
|---|---:|---:|---:|
| Publish first, producer-first trace | 1 | 11 | 0 |
| Publish first, consumer-first trace | 1 | 16 | 1 |
| Publish first, joint exploration | 5 | 34 | 1 |
| Flush first, joint exploration | 1 | 10 | 0 |

The producer-first trace misses the race. **A simple consumer-first single-trace baseline finds it too.** This demonstrates schedule sensitivity, not a new detection algorithm or an advantage over strong baselines.

## Reproduce

From this checkout, with Python 3.11 or newer and its standard library:

```sh
nice -n 19 python3 tools/demo.py
nice -n 19 python3 -m unittest discover -s tests -v
```

The demo prints the table, a replayed instruction trace, the crash image, and the fix. A local CPU is enough; no GPU, downloads, paid services, or application data are used. Hardware and model boundaries are documented in the [project notes](docs/README.md), together with the preserved research charter and full probe instructions.

## Limitations

- Synthetic examples, not bugs discovered in real applications.
- Atomic whole-record writes and independent record persistence; no torn writes or filesystem metadata.
- Exploration allows at most two preemptions, not all possible schedules.
- No native processes, ext4, SQLite, mmap, or physical power-loss experiments.
- Flush-before-publication fixes this model, not every real storage protocol.

## Prior work and authorship

The visibility-before-durability problem is established in [PMRace](https://github.com/yhuacode/pmrace) and [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf). [PerSeVerE](https://plv.mpi-sws.org/persevere/) explores concurrency and persistence together; [ALICE](https://github.com/madthanu/alice) constructs application crash states. This is an independently authored teaching model, not a reproduction of their implementations.

Alp Cetin (`mottopanikeiku`), MIT license. AI assistance was used in research and implementation.
