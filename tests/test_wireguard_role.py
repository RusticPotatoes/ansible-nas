"""The wireguard role honours its documented settings: wireguard_udp_port sets the published
port and the server port in the peer configs, wireguard_allowed_ips sets the peers' allowed IPs.

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import unittest
from pathlib import Path

import yaml

ROLE = Path(__file__).resolve().parent.parent / "roles" / "wireguard"


def container_task():
    tasks = yaml.safe_load((ROLE / "tasks" / "main.yml").read_text())
    block = next(t for t in tasks if "block" in t)["block"]
    return next(t for t in block if t.get("name") == "Create WireGuard Docker Container")


class WireGuardRoleSettings(unittest.TestCase):
    def setUp(self):
        self.task = container_task()["community.docker.docker_container"]
        self.defaults = yaml.safe_load((ROLE / "defaults" / "main.yml").read_text())

    def test_published_port_comes_from_udp_port_setting(self):
        self.assertEqual(self.task["ports"], ["{{ wireguard_udp_port }}:51820/udp"])

    def test_peer_configs_get_server_port_from_udp_port_setting(self):
        self.assertEqual(self.task["env"]["SERVERPORT"], "{{ wireguard_udp_port }}")

    def test_allowed_ips_come_from_setting(self):
        self.assertEqual(self.task["env"]["ALLOWEDIPS"], "{{ wireguard_allowed_ips }}")

    def test_defaults_are_todays_values(self):
        self.assertEqual(str(self.defaults["wireguard_udp_port"]), "51820")
        self.assertEqual(self.defaults["wireguard_allowed_ips"], "0.0.0.0/0")


if __name__ == "__main__":
    unittest.main()
