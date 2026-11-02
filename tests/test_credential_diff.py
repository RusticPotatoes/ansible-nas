"""Tasks that write a credential into a file on the NAS keep its content out of --diff.

    python3 -m unittest discover -s tests -p 'test_*.py'

`make run` does a --check --diff dry run first; the diff of a file that holds a password,
token or key prints it on the terminal. Each task below writes such a file, so it carries
no_log: true. Every other file-writing task in roles/ keeps its diff.
"""

import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLES = REPO / "roles"
FILE_MODULES = {
    "template",
    "copy",
    "lineinfile",
    "blockinfile",
    "ansible.builtin.template",
    "ansible.builtin.copy",
    "ansible.builtin.lineinfile",
    "ansible.builtin.blockinfile",
}
# A templated value whose name says it is a credential.
CREDENTIAL_VAR = re.compile(r"password|passwd|token|api_?key|secret|_pass\b|bcrypt", re.I)
TEMPLATED = re.compile(r"\{\{.*?\}\}")

# Tasks whose file holds a credential the name pattern cannot see: a whole config document
# built from one variable (ddns_updater), and a bcrypt password hash shipped in files/.
KNOWN = {
    ("backrest", "Seed Backrest config (only if none exists)"),
    ("cloudflare_ddns", "Template Cloudflare Dynamic DNS config.yml with scoped token"),
    ("ddns_updater", "Generate config.json"),
    ("gatus", "Create Gatus config"),
    ("loki", "Template Loki config"),
    ("route53_ddns", "Generate AWS Route53 Dynamic DNS config file"),
    ("stats", "Template Grafana contact points"),
    ("stats", "Template Prometheus config"),
    ("thelounge", "Set up admin user"),
    ("virtual_desktop", "Create users file"),
    ("znc", "Template Znc config"),
}


def file_tasks():
    """Yield (role, task_file, task) for every file-writing task under roles/, blocks included."""
    for path in sorted(ROLES.glob("*/tasks/*.yml")):
        role = path.parts[-3]
        data = yaml.safe_load(path.read_text()) or []

        def walk(tasks):
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                if "block" in task:
                    yield from walk(task["block"])
                    continue
                if any(module in task for module in FILE_MODULES):
                    yield role, path, task

        yield from walk(data)


def module_args(task):
    return next(task[module] for module in FILE_MODULES if module in task)


def looks_credential(role, path, task):
    """True when the text the task writes names a credential variable."""
    args = module_args(task)
    text = str(args.get("content", ""))
    src = args.get("src")
    if src and "{{" not in str(src):
        for folder in ("templates", "files"):
            source = ROLES / role / folder / src
            if source.exists():
                text += source.read_text()
                break
    return any(CREDENTIAL_VAR.search(expr) for expr in TEMPLATED.findall(text)) or bool(
        re.search(r"\$2[aby]\$", text)
    )


class CredentialDiffTest(unittest.TestCase):
    def test_credential_files_have_no_log(self):
        missing = []
        for role, path, task in file_tasks():
            if (role, task.get("name")) in KNOWN and task.get("no_log") is not True:
                missing.append(f"{path.relative_to(REPO)}: {task.get('name')}")
        self.assertEqual([], missing, "credential files whose diff is not hidden")

    def test_no_unlisted_credential_file(self):
        unlisted = []
        for role, path, task in file_tasks():
            if (role, task.get("name")) not in KNOWN and looks_credential(role, path, task):
                unlisted.append(f"{path.relative_to(REPO)}: {task.get('name')}")
        self.assertEqual([], unlisted, "file tasks that name a credential but are not in KNOWN")

    def test_other_file_tasks_keep_their_diff(self):
        hidden = []
        for role, path, task in file_tasks():
            if (role, task.get("name")) not in KNOWN and task.get("no_log"):
                hidden.append(f"{path.relative_to(REPO)}: {task.get('name')}")
        self.assertEqual([], hidden, "non-credential file tasks whose diff is hidden")


if __name__ == "__main__":
    unittest.main()
