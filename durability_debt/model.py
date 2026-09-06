"""Explicit finite semantics; not a POSIX, ext4, or SQLite model.

A record persists a prefix of its atomic write history. Flush forces the
current prefix of one record. Records persist independently. Handoff and
registers are volatile. Only instruction boundaries are scheduling points.
"""
from dataclasses import dataclass, replace
from itertools import product
from typing import Iterator


@dataclass(frozen=True)
class Instruction:
    kind: str
    target: str
    value: int | str | None = None


@dataclass(frozen=True)
class Claim:
    """Recovery requires dependent <= source, or discards an invalid cache."""

    source: str
    dependent: str
    discard_invalid: bool = False


@dataclass(frozen=True)
class Program:
    name: str
    initial: tuple[tuple[str, int], ...]
    actors: tuple[tuple[Instruction, ...], ...]
    claims: tuple[Claim, ...]

    def __post_init__(self) -> None:
        names = [name for name, _ in self.initial]
        if not self.name or not names or len(names) != len(set(names)):
            raise ValueError("program needs a name and unique records")
        if any(not name or type(value) is not int for name, value in self.initial):
            raise ValueError("records require nonempty names and integer values")
        if not 1 <= len(self.actors) <= 2:
            raise ValueError("reference scope is one or two actors")
        for actor in self.actors:
            registers: set[str] = set()
            for instruction in actor:
                kind, target, value = instruction.kind, instruction.target, instruction.value
                if kind not in {"write", "read", "copy", "flush", "signal", "wait"}:
                    raise ValueError(f"unsupported instruction: {kind}")
                if not target or (kind not in {"signal", "wait"} and target not in names):
                    raise ValueError(f"unknown or empty target: {target}")
                if kind == "write" and type(value) is not int:
                    raise ValueError("write requires an integer")
                if kind in {"read", "copy"}:
                    if not isinstance(value, str) or not value:
                        raise ValueError("read/copy requires a register name")
                    if kind == "copy" and value not in registers:
                        raise ValueError("copy uses an undefined actor-local register")
                    registers.add(value)
                elif kind != "write" and value is not None:
                    raise ValueError("unexpected instruction operand")
        dependents = [claim.dependent for claim in self.claims]
        if len(dependents) != len(set(dependents)):
            raise ValueError("each dependent has exactly one recovery policy")
        discarded = {claim.dependent for claim in self.claims if claim.discard_invalid}
        for claim in self.claims:
            if claim.source not in names or claim.dependent not in names:
                raise ValueError("claim refers to an unknown record")
            if claim.source == claim.dependent or claim.source in discarded:
                raise ValueError("claim source must be a distinct non-discardable record")


@dataclass(frozen=True)
class State:
    pc: tuple[int, ...]
    histories: tuple[tuple[int, ...], ...]
    forced: tuple[int, ...]
    registers: tuple[tuple[tuple[str, int], ...], ...]
    signals: frozenset[str] = frozenset()


def initial_state(program: Program) -> State:
    return State(
        pc=(0,) * len(program.actors),
        histories=tuple((value,) for _, value in program.initial),
        forced=(0,) * len(program.initial),
        registers=((),) * len(program.actors),
    )


def enabled(program: Program, state: State) -> tuple[int, ...]:
    actors = []
    for actor, instructions in enumerate(program.actors):
        if state.pc[actor] == len(instructions):
            continue
        instruction = instructions[state.pc[actor]]
        if instruction.kind != "wait" or instruction.target in state.signals:
            actors.append(actor)
    return tuple(actors)


def step(program: Program, state: State, actor: int) -> State:
    if actor not in enabled(program, state):
        raise ValueError("actor is blocked, finished, or unknown")
    instruction = program.actors[actor][state.pc[actor]]
    pc = list(state.pc)
    pc[actor] += 1
    next_state = replace(state, pc=tuple(pc))
    kind, target, value = instruction.kind, instruction.target, instruction.value
    if kind == "wait":
        return next_state
    if kind == "signal":
        return replace(next_state, signals=state.signals | {target})
    index = next(i for i, (name, _) in enumerate(program.initial) if name == target)
    if kind == "flush":
        forced = list(state.forced)
        forced[index] = len(state.histories[index]) - 1
        return replace(next_state, forced=tuple(forced))
    if kind == "read":
        registers = list(state.registers)
        local = dict(registers[actor])
        local[value] = state.histories[index][-1]
        registers[actor] = tuple(sorted(local.items()))
        return replace(next_state, registers=tuple(registers))
    payload = value if kind == "write" else dict(state.registers[actor])[value]
    histories = list(state.histories)
    histories[index] += (payload,)
    return replace(next_state, histories=tuple(histories))


def disk_image(program: Program, state: State, versions: tuple[int, ...]) -> dict[str, int]:
    if len(versions) != len(program.initial):
        raise ValueError("one persisted prefix is required per record")
    for index, version in enumerate(versions):
        if type(version) is not int or not state.forced[index] <= version < len(state.histories[index]):
            raise ValueError("persisted prefix violates the record flush/history")
    return {
        name: state.histories[index][versions[index]]
        for index, (name, _) in enumerate(program.initial)
    }


def crash_versions(program: Program, state: State, policy: str) -> Iterator[tuple[int, ...]]:
    ranges = tuple(range(forced, len(history)) for forced, history in zip(state.forced, state.histories))
    if policy == "cartesian":
        yield from product(*ranges)
        return
    if policy != "extrema":
        raise ValueError(f"unknown crash policy: {policy}")
    # Strong elementary baseline, NOT a proposed novel reduction. For these
    # independent integer-order claims, source minimum/dependent maximum is
    # an exact existential counterexample oracle. It does not enumerate all
    # recovery observations and does not generalize to arbitrary checkers.
    names = [name for name, _ in program.initial]
    candidates = set()
    for claim in program.claims:
        versions = list(state.forced)
        source, dependent = names.index(claim.source), names.index(claim.dependent)
        versions[source] = min(ranges[source], key=state.histories[source].__getitem__)
        versions[dependent] = max(ranges[dependent], key=state.histories[dependent].__getitem__)
        candidates.add(tuple(versions))
    if not candidates:
        candidates.add(state.forced)
    yield from sorted(candidates)


def recover(program: Program, disk: dict[str, int]) -> tuple[dict[str, int | None], tuple[str, ...]]:
    recovered: dict[str, int | None] = dict(disk)
    violations = []
    for claim in program.claims:
        if disk[claim.dependent] > disk[claim.source]:
            if claim.discard_invalid:
                recovered[claim.dependent] = None
            else:
                violations.append(f"{claim.dependent}<={claim.source}")
    return recovered, tuple(violations)


def observation(program: Program, recovered: dict[str, int | None]) -> tuple:
    relevant = {name for claim in program.claims for name in (claim.source, claim.dependent)}
    return tuple((name, recovered[name]) for name in sorted(relevant))
