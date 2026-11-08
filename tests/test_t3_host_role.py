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

    def test_the_play_runs_as_the_user(self):
        play = self.playbook[0]
        self.assertFalse(play.get("become", False))

    def test_it_turns_the_providers_on_without_dropping_other_settings(self):
        writes = [t for t in self.tasks if "ansible.builtin.copy" in t
                  and "settings.json" in str(t["ansible.builtin.copy"].get("dest"))]
        self.assertEqual(len(writes), 1)
        self.assertIn("combine", writes[0]["ansible.builtin.copy"]["content"])
        self.assertIn("recursive=True", writes[0]["ansible.builtin.copy"]["content"])

    def test_it_installs_node_lts_for_the_user_checked_by_checksum(self):
        self.assertTrue(self.defaults["t3_node_version"].startswith("24."))
        self.assertEqual(set(self.defaults["t3_node_sha256"]), {"x64", "arm64"})
        fetch = [t for t in self.tasks if "ansible.builtin.get_url" in t
                 and "nodejs.org" in t["ansible.builtin.get_url"]["url"]]
        self.assertEqual(len(fetch), 1)
        self.assertIn("checksum", fetch[0]["ansible.builtin.get_url"])
        links = [t for t in self.tasks if "ansible.builtin.file" in t
                 and t["ansible.builtin.file"].get("state") == "link"]
        self.assertEqual(links[0]["loop"], ["node", "npm", "npx"])

    def test_the_service_finds_the_agents_and_only_linger_needs_root(self):
        by_name = {t.get("name"): t for t in self.tasks}
        path = [t for t in self.tasks if "ansible.builtin.copy" in t
                and "path.conf" in str(t["ansible.builtin.copy"]["dest"])]
        self.assertEqual(len(path), 1)
        self.assertIn("{{ t3_bin_directory }}", path[0]["ansible.builtin.copy"]["content"])
        root = [n for n, t in by_name.items() if t.get("become")]
        self.assertEqual(len(root), 1)
        self.assertIn("enable-linger", by_name[root[0]]["ansible.builtin.command"]["cmd"])
        self.assertIn("t3_host_sudo", by_name[root[0]]["tags"])

    def test_lan_access_is_off_unless_asked_and_set_through_the_service_env(self):
        self.assertIs(self.defaults["t3_lan"], False)
        env = [t for t in self.tasks if "ansible.builtin.lineinfile" in t
               and "service.env" in str(t["ansible.builtin.lineinfile"]["path"])]
        self.assertEqual(len(env), 1)
        line = env[0]["ansible.builtin.lineinfile"]
        self.assertEqual(line["regexp"], "^T3CODE_LAN=")
        self.assertIn("t3_lan", line["line"])
        self.assertEqual(env[0]["notify"], "Restart T3 Code")

    def test_the_playbook_targets_its_own_group(self):
        self.assertEqual(self.playbook[0]["hosts"], "t3")
        self.assertEqual(self.playbook[0]["roles"][0]["role"], "t3_host")


if __name__ == "__main__":
    unittest.main()
