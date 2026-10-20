"""Check isolated project installations without contacting WorkMedow."""

import argparse
import hashlib
import json
import re
from pathlib import Path


def verify(source: Path, project: Path) -> dict:
    source = source.resolve(strict=True)
    project = project.resolve(strict=True)
    if source == project or project.is_relative_to(source):
        raise ValueError("Use a separate temporary project for the installation.")

    required = {"SKILL.md", "agents/openai.yaml"}
    body = (source / "SKILL.md").read_text()
    for target in re.findall(r"\]\(([^\s)]+)\)", body):
        if ":" in target or target.startswith("#"):
            continue
        relative = target.split("#", 1)[0]
        resolved = (source / relative).resolve(strict=True)
        if not resolved.is_relative_to(source) or not resolved.is_file():
            raise ValueError("A Skill reference must resolve inside the source.")
        required.add(relative)

    targets = {
        "codex": project / ".agents/skills/workmedow",
        "openclaw": project / "skills/workmedow",
    }
    for host, root in targets.items():
        if root.is_symlink() or not root.resolve(strict=True).is_relative_to(project):
            raise ValueError(f"{host} installation escaped the temporary project.")
        for relative in sorted(required):
            origin, installed = source / relative, root / relative
            if origin.is_symlink() or installed.is_symlink():
                raise ValueError("The copy-mode smoke test must use regular files.")
            if origin.read_bytes() != installed.read_bytes():
                raise ValueError(f"{host}: incomplete or changed file {relative}")

    return {
        "project_scope": True,
        "hosts": list(targets),
        "files_per_host": sorted(required),
        "skill_sha256": hashlib.sha256((source / "SKILL.md").read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--project", required=True, type=Path)
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.source, arguments.project), indent=2))
