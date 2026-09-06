"""Run the selection probe and bind its evidence to inputs and source."""
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from .cases import cases
from .explore import explore


SCHEMA = "durability-debt-probe/1"
SETTINGS = {"max_preemptions": 2, "max_prefixes": 50_000, "max_crash_evaluations": 250_000}


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write(path: Path, value: dict) -> str:
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)
    return _digest(data)


def _source() -> dict[str, str]:
    root = Path(__file__).parent
    return {f"durability_debt/{path.name}": _digest(path.read_bytes()) for path in sorted(root.glob("*.py"))}


def _environment() -> dict[str, str]:
    return {"python": sys.version, "platform": platform.platform(), "implementation": platform.python_implementation()}


def run_probe(output: Path) -> dict:
    # Refusal happens before any write to an existing run, including a failed
    # run. Choose another path for a rerun; never mix evidence bundles.
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"schema": SCHEMA, "started_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": _source(), "environment": _environment(), "artifacts_sha256": {}}
    try:
        programs = cases()
        inputs = {"schema": SCHEMA, "settings": SETTINGS, "programs": [asdict(program) for program in programs]}
        manifest["artifacts_sha256"]["inputs.json"] = _write(output / "inputs.json", inputs)
        results = {}
        for program in programs:
            results[program.name] = {
                "seed_cartesian": explore(program, scheduling="seed", **SETTINGS),
                "bad_seed_cartesian": explore(program, scheduling="seed", seed_order="consumer_first", **SETTINGS),
                "joint_cartesian": explore(program, **SETTINGS),
                "reversed_joint_cartesian": explore(program, seed_order="consumer_first", **SETTINGS),
                "joint_extrema": explore(program, crash_policy="extrema", **SETTINGS),
            }
        def fails(case: str, policy: str = "joint_cartesian") -> bool:
            return bool(results[case][policy]["unique_violating_observations"])
        gates = {
            "seed_schedule_hides_race": not fails("publish_before_flush", "seed_cartesian"),
            "joint_schedule_exposes_race": fails("publish_before_flush"),
            "bad_seed_baseline_gets_full_credit": fails("publish_before_flush", "bad_seed_cartesian"),
            "joint_outcomes_are_seed_order_invariant": all(
                policies["joint_cartesian"]["recovery_outcomes"]
                == policies["reversed_joint_cartesian"]["recovery_outcomes"]
                for policies in results.values()),
            "durable_handoff_prevents_violation": not fails("flush_before_publish"),
            "old_version_consumer_is_allowed": not fails("old_version_consumer"),
            "no_sink_means_no_cross_resource_violation": not fails("no_relevant_sink"),
            "independent_logger_is_not_a_bug": not fails("independent_logger"),
            "invalid_cache_is_discarded": not fails("self_validating_cache"),
            "ordinary_missing_flush_is_found_by_seed": fails("single_process_missing_flush", "seed_cartesian"),
            "extrema_matches_existence_oracle": all(
                fails(name) == fails(name, "joint_extrema") for name in results),
            "no_crash_controls_pass": all(
                result["no_crash_violations"] == 0 for policies in results.values() for result in policies.values()),
            "all_cases_terminate_without_deadlock": all(
                result["complete_schedules"] > 0 and result["deadlocked_prefixes"] == 0
                for policies in results.values() for result in policies.values()),
        }
        report = {
            "schema": SCHEMA, "scope": "finite independent atomic-record model only",
            "decision": "mechanism sanity only; novelty and native feasibility remain open",
            "gates": gates, "passed": all(gates.values()), "results": results,
        }
        manifest["artifacts_sha256"]["report.json"] = _write(output / "report.json", report)
        manifest["status"] = "completed" if report["passed"] else "gate_failed"
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        _write(output / "manifest.json", manifest)
        return report
    except BaseException as error:
        if not (output / "manifest.json").exists():
            manifest["status"] = "failed"
            manifest["error"] = {"type": type(error).__name__, "message": str(error)}
            manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
            _write(output / "manifest.json", manifest)
        raise


def verify_bundle(output: Path) -> dict:
    """Check accidental drift and checkpoint reuse, not signed authenticity."""
    manifest = json.loads((output / "manifest.json").read_text())
    if manifest.get("schema") != SCHEMA or manifest.get("status") != "completed":
        raise ValueError("bundle is not a completed compatible checkpoint")
    if manifest.get("source_sha256") != _source():
        raise ValueError("source changed; rerun instead of reusing this checkpoint")
    if manifest.get("environment") != _environment():
        raise ValueError("environment changed; checkpoint is historical, not reusable here")
    artifacts = manifest.get("artifacts_sha256", {})
    if set(artifacts) != {"inputs.json", "report.json"}:
        raise ValueError("bundle artifact set is incomplete or unexpected")
    for filename, expected in artifacts.items():
        if _digest((output / filename).read_bytes()) != expected:
            raise ValueError(f"artifact hash mismatch: {filename}")
    expected_inputs = {"schema": SCHEMA, "settings": SETTINGS, "programs": [asdict(program) for program in cases()]}
    # Round-trip tuple fields to their serialized list representation.
    if json.loads((output / "inputs.json").read_text()) != json.loads(json.dumps(expected_inputs)):
        raise ValueError("inputs/settings changed; checkpoint is not reusable")
    report = json.loads((output / "report.json").read_text())
    if report.get("passed") is not True or not report.get("gates") or not all(report["gates"].values()):
        raise ValueError("probe gates did not pass")
    return {"verified": True, "scope": report["scope"], "authentication": "not provided"}
