"""The openbao role: the house's vault in its own role, on its own network, keeping the data
the Endora collection's role left (Endora ADR 0127, amended 2026-11-07).

    python3 -m unittest discover -s tests -p 'test_*.py'

Reads the role's files as data, and runs its health check against a pretend `bao` that exits
as the real one does: 0 unsealed, 2 sealed (or not initialised), 1 when it cannot reach the
server.
"""

import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "openbao"
DIGEST = "sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def tasks_of(blocks):
    """Every task, flattened out of blocks, in order."""
    out = []
    for t in blocks:
        if "block" in t:
            out.extend(tasks_of(t["block"]))
        else:
            out.append(t)
    return out


def module(task, name):
    return task.get(f"community.docker.{name}")


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.vars = load(ROLE / "vars" / "main.yml")
        cls.tasks = tasks_of(load(ROLE / "tasks" / "main.yml"))

    def container_task(self):
        found = [
            t for t in self.tasks
            if module(t, "docker_container")
            and module(t, "docker_container").get("name") == "{{ openbao_container_name }}"
            and module(t, "docker_container").get("state") == "started"
        ]
        self.assertEqual(len(found), 1, "one task starts the vault")
        return found[0]

    def test_it_is_off_unless_switched_on(self):
        self.assertIs(self.defaults["openbao_enabled"], False)

    def test_it_runs_the_same_image_pinned_by_digest(self):
        # The move changes where the vault is declared, never which vault runs.
        self.assertTrue(self.defaults["openbao_image"].endswith("@" + DIGEST))
        container = module(self.container_task(), "docker_container")
        self.assertIs(container["pull"], False)
        self.assertEqual(container["labels"]["com.centurylinklabs.watchtower.enable"], "false")

    def test_it_keeps_the_data_where_it_is(self):
        # Same folder the Endora collection's role used, and an inventory that still names it
        # the old way (openbao_data_dir) is honoured: the vault opens with its old shares.
        self.assertIn("openbao_data_dir", self.defaults["openbao_data_directory"])
        self.assertIn("docker_home", self.defaults["openbao_data_directory"])
        self.assertIn("/openbao", self.defaults["openbao_data_directory"])
        container = module(self.container_task(), "docker_container")
        self.assertEqual(container["volumes"], ["{{ openbao_data_directory }}:/openbao/file"])
        # Raft storage only opens under the node id it was made with.
        self.assertEqual(self.vars["openbao_config"]["storage"]["raft"]["path"], "/openbao/file")
        self.assertEqual(self.vars["openbao_config"]["storage"]["raft"]["node_id"], "endora")
        # The declared audit device keeps its path, so it is the same device, not a second one.
        self.assertEqual(self.vars["openbao_config"]["audit"][0]["path"], "endora-audit")

    def test_no_task_removes_the_data(self):
        for t in self.tasks:
            f = t.get("ansible.builtin.file")
            if f and f.get("state") == "absent":
                self.fail(f"a task removes a path: {t['name']}")

    def test_it_has_its_own_internal_network(self):
        self.assertEqual(self.defaults["openbao_network_name"], "openbao")
        nets = [module(t, "docker_network") for t in self.tasks if module(t, "docker_network")]
        self.assertEqual(len(nets), 1)
        net = nets[0]
        self.assertEqual(net["name"], "{{ openbao_network_name }}")
        self.assertIs(net["internal"], True)
        self.assertEqual(
            net["driver_options"]["com.docker.network.bridge.gateway_mode_ipv4"], "isolated"
        )
        container = module(self.container_task(), "docker_container")
        self.assertEqual(container["network_mode"], "{{ openbao_network_name }}")
        self.assertIn("openbao_network_name", str(container["networks"]))
        # Clients reach it by this name: http://openbao:8200.
        self.assertEqual(self.defaults["openbao_alias"], "openbao")
        self.assertEqual(self.vars["openbao_config"]["api_addr"], "http://{{ openbao_alias }}:8200")

    def test_it_no_longer_needs_endoras_network(self):
        text = (ROLE / "tasks" / "main.yml").read_text(encoding="utf-8")
        self.assertNotIn("endora_vault", text)
        self.assertNotIn("docker_network_info", text)

    def test_it_retires_the_container_endora_ran_before_starting_its_own(self):
        self.assertEqual(self.defaults["openbao_legacy_container_name"], "endora-openbao")
        names = [t["name"] for t in self.tasks]
        legacy = [
            i for i, t in enumerate(self.tasks)
            if module(t, "docker_container")
            and module(t, "docker_container").get("name") == "{{ openbao_legacy_container_name }}"
            and module(t, "docker_container").get("state") == "absent"
        ]
        self.assertEqual(len(legacy), 1, names)
        self.assertLess(legacy[0], self.tasks.index(self.container_task()))

    def test_no_port_on_the_host_unless_asked(self):
        self.assertEqual(self.defaults["openbao_port"], "")

    def health(self, bao_exits):
        """Runs the container's health check with a pretend `bao`, returning its exit code."""
        test = module(self.container_task(), "docker_container")["healthcheck"]["test"]
        self.assertEqual(test[0], "CMD-SHELL")
        with tempfile.TemporaryDirectory() as d:
            bao = Path(d) / "bao"
            bao.write_text(f"#!/bin/sh\nexit {bao_exits}\n", encoding="utf-8")
            bao.chmod(bao.stat().st_mode | stat.S_IEXEC)
            env = dict(os.environ, PATH=f"{d}:{os.environ['PATH']}")
            return subprocess.run(["sh", "-c", test[1]], env=env, check=False).returncode

    def test_the_health_check_says_healthy_only_when_unsealed(self):
        self.assertEqual(self.health(0), 0, "unsealed is healthy")
        self.assertNotEqual(self.health(2), 0, "sealed is unhealthy, not merely answering")
        self.assertNotEqual(self.health(1), 0, "not answering is unhealthy")

    def test_the_run_reports_whether_it_is_sealed(self):
        execs = [module(t, "docker_container_exec") for t in self.tasks
                 if module(t, "docker_container_exec")]
        self.assertEqual(len(execs), 1)
        self.assertIn("bao status", execs[0]["command"])
        self.assertIn("-format=json", execs[0]["command"])
        reports = [t for t in self.tasks if "ansible.builtin.debug" in t]
        self.assertTrue(any("sealed" in str(t["ansible.builtin.debug"]) for t in reports))

    def test_it_holds_no_secret(self):
        for name in self.defaults:
            for word in ("token", "password", "share", "unseal_key", "secret"):
                self.assertNotIn(word, name, f"{name} looks like a secret setting")
        for path in ROLE.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for marker in ("hvs.", "s.ey", "-----BEGIN"):
                    self.assertNotIn(marker, text, f"{path} carries what looks like a secret")

    def test_it_stops_when_switched_off_keeping_its_data(self):
        stops = [
            t for t in self.tasks
            if module(t, "docker_container")
            and module(t, "docker_container").get("name") == "{{ openbao_container_name }}"
            and module(t, "docker_container").get("state") == "absent"
        ]
        self.assertEqual(len(stops), 1)


class ThePlaybook(unittest.TestCase):
    def test_the_playbook_runs_this_role_not_endoras(self):
        play = load(REPO / "nas.yml")
        roles = [r for p in play for r in p.get("roles", [])]
        names = [r["role"] if isinstance(r, dict) else r for r in roles]
        self.assertIn("openbao", names)
        self.assertNotIn("endora.homelab.openbao", names)
        entry = roles[names.index("openbao")]
        self.assertIn("openbao", entry["tags"])

    def test_it_follows_the_forks_conventions(self):
        self.assertTrue((ROLE / "molecule" / "default" / "molecule.yml").is_file())
        self.assertTrue((ROLE / "molecule" / "default" / "verify.yml").is_file())
        self.assertTrue((REPO / "website" / "docs" / "applications" / "other" / "openbao.md").is_file())


if __name__ == "__main__":
    unittest.main()
