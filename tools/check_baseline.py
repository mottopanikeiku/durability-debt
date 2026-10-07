"""Validate the archived research DAG, local links, and original evidence."""
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
# These historical graph outputs were instructions, not result evidence.
# Keep the archived graph intact while accounting for their explicit removal.
RETIRED_PROMPTS = {"AGENTS.md", "NEXT_STEPS.md"}


def check() -> dict:
    graph = json.loads((ROOT / "docs/workflow/graph.json").read_text())
    nodes = {node["id"]: node for node in graph["nodes"]}
    if len(nodes) != len(graph["nodes"]):
        raise ValueError("duplicate graph node")
    visiting, visited, outputs = set(), set(), set()

    def visit(name):
        if name in visiting:
            raise ValueError("dependency cycle")
        if name in visited:
            return
        if name not in nodes:
            raise ValueError(f"unknown prerequisite: {name}")
        node = nodes[name]
        if node["status"] not in {"completed", "pending", "failed", "blocked"}:
            raise ValueError("unknown graph status")
        for field in ("objective", "owner", "inputs", "outputs", "acceptance", "downstream_evidence"):
            if not node.get(field):
                raise ValueError(f"missing {field} in {name}")
        visiting.add(name)
        for predecessor in node["depends_on"]:
            visit(predecessor)
            if node["status"] == "completed" and nodes[predecessor]["status"] != "completed":
                raise ValueError("completed node depends on unaccepted evidence")
        for output in node["outputs"]:
            path = Path(output)
            if path.is_absolute() or ".." in path.parts or output in outputs:
                raise ValueError(f"unsafe or multiply owned output: {output}")
            outputs.add(output)
            if output in RETIRED_PROMPTS:
                continue
            archived = path.parts[0] in {"research", "workflow"}
            location = ROOT / "docs" / path if archived else ROOT / path
            if node["status"] == "completed" and not location.is_file():
                raise ValueError(f"completed output missing: {output}")
        visiting.remove(name)
        visited.add(name)

    for name in nodes:
        visit(name)
    next_node = nodes[graph["next_node"]]
    if next_node["status"] != "pending" or any(nodes[name]["status"] != "completed" for name in next_node["depends_on"]):
        raise ValueError("next research node is not actionable")
    for document in [ROOT / "README.md", ROOT / "AGENTS.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            if not (document.parent / target.split("#", 1)[0]).exists():
                raise ValueError(f"broken local link in {document.name}: {target}")
    manifest = json.loads((ROOT / "results/launch/manifest.json").read_text())
    if manifest["status"] != "completed":
        raise ValueError("original evidence did not complete")
    for filename, digest in manifest["source_sha256"].items():
        if hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() != digest:
            raise ValueError(f"original source evidence is stale: {filename}")
    for filename, digest in manifest["artifacts_sha256"].items():
        if hashlib.sha256((ROOT / "results/launch" / filename).read_bytes()).hexdigest() != digest:
            raise ValueError(f"original artifact changed: {filename}")
    json.loads((ROOT / "docs/research/SOURCES.json").read_text())
    return {"valid": True, "nodes": len(nodes), "completed": sum(node["status"] == "completed" for node in nodes.values()),
            "next_node": graph["next_node"], "scope": "archived research structure and evidence integrity, not current project direction"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
