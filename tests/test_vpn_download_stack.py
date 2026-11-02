"""The VPN download stack and the apps that join gluetun's network with it (#1042).

Every role whose container joins gluetun's network because the stack is on must be in
gluetun_routed_containers exactly when it is on, with its port published through gluetun, and
must run under the gluetun tag, so a gluetun run or a stack restart never leaves one stopped.

    python3 -m unittest discover -s tests -p 'test_*.py'

Needs ansible-playbook on the PATH; the stack's facts are worked out by running the role locally.
"""

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLES = REPO / "roles"
STACK = "vpn-download-stack"
JOINS = re.compile(r"network_mode: .*gluetun_name if .*vpn_download_stack_enabled", re.M)


def joiners():
    """Roles whose container joins gluetun's network when the stack is on."""
    found = []
    for tasks in sorted(ROLES.glob("*/tasks/main.yml")):
        if JOINS.search(tasks.read_text()):
            found.append(tasks.parent.parent.name)
    return found


def defaults(role):
    return yaml.safe_load((ROLES / role / "defaults" / "main.yml").read_text()) or {}


def nas_tags():
    """The tags each role carries in nas.yml."""
    plays = yaml.safe_load((REPO / "nas.yml").read_text())
    tags = {}
    for entry in plays[0]["roles"]:
        if isinstance(entry, dict):
            tags[entry["role"]] = set(entry.get("tags", []))
    return tags


def stack_run(tmp, overrides):
    """The gluetun_routed_containers the stack role works out, with the given variables."""
    out = Path(tmp) / "routed.json"
    include = [str(ROLES / role / "defaults" / "main.yml") for role in [*joiners(), "gluetun", STACK]]
    play = [{
        "hosts": "localhost",
        "connection": "local",
        "gather_facts": False,
        "pre_tasks": [{"ansible.builtin.include_vars": {"file": path}} for path in include],
        "roles": [STACK],
        "tasks": [{"ansible.builtin.copy": {
            "content": "{{ gluetun_routed_containers | to_json }}", "dest": str(out)}}],
    }]
    playbook = Path(tmp) / "site.yml"
    playbook.write_text(yaml.safe_dump(play))
    env = dict(os.environ, ANSIBLE_ROLES_PATH=str(ROLES), ANSIBLE_LOCALHOST_WARNING="False",
               ANSIBLE_INVENTORY_UNPARSED_WARNING="False")
    ran = subprocess.run(
        ["ansible-playbook", "-i", "localhost,", str(playbook),
         "-e", json.dumps({"vpn_download_stack_enabled": True, **overrides})],
        cwd=REPO, env=env, capture_output=True, text=True, check=False,
    )
    if ran.returncode != 0:
        raise AssertionError(ran.stdout + ran.stderr)
    return json.loads(out.read_text())


class TheStackAndItsJoiners(unittest.TestCase):
    def test_every_joiner_in_nas_yml_runs_under_the_gluetun_tag(self):
        tags = nas_tags()
        in_play = [role for role in joiners() if role in tags]
        self.assertTrue(in_play, "no joiner found in nas.yml; the test would prove nothing")
        missing = [role for role in in_play if "gluetun" not in tags[role]]
        self.assertEqual(missing, [], "roles in nas.yml without the gluetun tag")

    def test_stack_on_routes_every_joiner_through_gluetun_with_its_port(self):
        # Every joiner switched on, the stack on: each is routed, once, with its port.
        on = {f"{role}_enabled": True for role in joiners()}
        on.update({f"vpn_download_stack_{role}_enabled": True for role in joiners()})
        with tempfile.TemporaryDirectory() as tmp:
            routed = stack_run(tmp, on)
        by_name = {entry["name"]: entry for entry in routed}
        self.assertEqual(len(by_name), len(routed), "a container is routed twice")
        for role in joiners():
            values = defaults(role)
            name = str(values[f"{role}_container_name"])
            self.assertIn(name, by_name, f"{role} joins gluetun but is not routed")
            port = str(values[f"{role}_port"])
            internal = re.search(r"\[\s*\w+_port ~ ':(\d+)'\]", (ROLES / role / "tasks/main.yml").read_text())
            self.assertIsNotNone(internal, f"{role} publishes no port of its own")
            self.assertEqual(by_name[name]["ports"], [f"{port}:{internal.group(1)}"], role)

    def test_a_joiner_is_routed_only_while_it_is_on(self):
        for role in joiners():
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                off = {f"{role}_enabled": False, f"vpn_download_stack_{role}_enabled": False,
                       f"{role}_vpn_enabled": False}
                routed = stack_run(tmp, off)
                name = str(defaults(role)[f"{role}_container_name"])
                self.assertNotIn(name, [entry["name"] for entry in routed])


if __name__ == "__main__":
    unittest.main()
