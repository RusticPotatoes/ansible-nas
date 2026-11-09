"""The agent_workspace role: gives a T3 Code remote its agents' workspace, only through the play.

    python3 -m unittest discover -s tests -p 'test_*.py'

The owner's rule: every tool, clone, key and file on those machines comes from the Ansible play,
never a hand edit over SSH and never T3's own clone tool. These tests pin that behaviour down:
the role is off by default, keys are per machine and per repo and registered from the laptop,
read-only repos cannot be pushed to, the seed of private state happens once and never carries
credentials.
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "agent_workspace"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def tasks_of(blocks):
    out = []
    for t in blocks or []:
        if "block" in t:
            out.extend(tasks_of(t["block"]))
        else:
            out.append(t)
    return out


def text(name):
    return (ROLE / "tasks" / name).read_text()


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.top = load(ROLE / "tasks" / "main.yml")
        cls.main = tasks_of(cls.top)
        cls.key = tasks_of(load(ROLE / "tasks" / "deploy_key.yml"))
        cls.play = load(REPO / "t3.yml")[0]

    def test_every_variable_is_named_for_the_role(self):
        for name in self.defaults:
            self.assertTrue(name.startswith("agent_workspace_"), name)

    def test_it_is_off_unless_asked_and_runs_after_t3_host(self):
        self.assertIs(self.defaults["agent_workspace_enabled"], False)
        roles = [r["role"] for r in self.play["roles"]]
        self.assertLess(roles.index("t3_host"), roles.index("agent_workspace"))
        entry = self.play["roles"][roles.index("agent_workspace")]
        self.assertIn("agent_workspace_enabled", entry["when"])

    def test_no_personal_value_is_tracked(self):
        self.assertEqual(self.defaults["agent_workspace_repos"], [])
        self.assertEqual(self.defaults["agent_workspace_git_email"], "")
        self.assertFalse(self.defaults["agent_workspace_seed_local_state"])

    def test_gh_comes_from_githubs_own_signed_apt_source(self):
        body = text("main.yml")
        self.assertIn("cli.github.com/packages", body)
        self.assertIn("signed-by=", body)

    def test_github_host_keys_are_pinned_not_trusted_on_first_use(self):
        keys = self.defaults["agent_workspace_github_host_keys"]
        self.assertTrue(any(k.startswith("ssh-ed25519 ") for k in keys))
        self.assertNotIn("ssh-keyscan", text("main.yml"))

    def test_keys_are_generated_on_the_host_and_registered_from_the_laptop(self):
        generate = [t for t in self.key if "ssh-keygen" in str(t.get("ansible.builtin.command", ""))]
        self.assertEqual(len(generate), 1)
        self.assertIn("creates", generate[0]["ansible.builtin.command"])
        gh = [t for t in self.key if "gh" in str(t.get("ansible.builtin.command", ""))]
        self.assertGreaterEqual(len(gh), 2)
        for t in gh:
            self.assertEqual(t["delegate_to"], "localhost")
            self.assertFalse(t.get("become", False))

    def test_a_key_is_registered_once_per_title_and_read_only_follows_the_repo(self):
        body = text("deploy_key.yml")
        self.assertEqual(self.defaults["agent_workspace_key_title"], "t3-{{ inventory_hostname }}")
        self.assertIn("read_only", body)
        post = [t for t in self.key if "POST" in str(t.get("ansible.builtin.command", ""))][0]
        self.assertIn("when", post)

    def test_a_read_only_repo_cannot_be_pushed_to(self):
        body = text("main.yml")
        self.assertIn("disabled://reader", body)
        self.assertIn("pushurl", body)

    def test_the_clone_only_fast_forwards_and_never_clobbers(self):
        clone = [t for t in self.main if "ansible.builtin.git" in t][0]["ansible.builtin.git"]
        self.assertIs(clone["update"], True)
        self.assertIs(clone["force"], False)

    def test_the_updater_is_an_hourly_user_timer(self):
        body = text("main.yml")
        self.assertIn("OnUnitActiveSec=1h", (ROLE / "templates" / "agent-config-update.timer.j2").read_text())
        self.assertIn("scripts/update.sh", (ROLE / "templates" / "agent-config-update.service.j2").read_text())
        self.assertIn("scope: user", body)

    def test_the_seed_is_once_only_gated_and_leaves_out_credentials(self):
        seed = [t for t in self.top if "block" in t and "ansible.posix.synchronize" in str(t["block"])]
        self.assertEqual(len(seed), 1)
        self.assertIn("agent_workspace_seed_local_state", str(seed[0]["when"]))
        self.assertIn("marker", str(seed[0]["when"]))
        seed = [t for t in self.main if "ansible.posix.synchronize" in t]
        excluded = " ".join(self.defaults["agent_workspace_seed_exclude"])
        for name in ("mac-rebuild", ".claude", ".codex", ".t3"):
            self.assertIn(name, excluded)
        self.assertIs(seed[0]["ansible.posix.synchronize"]["delete"], False)


class ADryRun(unittest.TestCase):
    def test_starting_the_timer_does_not_fail_before_its_unit_exists(self):
        tasks = tasks_of(load(ROLE / "tasks" / "main.yml"))
        start = [t for t in tasks if t.get("name") == "Keep the timer running"]
        self.assertEqual(len(start), 1)
        self.assertEqual(start[0].get("ignore_errors"), "{{ ansible_check_mode }}")

    def test_a_failed_or_changed_timer_is_restarted_not_only_reloaded(self):
        # A timer whose service could not be queued goes `failed` with no next run; only a start or
        # restart repairs it (checked on systemd 259), and a changed unit needs a restart as well.
        tasks = tasks_of(load(ROLE / "tasks" / "main.yml"))
        repair = [t for t in tasks if t.get("name") == "Restart the timer when it has failed or stopped"]
        self.assertEqual(len(repair), 1)
        self.assertEqual(repair[0]["ansible.builtin.systemd_service"]["state"], "restarted")
        self.assertIn("ActiveState", repair[0]["when"])
        write = [t for t in tasks if t.get("name") == "Write the updater's service and timer"][0]
        handlers = load(ROLE / "handlers" / "main.yml")
        self.assertEqual(write["notify"], handlers[0]["name"])
        self.assertEqual(handlers[0]["ansible.builtin.systemd_service"]["state"], "restarted")
        self.assertEqual(handlers[0]["ansible.builtin.systemd_service"]["name"], "agent-config-update.timer")


if __name__ == "__main__":
    unittest.main()
