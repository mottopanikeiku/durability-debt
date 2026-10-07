from dataclasses import asdict
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from durability_debt.cases import cases
from durability_debt.explore import explore, replay_witness
from durability_debt.model import crash_versions, disk_image, initial_state, recover, step
from tools.build_site import ROOT, build, scenario_data
from tools.check_baseline import check


class EmbeddedDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data = False
        self.chunks = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "scenario-data":
            self.in_data = True

    def handle_data(self, data):
        if self.in_data:
            self.chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_data = False


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = scenario_data()
        cls.programs = {program.name: program for program in cases()}

    def test_every_boundary_and_crash_image_comes_from_the_model(self):
        for scenario in self.data["scenarios"]:
            program = self.programs[scenario["id"]]
            state = initial_state(program)
            self.assertEqual(len(scenario["checkpoints"]), len(scenario["actors"]) + 1)
            for boundary, point in enumerate(scenario["checkpoints"]):
                self.assertEqual(point["boundary"], boundary)
                self.assertEqual(point["visible"], {
                    name: state.histories[index][-1] for index, (name, _) in enumerate(program.initial)})
                self.assertEqual(point["forced"], {
                    name: state.histories[index][state.forced[index]]
                    for index, (name, _) in enumerate(program.initial)})
                self.assertEqual(point["signals"], sorted(state.signals))
                self.assertEqual(point["registers"], [dict(registers) for registers in state.registers])
                expected = []
                for versions in crash_versions(program, state, "cartesian"):
                    disk = disk_image(program, state, versions)
                    recovered, violations = recover(program, disk)
                    expected.append({"persisted_prefixes": list(versions), "disk": disk,
                                     "recovered": recovered, "violations": list(violations)})
                self.assertEqual(point["crash_images"], expected)
                if boundary < len(scenario["actors"]):
                    actor = scenario["actors"][boundary]
                    instruction = program.actors[actor][state.pc[actor]]
                    self.assertEqual(scenario["checkpoints"][boundary + 1]["event"],
                                     {"actor": actor, "instruction": asdict(instruction)})
                    state = step(program, state, actor)
            self.assertEqual(state.pc, tuple(len(actor) for actor in program.actors))

    def test_focused_unsafe_crash_is_a_replayable_flushed_manifest(self):
        unsafe = self.data["scenarios"][0]
        point = unsafe["checkpoints"][unsafe["focus_boundary"]]
        self.assertEqual(point["event"]["instruction"],
                         {"kind": "flush", "target": "manifest", "value": None})
        self.assertEqual(point["forced"], {"source": 0, "manifest": 1})
        image = next(image for image in point["crash_images"] if image["violations"])
        self.assertEqual(image["disk"], {"source": 0, "manifest": 1})
        witness = explore(self.programs[unsafe["id"]])["first_witness"]
        witness = {**witness, **image, "actors": unsafe["actors"][:point["boundary"]]}
        self.assertTrue(replay_witness(self.programs[unsafe["id"]], witness)["verified"])

    def test_fixed_trace_and_both_terminal_states_recover(self):
        fixed = self.data["scenarios"][1]
        self.assertTrue(all(not image["violations"] for point in fixed["checkpoints"]
                            for image in point["crash_images"]))
        for scenario in self.data["scenarios"]:
            self.assertEqual(scenario["checkpoints"][-1]["crash_images"], [{
                "persisted_prefixes": [1, 1], "disk": {"source": 1, "manifest": 1},
                "recovered": {"source": 1, "manifest": 1}, "violations": []}])

    def test_generated_comparisons_match_saved_report(self):
        archived = json.loads((ROOT / "results/launch/report.json").read_text())["results"]
        keys = [("publish_before_flush", "seed_cartesian"),
                ("publish_before_flush", "bad_seed_cartesian"),
                ("publish_before_flush", "joint_cartesian"),
                ("flush_before_publish", "joint_cartesian")]
        for comparison, (program, policy) in zip(self.data["comparisons"], keys):
            for key in ("complete_schedules", "crash_evaluations", "unique_violating_observations"):
                self.assertEqual(comparison[key], archived[program][policy][key])

    def test_build_is_deterministic_and_readable_without_javascript(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first", Path(directory) / "second"
            build(first)
            build(second)
            self.assertEqual(sorted(path.name for path in first.iterdir()),
                             ["app.js", "index.html", "scenario.json", "style.css"])
            for path in first.iterdir():
                self.assertEqual(path.read_bytes(), (second / path.name).read_bytes())
            page = (first / "index.html").read_text()
            parser = EmbeddedDataParser()
            parser.feed(page)
            self.assertEqual(json.loads("".join(parser.chunks)), self.data)
            self.assertEqual(json.loads((first / "scenario.json").read_text()), self.data)
            self.assertIn("Consumer: flush manifest", page)
            self.assertIn("Violates manifest&lt;=source", page)
            self.assertEqual(page.count("<details>"), sum(len(scenario["checkpoints"])
                                                         for scenario in self.data["scenarios"]))
            self.assertNotIn("${", page)
            self.assertNotIn(str(ROOT), page)

    def test_archived_checker_allows_only_retired_prompts_to_be_absent(self):
        self.assertFalse((ROOT / "docs/AGENTS.md").exists())
        self.assertFalse((ROOT / "docs/NEXT_STEPS.md").exists())
        self.assertTrue(check()["valid"])
        original = Path.is_file

        def missing_model(path):
            return False if path == ROOT / "durability_debt/model.py" else original(path)

        with patch.object(Path, "is_file", missing_model):
            with self.assertRaisesRegex(ValueError, "completed output missing"):
                check()


if __name__ == "__main__":
    unittest.main()
