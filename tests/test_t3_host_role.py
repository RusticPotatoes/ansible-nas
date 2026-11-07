"""The t3_host role: makes a machine a T3 Code remote that can run Claude, Codex and Antigravity.

    python3 -m unittest discover -s tests -p 'test_*.py'

T3 Code's desktop app already puts its own server on a remote over SSH. What it can't do is
install the agents' command-line tools, or turn on a provider that is off by default
(Antigravity). The role does both, as the remote's user: each tool's official installer drops
one binary in ~/.local/bin, so nothing needs root.
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "t3_host"


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


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.tasks = tasks_of(load(ROLE / "tasks" / "main.yml"))
        cls.playbook = load(REPO / "t3.yml")

    def test_every_variable_is_named_for_the_role(self):
        for name in self.defaults:
            self.assertTrue(name.startswith("t3_"), name)

    def test_it_installs_the_three_agents_with_their_official_installers(self):
        clis = {c["name"]: c for c in self.defaults["t3_clis"]}
        self.assertEqual(set(clis), {"claude", "codex", "agy"})
        self.assertEqual(clis["claude"]["installer"], "https://claude.ai/install.sh")
        self.assertEqual(clis["codex"]["installer"], "https://chatgpt.com/codex/install.sh")
        self.assertEqual(clis["agy"]["installer"], "https://antigravity.google/cli/install.sh")
        for cli in clis.values():
            self.assertIn(cli["provider"], {"claudeAgent", "codex", "antigravity"})

    def test_an_installed_agent_is_not_reinstalled(self):
        runs = [t for t in self.tasks if "ansible.builtin.command" in t
                and "installer" in str(t["ansible.builtin.command"])]
        self.assertEqual(len(runs), 1)
        self.assertIn("creates", runs[0]["args"])

    def test_nothing_runs_as_root(self):
        self.assertFalse(any(t.get("become") for t in self.tasks))
        play = self.playbook[0]
        self.assertFalse(play.get("become", False))

    def test_it_turns_the_providers_on_without_dropping_other_settings(self):
        writes = [t for t in self.tasks if "ansible.builtin.copy" in t
                  and "settings.json" in str(t["ansible.builtin.copy"].get("dest"))]
        self.assertEqual(len(writes), 1)
        self.assertIn("combine", writes[0]["ansible.builtin.copy"]["content"])
        self.assertIn("recursive=True", writes[0]["ansible.builtin.copy"]["content"])

    def test_the_playbook_targets_its_own_group(self):
        self.assertEqual(self.playbook[0]["hosts"], "t3")
        self.assertEqual(self.playbook[0]["roles"][0]["role"], "t3_host")


if __name__ == "__main__":
    unittest.main()
