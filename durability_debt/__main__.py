"""Dependency-free command line for the finite reference artifact."""
import argparse
import json
from pathlib import Path
import sys

from .probe import run_probe, verify_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    probe = commands.add_parser("probe", help="run bounded finite experiments into a new directory")
    probe.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify", help="check a completed bundle for checkpoint reuse")
    verify.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "verify":
            print(json.dumps(verify_bundle(args.directory), indent=2))
            return 0
        report = run_probe(args.output)
        print(json.dumps({"passed": report["passed"], "scope": report["scope"],
                          "decision": report["decision"], "gates": report["gates"],
                          "bundle": str(args.output)}, indent=2))
        return 0 if report["passed"] else 1
    except (OSError, ValueError, RuntimeError) as error:
        print(f"durability-debt: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
