"""Print the modeled race, replay its crash witness, and compare the fix."""
from pathlib import Path
import sys

# Run directly from a checkout without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from durability_debt.cases import cases
from durability_debt.explore import explore, replay_witness


def main() -> None:
    programs = {program.name: program for program in cases()}
    unsafe = programs["publish_before_flush"]
    comparisons = (
        ("publish_before_flush", "producer-first trace", explore(unsafe, scheduling="seed")),
        ("publish_before_flush", "consumer-first trace", explore(unsafe, scheduling="seed", seed_order="consumer_first")),
        ("publish_before_flush", "joint exploration", explore(unsafe)),
        ("flush_before_publish", "joint exploration", explore(programs["flush_before_publish"])),
    )
    print("Finite atomic-record model; at most two preemptions.")
    print("Case                  Search                Schedules  Crash checks  Bad observations")
    for name, search, result in comparisons:
        print(f"{name:21} {search:21} {result['complete_schedules']:9}"
              f" {result['crash_evaluations']:13} {result['unique_violating_observations']:17}")

    # The first bad image allows an unflushed manifest to persist. Include
    # the consumer's next instruction (flush) to show a forced durable result.
    first = comparisons[2][2]["first_witness"]
    witness = {**first, "actors": first["actors"] + [1]}
    replay = replay_witness(unsafe, witness)
    print("\nReplayed failing prefix after consumer flush (source is still unflushed):")
    for event in replay["events"]:
        instruction = event["instruction"]
        actor = "producer" if event["actor"] == 0 else "consumer"
        operand = "" if instruction["value"] is None else f" {instruction['value']}"
        print(f"  {actor}: {instruction['kind']} {instruction['target']}{operand}")
    print(f"  crash image: source={witness['disk']['source']}, manifest={witness['disk']['manifest']}")
    print(f"  recovery requires manifest <= source; violated: {', '.join(witness['violations'])}")
    print("\nFix: write source -> flush source -> signal ready.")
    print("The consumer-first single-trace baseline finds the same failure; no novelty or speedup claim.")


if __name__ == "__main__":
    main()
