"""Build a dependency-free teaching page from the finite reference model."""
import argparse
from dataclasses import asdict
import hashlib
from html import escape
import json
from pathlib import Path
import shutil
from string import Template
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from durability_debt.cases import cases
from durability_debt.explore import explore, replay_witness
from durability_debt.model import crash_versions, disk_image, enabled, initial_state, recover, step


def checkpoints(program, actors):
    """Enumerate every admitted crash image after each instruction boundary."""
    state = initial_state(program)
    result = []
    event = None
    for boundary in range(len(actors) + 1):
        images = []
        for versions in crash_versions(program, state, "cartesian"):
            disk = disk_image(program, state, versions)
            recovered, violations = recover(program, disk)
            images.append({"persisted_prefixes": list(versions), "disk": disk,
                           "recovered": recovered, "violations": list(violations)})
        result.append({
            "boundary": boundary, "event": event,
            "visible": {name: state.histories[index][-1]
                        for index, (name, _) in enumerate(program.initial)},
            "forced": {name: state.histories[index][state.forced[index]]
                       for index, (name, _) in enumerate(program.initial)},
            "signals": sorted(state.signals),
            "registers": [dict(registers) for registers in state.registers],
            "crash_images": images,
        })
        if boundary < len(actors):
            actor = actors[boundary]
            instruction = program.actors[actor][state.pc[actor]]
            event = {"actor": actor, "instruction": asdict(instruction)}
            state = step(program, state, actor)
    if enabled(program, state) or any(pc != len(actor) for pc, actor in zip(state.pc, program.actors)):
        raise ValueError("teaching trace must be a complete feasible schedule")
    return result


def scenario_data():
    programs = {program.name: program for program in cases()}
    unsafe = programs["publish_before_flush"]
    unsafe_result = explore(unsafe)
    witness = unsafe_result["first_witness"]
    # As in tools/demo.py, extend the first counterexample through the
    # consumer's flush. Replay checks the image and scheduling bound.
    actors = witness["actors"] + [1]
    replay_witness(unsafe, {**witness, "actors": actors})
    state = initial_state(unsafe)
    for actor in actors:
        state = step(unsafe, state, actor)
    while enabled(unsafe, state):
        actor = enabled(unsafe, state)[0]
        actors.append(actor)
        state = step(unsafe, state, actor)

    scenarios = []
    for name, title, trace in (
        ("publish_before_flush", "Publish before flushing", actors),
        ("flush_before_publish", "Flush before publishing", None),
    ):
        program = programs[name]
        exploration = unsafe_result if name == unsafe.name else explore(program)
        trace = trace if trace is not None else exploration["seed_or_first_complete_schedule"]
        points = checkpoints(program, trace)
        focus = next(point["boundary"] for point in points
                     if point["event"] and point["event"]["instruction"]["kind"] == "flush"
                     and point["event"]["instruction"]["target"] == "manifest")
        scenarios.append({"id": name, "title": title, "actors": trace,
                          "claims": [asdict(claim) for claim in program.claims],
                          "focus_boundary": focus, "checkpoints": points})

    comparisons = []
    for program, label, options in (
        (unsafe, "Publish first / producer-first trace", {"scheduling": "seed"}),
        (unsafe, "Publish first / consumer-first trace", {"scheduling": "seed", "seed_order": "consumer_first"}),
        (unsafe, "Publish first / joint exploration", {}),
        (programs["flush_before_publish"], "Flush first / joint exploration", {}),
    ):
        result = explore(program, **options)
        comparisons.append({"label": label, **{key: result[key] for key in (
            "complete_schedules", "crash_evaluations", "unique_violating_observations")}})
    return {"schema": "durability-debt-teaching/1", "max_preemptions": unsafe_result["max_preemptions"],
            "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in (ROOT / "durability_debt/cases.py", ROOT / "durability_debt/model.py",
                                           ROOT / "durability_debt/explore.py")},
            "scenarios": scenarios, "comparisons": comparisons}


def event_label(event):
    if event is None:
        return "Initial state"
    instruction = event["instruction"]
    operand = "" if instruction["value"] is None else f" {instruction['value']}"
    actor = "Producer" if event["actor"] == 0 else "Consumer"
    return f"{actor}: {instruction['kind']} {instruction['target']}{operand}"


def render_image_rows(images):
    rows = []
    for image in images:
        disk = image["disk"]
        violations = image["violations"]
        outcome = "Violates " + ", ".join(violations) if violations else "Recovers: rule holds"
        style = "bad" if violations else "good"
        rows.append(f'<tr class="{style}"><td>{disk["source"]}</td><td>{disk["manifest"]}</td>'
                    f'<td>{escape(outcome)}</td></tr>')
    return "".join(rows)


def static_content(data):
    """Keep the complete lesson readable when JavaScript is unavailable."""
    sections = []
    for scenario in data["scenarios"]:
        points = []
        for point in scenario["checkpoints"]:
            points.append(f'<details><summary>{point["boundary"]}. {escape(event_label(point["event"]))}</summary>'
                          '<table><caption>Every allowed crash image at this boundary</caption>'
                          '<thead><tr><th>Source on disk</th><th>Manifest on disk</th><th>Recovery</th></tr></thead>'
                          f'<tbody>{render_image_rows(point["crash_images"])}</tbody></table></details>')
        sections.append(f'<section><h3>{escape(scenario["title"])}</h3>{"".join(points)}</section>')
    return "".join(sections)


def comparison_rows(data):
    return "".join(f'<tr><th scope="row">{escape(row["label"])}</th>'
                   f'<td>{row["complete_schedules"]}</td><td>{row["crash_evaluations"]}</td>'
                   f'<td>{row["unique_violating_observations"]}</td></tr>'
                   for row in data["comparisons"])


def build(output):
    output = Path(output)
    if output.resolve() == (ROOT / "site").resolve():
        raise ValueError("choose an output directory other than the site source directory")
    data = scenario_data()
    output.mkdir(parents=True, exist_ok=True)
    for name in ("style.css", "app.js"):
        shutil.copyfile(ROOT / "site" / name, output / name)
    serialized = json.dumps(data, sort_keys=True, indent=2) + "\n"
    (output / "scenario.json").write_text(serialized, encoding="utf-8")
    embedded = json.dumps(data, sort_keys=True).replace("<", "\\u003c")
    template = Template((ROOT / "site/index.html").read_text(encoding="utf-8"))
    page = template.substitute(data=embedded, static_content=static_content(data),
                               comparisons=comparison_rows(data))
    (output / "index.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
