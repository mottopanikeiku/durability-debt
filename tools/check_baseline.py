"""Validate local documentation links and original source/artifact hashes."""
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def check() -> dict:
    for document in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            if not (document.parent / target.split("#", 1)[0]).exists():
                raise ValueError(f"broken local link in {document.name}: {target}")
    manifest = json.loads((ROOT / "results/launch/manifest.json").read_text())
    if manifest["status"] != "completed":
        raise ValueError("original evidence did not complete")
    for filename, digest in manifest["source_sha256"].items():
        if not (ROOT / filename).is_file():
            raise ValueError(f"original source missing: {filename}")
        if hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() != digest:
            raise ValueError(f"original source evidence is stale: {filename}")
    for filename, digest in manifest["artifacts_sha256"].items():
        if hashlib.sha256((ROOT / "results/launch" / filename).read_bytes()).hexdigest() != digest:
            raise ValueError(f"original artifact changed: {filename}")
    json.loads((ROOT / "docs/research/SOURCES.json").read_text())
    return {"valid": True, "scope": "local documentation links and original source/artifact hashes"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
