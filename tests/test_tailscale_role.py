"""The tailscale role, run by t3.yml: puts each T3 Code remote on the owner's tailnet, so
another T3 Code can link it over HTTPS (T3's own `tailscale serve`) instead of plain http.

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "tailscale"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.tasks = load(ROLE / "tasks" / "main.yml")
        cls.play = load(REPO / "t3.yml")[0]

    def test_every_variable_is_named_for_the_role(self):
        for name in self.defaults:
            self.assertTrue(name.startswith("tailscale_"), name)

    def test_it_is_off_unless_asked(self):
        self.assertIs(self.defaults["tailscale_enabled"], False)
        entry = [r for r in self.play["roles"] if r["role"] == "tailscale"][0]
        self.assertIn("tailscale_enabled", entry["when"])
        self.assertTrue(entry["become"])

    def test_it_installs_from_tailscales_own_signed_apt_source(self):
        text = (ROLE / "tasks" / "main.yml").read_text()
        self.assertIn("pkgs.tailscale.com/stable/ubuntu", text)
        self.assertIn("signed-by=", text)

    def test_the_user_may_configure_serve_so_t3_can_publish_itself(self):
        text = (ROLE / "tasks" / "main.yml").read_text()
        self.assertIn("--operator=", text)

    def test_it_joins_with_a_key_only_when_given_one_and_never_logs_it(self):
        joins = [t for t in self.tasks if "tailscale up" in str(t.get("ansible.builtin.command", ""))]
        self.assertEqual(len(joins), 1)
        self.assertIn("tailscale_auth_key", str(joins[0]["when"]))
        self.assertTrue(joins[0]["no_log"])

    def test_the_t3_play_finds_the_classic_sudo_like_the_builders_play(self):
        names = [t["name"] for t in self.play.get("pre_tasks", [])]
        self.assertIn("Find the classic sudo", names)


if __name__ == "__main__":
    unittest.main()
