import unittest
from pathlib import Path

import yaml

ROLE = Path(__file__).resolve().parent.parent / "roles" / "wireguard"


def container_task():
    tasks = yaml.safe_load((ROLE / "tasks" / "main.yml").read_text())
    block = tasks[0]["block"]
    return next(t["community.docker.docker_container"] for t in block
                if "community.docker.docker_container" in t)


class TheWireguardRole(unittest.TestCase):
    def test_the_published_udp_port_comes_from_wireguard_udp_port(self):
        self.assertEqual(container_task()["ports"], ["{{ wireguard_udp_port }}:51820/udp"])

    def test_the_server_port_for_peer_configs_comes_from_wireguard_udp_port(self):
        self.assertEqual(container_task()["env"]["SERVERPORT"], "{{ wireguard_udp_port }}")

    def test_the_allowed_ips_come_from_wireguard_allowed_ips(self):
        self.assertEqual(container_task()["env"]["ALLOWEDIPS"], "{{ wireguard_allowed_ips }}")

    def test_the_defaults_keep_port_51820_and_all_traffic(self):
        defaults = yaml.safe_load((ROLE / "defaults" / "main.yml").read_text())
        self.assertEqual(str(defaults["wireguard_udp_port"]), "51820")
        self.assertEqual(defaults["wireguard_allowed_ips"], "0.0.0.0/0")


if __name__ == "__main__":
    unittest.main()
