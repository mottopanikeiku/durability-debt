# Durability Debt

An interactive model of one crash-consistency bug. A producer makes a write visible before it is durable, a consumer builds on it and saves the result, and a crash leaves that result on disk without the input it came from.

```text
Producer                       Consumer
write source = 1
signal ready ----------------> wait ready
                               read source = 1
                               copy manifest from read
                               flush manifest
                 CRASH before producer flushes source
```

The producer writes `source = 1` and signals "ready" before flushing it. The consumer reads the new source, writes `manifest = 1` and flushes that. A crash before the producer's flush can leave `manifest = 1` and `source = 0` on disk, which breaks the recovery rule `manifest <= source`. In this model, flushing the source before signaling (`write source; flush source; signal ready`) leaves no bad crash state.

![Stepping through the unsafe ordering, then the fixed one](assets/durability-debt.gif)

The [lesson page](https://mottopanikeiku.github.io/durability-debt/) steps through either ordering one instruction at a time. After each instruction it lists every disk state a crash could leave and marks the ones that break recovery. It works offline, and the tables are plain HTML if JavaScript is off.

A small explorer generates all of it. With at most two preemptions, the unsafe ordering has five schedules and one bad crash outcome in 34 crash checks. Whether a single test run sees the bug depends on the schedule. A producer-first trace flushes the source before the consumer reads it and never sees it; a consumer-first trace finds it.

## Building the page

Python 3.11+, no dependencies:

```sh
python3 tools/build_site.py --output _site
python3 tools/demo.py
python3 -m unittest discover -s tests -v
```

Then open `_site/index.html`. The [model notes](docs/model.md) cover the instructions, scheduling and saved results.

## Related work

The same failure class is studied in [PMRace](https://github.com/yhuacode/pmrace), [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf), [PerSeVerE](https://plv.mpi-sws.org/persevere/) and [ALICE](https://github.com/madthanu/alice), on real persistent memory and file systems. This repo uses a tiny integer-record model so the bug is easy to see. MIT license.
