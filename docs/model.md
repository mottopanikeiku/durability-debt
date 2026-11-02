# The model

Records are atomic integers that persist independently of each other, while registers and signals are volatile and vanish in a crash. A crash can happen at any instruction boundary, and the explorer enumerates schedules with at most two preemptions. Torn writes, file-system metadata and real devices are outside the model. The code is in [model.py](../durability_debt/model.py), [explore.py](../durability_debt/explore.py) and [cases.py](../durability_debt/cases.py).

## State and instructions

A program has one or two actors, integer records and recovery claims, and each record keeps its write history along with a forced-persistence index.

| Instruction | Effect |
|---|---|
| `write(record, n)` | append a visible atomic version |
| `read(record, reg)` | read the latest visible version |
| `copy(record, reg)` | write the actor's saved value |
| `flush(record)` | force persistence up to the current latest version |
| `signal(name)` / `wait(name)` | volatile handoff, no persistence guarantee |

## Crashes and recovery

At every instruction boundary the explorer picks, for each record, any persisted version between its forced and latest index, and registers and signals vanish. A flush stops rollback past its point, but it doesn't force later writes to survive.

`Claim(source, dependent)` requires `dependent <= source` after recovery, and with `discard_invalid=True` a dependent value that names a missing source is dropped, which models a rebuildable cache.

## Scheduling

The search allows two preemptions, where switching away from an actor that could still run counts as one. A producer-first trace always runs the lowest enabled actor and a consumer-first trace the highest, while joint exploration branches on every choice. Searches stop at 50,000 prefixes or 250,000 crash checks.

For a claim `dependent <= source`, a violating image exists exactly when `max(dependent) > min(source)` over the persisted values that may survive. The `joint_extrema` search checks only that candidate per claim, so it finds the same failures with fewer crash checks.

## Results

Joint exploration of the eight example programs gives these counts, taken from [results/launch/report.json](../results/launch/report.json):

| Program | Schedules | Crash checks | Bad observations |
|---|---:|---:|---:|
| `publish_before_flush` | 5 | 34 | 1 |
| `flush_before_publish` | 1 | 10 | 0 |
| `old_version_consumer` | 4 | 29 | 0 |
| `no_relevant_sink` | 3 | 15 | 0 |
| `independent_logger` | 5 | 34 | 0 |
| `self_validating_cache` | 5 | 34 | 0 |
| `single_process_missing_flush` | 1 | 9 | 1 |
| `independent_noise` | 9 | 193 | 1 |

The producer-first trace flushes the source before the consumer reads it, so it never sees the bug, while the consumer-first trace finds it in 16 crash checks.

## Run everything

```sh
python3 -m durability_debt probe --output runs/local
python3 -m durability_debt verify runs/local
python3 tools/check_baseline.py
python3 -m unittest discover -s tests -v
```

Each probe should get a fresh output directory, and `verify` rejects a run whose sources, settings or files have changed.

## Further reading

- [PMRace](https://github.com/yhuacode/pmrace) (ASPLOS 2022): cross-thread reads of unpersisted memory.
- [DURINN](https://www.usenix.org/system/files/osdi22-fu.pdf) (OSDI 2022): visible-but-not-durable states in persistent memory.
- [PerSeVerE](https://plv.mpi-sws.org/persevere/) (POPL 2021): concurrency and ext4 persistence in one model checker.
- [ALICE](https://github.com/madthanu/alice) (OSDI 2014): application crash states from syscall traces.
- [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) and [SQLite atomic commit](https://sqlite.org/atomiccommit.html): why real files need more than a data flush.
