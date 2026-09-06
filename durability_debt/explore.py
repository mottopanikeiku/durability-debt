"""Exhaustive bounded scheduling and replayable crash witnesses."""
from dataclasses import asdict

from .model import Program, State, crash_versions, disk_image, enabled, initial_state, observation, recover, step


class ExplorationLimit(RuntimeError):
    """A resource cap was reached; no completeness claim is available."""


def explore(
    program: Program,
    *,
    crash_policy: str = "cartesian",
    scheduling: str = "joint",
    max_preemptions: int = 2,
    max_prefixes: int = 50_000,
    max_crash_evaluations: int = 250_000,
) -> dict:
    if crash_policy not in {"cartesian", "extrema"} or scheduling not in {"joint", "seed"}:
        raise ValueError("unsupported exploration policy")
    if max_preemptions < 0 or max_prefixes < 1 or max_crash_evaluations < 1:
        raise ValueError("invalid exploration bound")
    counts = dict(prefixes=0, complete_schedules=0, deadlocked_prefixes=0,
                  crash_evaluations=0, preemption_pruned_branches=0,
                  no_crash_violations=0)
    raw_images, observations, failures = set(), set(), set()
    first_witness = None
    first_terminal = None

    def visit(state: State, trace: tuple[int, ...], previous: int | None, preemptions: int) -> None:
        nonlocal first_witness, first_terminal
        counts["prefixes"] += 1
        if counts["prefixes"] > max_prefixes:
            raise ExplorationLimit("prefix cap reached")
        for versions in crash_versions(program, state, crash_policy):
            counts["crash_evaluations"] += 1
            if counts["crash_evaluations"] > max_crash_evaluations:
                raise ExplorationLimit("crash-evaluation cap reached")
            disk = disk_image(program, state, versions)
            recovered, violations = recover(program, disk)
            projected = observation(program, recovered)
            raw_images.add(tuple(sorted(disk.items())))
            observations.add((projected, violations))
            if violations:
                failures.add((projected, violations))
                if first_witness is None:
                    first_witness = {
                        "actors": list(trace), "persisted_prefixes": list(versions),
                        "disk": disk, "recovered": recovered,
                        "violations": list(violations), "preemptions": preemptions,
                    }
        available = enabled(program, state)
        terminal = all(pc == len(actor) for pc, actor in zip(state.pc, program.actors))
        if terminal:
            counts["complete_schedules"] += 1
            visible = disk_image(program, state, tuple(len(history) - 1 for history in state.histories))
            _, violations = recover(program, visible)
            counts["no_crash_violations"] += bool(violations)
            if first_terminal is None:
                first_terminal = list(trace)
            return
        if not available:
            counts["deadlocked_prefixes"] += 1
            return
        if scheduling == "seed":
            available = available[:1]
        for actor in available:
            # Switching away from a still-enabled actor is a preemption;
            # switching after termination/blocking is not.
            added = previous is not None and actor != previous and previous in enabled(program, state)
            next_preemptions = preemptions + int(added)
            if next_preemptions > max_preemptions:
                counts["preemption_pruned_branches"] += 1
                continue
            visit(step(program, state, actor), trace + (actor,), actor, next_preemptions)

    visit(initial_state(program), (), None, 0)
    replay = replay_witness(program, first_witness, max_preemptions=max_preemptions) if first_witness else None
    return {
        "program": program.name, "crash_policy": crash_policy, "scheduling": scheduling,
        "max_preemptions": max_preemptions, "complete_within_bound": True,
        "coverage": "all admitted crash images" if crash_policy == "cartesian" else "existence oracle for declared integer-order claims only",
        **counts, "unique_raw_images": len(raw_images),
        "unique_recovery_observations": len(observations),
        "unique_violating_observations": len(failures),
        "first_witness": first_witness, "witness_replay": replay,
        "seed_or_first_complete_schedule": first_terminal,
    }


def replay_witness(program: Program, witness: dict, *, max_preemptions: int = 2) -> dict:
    state = initial_state(program)
    previous = None
    preemptions = 0
    events = []
    for actor in witness["actors"]:
        if type(actor) is not int or actor not in enabled(program, state):
            raise ValueError("witness contains an infeasible actor choice")
        if previous is not None and actor != previous and previous in enabled(program, state):
            preemptions += 1
        if preemptions > max_preemptions:
            raise ValueError("witness exceeds the scheduling bound")
        instruction = program.actors[actor][state.pc[actor]]
        events.append({"actor": actor, "pc": state.pc[actor], "instruction": asdict(instruction)})
        state = step(program, state, actor)
        previous = actor
    disk = disk_image(program, state, tuple(witness["persisted_prefixes"]))
    recovered, violations = recover(program, disk)
    if (disk != witness["disk"] or recovered != witness["recovered"]
            or list(violations) != witness["violations"] or preemptions != witness["preemptions"]):
        raise ValueError("witness result does not match replay")
    if not violations:
        raise ValueError("witness does not violate a recovery claim")
    return {"verified": True, "events": events}
