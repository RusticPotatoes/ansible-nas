"""The build_host role and builders.yml: Docker and Rust on a machine that builds for others.

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "build_host"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.tasks = load(ROLE / "tasks" / "main.yml")
        cls.play = load(REPO / "builders.yml")[0]

    def test_every_variable_is_named_for_the_role(self):
        for name in self.defaults:
            self.assertTrue(name.startswith("build_host_"), name)

    def test_docker_comes_from_the_pinned_role_with_the_user_in_its_group(self):
        docker = self.play["roles"][0]
        self.assertEqual(docker["role"], "geerlingguy.docker")
        self.assertTrue(docker["become"])
        self.assertIn("{{ ansible_user_id }}", docker["vars"]["docker_users"])
        gc = docker["vars"]["docker_daemon_options"]["builder"]["gc"]
        self.assertTrue(gc["enabled"])

    def test_rust_is_installed_for_the_user_once(self):
        rust = [t for t in self.tasks if "rustup-init" in str(t.get("ansible.builtin.command", ""))]
        self.assertEqual(len(rust), 1)
        self.assertNotIn("become", rust[0])
        self.assertIn("creates", rust[0]["ansible.builtin.command"])

    def test_only_the_apt_packages_need_root(self):
        root = [t["name"] for t in self.tasks if t.get("become")]
        self.assertEqual(root, ["Install the native build tools"])

    def test_the_play_targets_the_builders_group(self):
        self.assertEqual(self.play["hosts"], "builders")


if __name__ == "__main__":
    unittest.main()
