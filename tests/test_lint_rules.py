"""The fork's own ansible-lint rules (tests/lint_rules), run as CI and Endora's check job run
ansible-lint, against fixtures where each role is one case.

    python3 -m unittest discover -s tests -p 'test_*.py'

Needs ansible-lint on the PATH, pinned as CI pins it (6.14.6).
"""

import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES = HERE / "lint_rules"
FIXTURES = RULES / "fixtures"
REPO = HERE.parent

# `path:line[:column]: [rule] message` or `path:line: rule: message`, as -p prints it.
FINDING = re.compile(r"^(?P<path>[^:\s]+):(?P<line>\d+)(?::\d+)?:\s*\[?(?P<rule>nas-[a-z-]+)\]?")


def findings(where, *args):
    """The nas-* findings of an ansible-lint run, as (path, line, rule)."""
    ran = subprocess.run(
        ["ansible-lint", "--offline", "-p", *args],
        cwd=where,
        capture_output=True,
        text=True,
        check=False,
    )
    found = set()
    for line in (ran.stdout + "\n" + ran.stderr).splitlines():
        match = FINDING.match(line.strip())
        if match:
            found.add((match["path"], int(match["line"]), match["rule"]))
    return found, ran


class TheRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The fixtures' own config: the fork's excludes them from its lint.
        cls.found, cls.ran = findings(
            FIXTURES, "-c", str(FIXTURES / ".ansible-lint"), "-r", str(RULES), "site.yml"
        )

    def of(self, role):
        return {(p, n, r) for p, n, r in self.found if f"/{role}/" in f"/{p}"}

    def test_the_controllers_paths_in_a_role_are_found_line_by_line(self):
        # EL-687: its defaults took the repo, the inventory and the vault from playbook_dir and
        # inventory_file, which under make run-remote are the laptop's.
        path = "roles/controller_paths/defaults/main.yml"
        self.assertEqual(
            self.of("controller_paths"),
            {(path, 3, "nas-controller-path"), (path, 4, "nas-controller-path"),
             (path, 5, "nas-controller-path")},
            self.ran.stdout + self.ran.stderr,
        )

    def test_a_playbook_run_on_the_nas_as_root_is_found(self):
        # EL-687: a timer's unit with no User= ran the playbook as root, which cannot load the
        # collections installed for the playbook's own user.
        self.assertEqual(
            self.of("playbook_as_root"),
            {("roles/playbook_as_root/templates/run.sh.j2", 4, "nas-playbook-user")},
            self.ran.stdout + self.ran.stderr,
        )

    def test_a_playbook_run_as_its_own_user_passes(self):
        self.assertEqual(self.of("playbook_as_user"), set(), self.ran.stdout + self.ran.stderr)

    def test_an_exemption_says_why_and_is_kept_to_its_line(self):
        self.assertEqual(self.of("exempted"), set(), self.ran.stdout + self.ran.stderr)

    def test_a_role_scheduling_a_job_of_its_own_is_found(self):
        # The gluetun stack's 2-hourly restart ran from a timer of its own role, and nobody
        # could say what ran on the NAS by itself, or why (#796): every scheduled job on the
        # host is one of nas_maintenance's, listed with its reason.
        self.assertEqual(
            self.of("own_timer") | self.of("own_cron"),
            {("roles/own_timer/templates/app-sweep.timer.j2", 1, "nas-scheduled-job"),
             ("roles/own_cron/tasks/main.yml", 3, "nas-scheduled-job")},
            self.ran.stdout + self.ran.stderr,
        )

    def test_the_nas_scheduled_jobs_are_nas_maintenances(self):
        self.assertEqual(self.of("nas_maintenance"), set(), self.ran.stdout + self.ran.stderr)

    def test_a_comment_or_another_variable_is_not_a_finding(self):
        self.assertEqual(self.of("clean"), set(), self.ran.stdout + self.ran.stderr)


class TheFork(unittest.TestCase):
    def test_nas_yml_has_no_finding_of_these_rules(self):
        # As CI runs it: the repository's own .ansible-lint, which loads the rules.
        found, ran = findings(REPO, "nas.yml")
        self.assertEqual(found, set(), ran.stdout[-3000:] + ran.stderr[-3000:])


    def test_the_vpn_download_stack_is_worked_out_on_every_run(self):
        # vpn-download-stack only sets facts other roles read: whether gluetun is on and which
        # containers it routes. Run under one tag (nas_maintenance), the gluetun job was built
        # without them and would have restarted sonarr with the stack every 2 hours.
        import yaml

        play = yaml.safe_load((REPO / "nas.yml").read_text(encoding="utf-8"))[0]
        tags = next(r["tags"] for r in play["roles"] if r.get("role") == "vpn-download-stack")
        self.assertIn("always", tags)


if __name__ == "__main__":
    unittest.main()
