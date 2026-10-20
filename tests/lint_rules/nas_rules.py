"""The fork's own ansible-lint rules: how this fork reaches the NAS, which a role's files cannot
show (see AGENTS.md, "How a change reaches the NAS"). Loaded through `rulesdir` in
.ansible-lint, so CI and Endora's check job run them with the rest; tested in
tests/test_lint_rules.py.

Each rule looks at a role once, when ansible-lint reaches its tasks/main.yml, and reads the
role's own files. A line is exempted, with a reason, by `noqa: <rule>` on it or on the line
above it.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.errors import MatchError

# A Jinja reference to one of the controller's paths: `{{ ... playbook_dir ... }}`.
CONTROLLER_PATH = re.compile(r"\{\{[^}]*?\b(playbook_dir|inventory_file|inventory_dir)\b")
# A command line that runs the playbook (not a comment): `ansible-playbook ...`, also by path.
RUNS_THE_PLAYBOOK = re.compile(r"^\s*(?:exec\s+)?(?:\S*/)?ansible-playbook(?:\s|$)")
# A systemd unit that says whose it is.
UNIT_USER = re.compile(r"^\s*User\s*=", re.MULTILINE)


def role_of(file: Lintable) -> Path | None:
    """The role whose tasks/main.yml this is, if it is one."""
    path = Path(str(file.path))
    if path.name not in ("main.yml", "main.yaml") or path.parent.name != "tasks":
        return None
    return path.parent.parent


def files_of(role: Path, folders: tuple[str, ...]) -> list[Path]:
    """The role's files in these folders, in a stable order."""
    found: list[Path] = []
    for folder in folders:
        where = role / folder
        if where.is_dir():
            found.extend(p for p in sorted(where.rglob("*")) if p.is_file())
    return found


def lines_of(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def exempted(lines: list[str], index: int, rule: str) -> bool:
    """`noqa: <rule>` on the line, or on the line above it."""
    marker = f"noqa: {rule}"
    return marker in lines[index] or (index > 0 and marker in lines[index - 1])


class NasControllerPathRule(AnsibleLintRule):
    """A role takes a path from the controller for something that lives on the NAS."""

    id = "nas-controller-path"
    shortdesc = "The controller's path baked into the NAS"
    description = (
        "playbook_dir, inventory_file and inventory_dir are paths on the machine that runs "
        "the playbook. The owner runs it from a laptop (make run-remote), so a value taken from "
        "them and written onto the NAS points at the laptop. Use the NAS's own path "
        "(AGENTS.md, How a change reaches the NAS)."
    )
    severity = "HIGH"
    tags = ["nas"]
    version_added = "fork"

    def matchyaml(self, file: Lintable) -> list[MatchError]:
        role = role_of(file)
        if role is None:
            return []
        found: list[MatchError] = []
        for path in files_of(role, ("defaults", "vars", "templates", "files")):
            lines = lines_of(path)
            for index, line in enumerate(lines):
                if line.lstrip().startswith("#") or not CONTROLLER_PATH.search(line):
                    continue
                if exempted(lines, index, self.id):
                    continue
                found.append(
                    self.create_matcherror(
                        message=f"{CONTROLLER_PATH.search(line).group(1)} is the controller's "
                        "path, not the NAS's",
                        linenumber=index + 1,
                        filename=Lintable(str(path), kind="vars"),
                    )
                )
        return found


class NasPlaybookUserRule(AnsibleLintRule):
    """A role runs the playbook on the NAS from a unit that does not say whose it is."""

    id = "nas-playbook-user"
    shortdesc = "The playbook run on the NAS as root"
    description = (
        "A role that runs ansible-playbook on the NAS (from a timer or a script) runs it as root "
        "unless its systemd unit sets User=. The collections and roles are installed for the "
        "playbook's own user, so as root it cannot load them. Set User= to that user "
        "(AGENTS.md, How a change reaches the NAS)."
    )
    severity = "HIGH"
    tags = ["nas"]
    version_added = "fork"

    def matchyaml(self, file: Lintable) -> list[MatchError]:
        role = role_of(file)
        if role is None:
            return []
        everything = files_of(role, ("tasks", "templates", "files"))
        if any(UNIT_USER.search("\n".join(lines_of(path))) for path in everything):
            return []
        found: list[MatchError] = []
        for path in files_of(role, ("templates", "files")):
            lines = lines_of(path)
            for index, line in enumerate(lines):
                if not RUNS_THE_PLAYBOOK.search(line) or exempted(lines, index, self.id):
                    continue
                found.append(
                    self.create_matcherror(
                        message="ansible-playbook runs on the NAS from a unit with no User=",
                        linenumber=index + 1,
                        filename=Lintable(str(path), kind="vars"),
                    )
                )
        return found
