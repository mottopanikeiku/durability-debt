# Durability Debt

**Joint schedule-and-crash exploration for cross-process recovery correctness.**

A producer can publish data before making it durable. A consumer can read that data and persist a dependent result. A crash may preserve the result while losing its input. Individually correct components do not necessarily compose into a crash-correct workflow.

## Research question

Can persistence-sensitive joint schedule/crash exploration find reproducible recovery failures in unmodified local Linux workflows substantially more efficiently than strong one-trace and composed schedule/crash baselines?

This is a **conditional research launch**, not a claim of established novelty or a completed Linux tester. Visible-before-durable races, persistence graphs, and joint concurrency/persistence model checking already exist. The closest threats are PerSeVerE, PMRace, DURINN, ALICE, Pathfinder, and RACEPRO. A useful wrapper is not automatically a new thesis.

## What is executable now

The repository contains a dependency-free finite reference model, exhaustive schedule/crash oracle, seed-schedule baseline, and a deliberately strong elementary extrema baseline. It tests existing atomic records, volatile handoff, and honored per-record flushes. It does **not** execute native applications or model ext4, SQLite internals, namespace operations, torn writes, or mmap.

```sh
python3 -m durability_debt probe --output /tmp/durability-debt-probe
python3 -m unittest discover -s tests -v
```

The probe creates a new immutable run directory; it refuses to overwrite an existing one. Inspect its `report.json` and `manifest.json`. Results distinguish repeated observations from unique recovery images and do not count synthetic witnesses as real bugs.

## Start here

1. [AGENTS.md](AGENTS.md): operational and authorship contract.
2. [NEXT_STEPS.md](NEXT_STEPS.md): exact successor entry point and stop conditions.
3. [research/THESIS.md](research/THESIS.md): provisional thesis and claim boundary.
4. [research/SELECTION.md](research/SELECTION.md): alternatives and adversarial selection.
5. [research/PRIOR_ART.md](research/PRIOR_ART.md): strongest existing work.
6. [research/PROTOCOL.md](research/PROTOCOL.md): preregistered experiments and kill gates.
7. [workflow/graph.json](workflow/graph.json): dependency DAG, owners, inputs, outputs, acceptance.
8. [research/CLAIMS.md](research/CLAIMS.md) and [research/LOOP_LOG.md](research/LOOP_LOG.md): verified state, failed branches, and next decisions.

## Success and failure

A positive thesis requires a substantive capability/reduction beyond ordinary tool composition, semantic recovery witnesses in unmodified real workflows, and fair matched-baseline evidence. A negative result is valid: preserve the artifact and explain which novelty, feasibility, or usefulness gate failed. Do not manufacture significance by weakening baselines, injecting faults into real subjects, or changing the question after seeing results.

Sole human author: **mottopanikeiku (alp)**. MIT license. AI assistance is used in research and implementation; it does not create additional human authors. All third-party work retains its attribution and license.
