import copy
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

from durability_debt.cases import cases
from durability_debt.explore import ExplorationLimit, explore, replay_witness
from durability_debt.model import Claim, Instruction as I, Program, crash_versions, disk_image, initial_state, recover, step
from durability_debt.probe import SETTINGS, run_probe, verify_bundle


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.programs = {program.name: program for program in cases()}

    def test_rescheduling_exposes_a_replayable_failure_hidden_by_seed(self):
        program = self.programs["publish_before_flush"]
        self.assertEqual(explore(program, scheduling="seed")["unique_violating_observations"], 0)
        result = explore(program)
        self.assertGreater(result["unique_violating_observations"], 0)
        witness = result["first_witness"]
        self.assertGreater(witness["disk"]["manifest"], witness["disk"]["source"])
        self.assertTrue(replay_witness(program, witness)["verified"])
        bad_seed = explore(program, scheduling="seed", seed_order="consumer_first")
        self.assertGreater(bad_seed["unique_violating_observations"], 0)
        reverse = explore(program, seed_order="consumer_first")
        self.assertEqual(result["recovery_outcomes"], reverse["recovery_outcomes"])

    def test_durability_before_publication_removes_the_failure(self):
        result = explore(self.programs["flush_before_publish"])
        self.assertEqual(result["unique_violating_observations"], 0)
        self.assertEqual(result["no_crash_violations"], 0)

    def test_old_read_and_absent_sink_do_not_invent_failures(self):
        old = explore(self.programs["old_version_consumer"])
        absent = explore(self.programs["no_relevant_sink"])
        self.assertEqual(old["unique_violating_observations"], 0)
        self.assertEqual(absent["unique_violating_observations"], 0)
        self.assertTrue(all(outcome["records"]["manifest"] == 0 for outcome in old["recovery_outcomes"]))

    def test_semantic_recovery_separates_candidates_from_bugs(self):
        logger = self.programs["independent_logger"]
        cache = self.programs["self_validating_cache"]
        self.assertEqual(recover(logger, {"source": 0, "log": 1})[1], ())
        recovered, violations = recover(cache, {"source": 0, "manifest": 1})
        self.assertIsNone(recovered["manifest"])
        self.assertEqual(violations, ())
        self.assertEqual(explore(cache)["unique_violating_observations"], 0)

    def test_ordinary_missing_flush_does_not_require_rescheduling(self):
        result = explore(self.programs["single_process_missing_flush"], scheduling="seed")
        self.assertGreater(result["unique_violating_observations"], 0)

    def test_flush_preserves_prefix_but_not_later_write(self):
        program = Program("flush", (("x", 0),),
                          ((I("write", "x", 1), I("flush", "x"), I("write", "x", 2)),), ())
        state = initial_state(program)
        for _ in range(3):
            state = step(program, state, 0)
        admitted = {disk_image(program, state, versions)["x"]
                    for versions in crash_versions(program, state, "cartesian")}
        self.assertEqual(admitted, {1, 2})
        with self.assertRaises(ValueError):
            disk_image(program, state, (0,))

    def test_extrema_checks_intermediate_not_only_latest_versions(self):
        program = Program("intermediate", (("source", 3), ("manifest", 0)),
                          ((I("write", "source", 1), I("write", "source", 3),
                            I("write", "manifest", 2), I("flush", "manifest")),),
                          (Claim("source", "manifest"),))
        full = explore(program)
        reduced = explore(program, crash_policy="extrema")
        self.assertGreater(full["unique_violating_observations"], 0)
        self.assertGreater(reduced["unique_violating_observations"], 0)
        self.assertEqual(reduced["first_witness"]["disk"]["source"], 1)
        self.assertEqual(full["no_crash_violations"], 0)

    def test_bound_and_resource_cap_cannot_masquerade_as_unbounded_proof(self):
        program = self.programs["publish_before_flush"]
        bounded = explore(program, max_preemptions=0)
        self.assertEqual(bounded["unique_violating_observations"], 0)
        self.assertGreater(bounded["preemption_pruned_branches"], 0)
        with self.assertRaises(ExplorationLimit):
            explore(program, max_prefixes=1)

    def test_deadlock_is_reported_instead_of_a_completed_schedule(self):
        program = Program("blocked", (("x", 0),), ((I("wait", "never"),),), ())
        result = explore(program)
        self.assertEqual(result["complete_schedules"], 0)
        self.assertEqual(result["deadlocked_prefixes"], 1)

    def test_replay_rejects_tampered_evidence(self):
        program = self.programs["publish_before_flush"]
        witness = copy.deepcopy(explore(program)["first_witness"])
        witness["disk"]["source"] = 99
        with self.assertRaises(ValueError):
            replay_witness(program, witness)

    def test_demo_prints_replayed_crash_and_credits_single_trace(self):
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, str(root / "tools/demo.py")],
            cwd=root, capture_output=True, text=True, check=True,
        )
        self.assertIn("consumer: flush manifest", completed.stdout)
        self.assertIn("crash image: source=0, manifest=1", completed.stdout)
        self.assertIn("violated: manifest<=source", completed.stdout)
        self.assertIn("write source -> flush source -> signal ready", completed.stdout)
        self.assertIn("consumer-first single-trace baseline finds the same failure", completed.stdout)

    def test_unsupported_operations_fail_closed(self):
        with self.assertRaises(ValueError):
            Program("mmap", (("x", 0),), ((I("mmap", "x"),),), ())
        with self.assertRaises(ValueError):
            Program("unread", (("x", 0),), ((I("copy", "x", "missing"),),), ())

    def test_bundle_refuses_overwrite_and_detects_artifact_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            run_probe(output)
            self.assertTrue(verify_bundle(output)["verified"])
            original = (output / "report.json").read_bytes()
            with self.assertRaises(FileExistsError):
                run_probe(output)
            self.assertEqual((output / "report.json").read_bytes(), original)
            (output / "report.json").write_bytes(original + b" ")
            with self.assertRaises(ValueError):
                verify_bundle(output)

    def test_failed_probe_preserves_failure_not_success_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "failed"
            with patch.dict(SETTINGS, {"max_prefixes": 1}):
                with self.assertRaises(ExplorationLimit):
                    run_probe(output)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "failed")
            with self.assertRaises(ValueError):
                verify_bundle(output)


if __name__ == "__main__":
    unittest.main()
