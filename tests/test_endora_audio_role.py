"""The endora_audio role: Endora Audio's four containers, laid out as Endora's compose laid out
its sound containers (Endora 6d95b9d4, docker-compose.yml), so moving over changes where they
are declared, not what runs.

    python3 -m unittest discover -s tests -p 'test_*.py'

Reads the role's files as data. The senders' API list is rendered with Jinja when it is
installed (it is wherever Ansible is).
"""

import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "endora_audio"
LIBRESPOT = "giof71/librespot@sha256:0c7cd19a49547cd0e34ac7c6d9aadd4b2703c5cb13acd1dbfd4982c311d478fb"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def tasks_of(blocks):
    out = []
    for t in blocks:
        if "block" in t:
            out.extend(tasks_of(t["block"]))
        else:
            out.append(t)
    return out


def container(tasks, name_var):
    found = [
        t["community.docker.docker_container"] for t in tasks
        if "community.docker.docker_container" in t
        and t["community.docker.docker_container"].get("name") == "{{ %s }}" % name_var
        and t["community.docker.docker_container"].get("state") != "absent"
    ]
    assert len(found) == 1, f"one task starts {name_var}: {len(found)}"
    return found[0]


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.raw = load(ROLE / "tasks" / "main.yml")
        cls.tasks = tasks_of(cls.raw)
        cls.hub = container(cls.tasks, "endora_audio_container_name")
        cls.spotify = container(cls.tasks, "endora_audio_spotify_container_name")
        cls.senders = container(cls.tasks, "endora_audio_senders_container_name")
        cls.door = container(cls.tasks, "endora_audio_airplay_container_name")

    def test_it_is_off_unless_switched_on_and_the_door_is_opt_in(self):
        self.assertIs(self.defaults["endora_audio_enabled"], False)
        self.assertIs(self.defaults["endora_audio_airplay_enabled"], False)
        # Publishing to the internet domain is the owner's decision, never a default.
        self.assertIs(self.defaults["endora_audio_available_externally"], False)
        self.assertEqual(self.defaults["endora_audio_airplay_ip"], "")
        self.assertEqual(self.defaults["endora_audio_airplay_mac"], "")

    def test_it_runs_the_published_images_and_stock_librespot(self):
        for key, name in [("endora_audio_image", "endora-audio"),
                          ("endora_audio_senders_image", "endora-audio-senders"),
                          ("endora_audio_airplay_image", "endora-audio-airplay")]:
            self.assertEqual(self.defaults[key], f"ghcr.io/rusticpotatos/{name}:{{{{ endora_audio_version }}}}")
        self.assertEqual(self.defaults["endora_audio_spotify_image"], LIBRESPOT, "the build Endora ran")
        self.assertEqual(self.defaults["endora_audio_version"], "1.0.0", "a release, never a moving tag")

    def test_the_hub_is_fenced_as_endora_ran_it_and_publishes_its_page(self):
        hub = self.hub
        self.assertTrue(hub["read_only"])
        self.assertEqual(hub["cap_drop"], ["ALL"])
        self.assertEqual(hub["security_opts"], ["no-new-privileges:true"])
        self.assertEqual(hub["tmpfs"], ["/tmp"])
        self.assertEqual(hub["etc_hosts"], {"host.docker.internal": "host-gateway"})
        self.assertEqual(hub["published_ports"], ["{{ endora_audio_port }}:8791"])
        self.assertEqual(hub["volumes"], [
            "{{ endora_audio_data_volume }}:/data",
            "{{ endora_audio_token_volume }}:/token",
            "{{ endora_audio_pipes_volume }}:/pipes",
            "{{ endora_audio_secret_volume }}:/sender-secret:ro",
        ])
        self.assertEqual(hub["env"]["SOUND_SENDER_PASSWORD_FILE"], "/sender-secret/password")
        self.assertEqual(self.defaults["endora_audio_memory"], "256m")

    def test_the_hub_reaches_the_four_senders_through_the_host(self):
        try:
            import jinja2
        except ImportError:
            self.skipTest("no jinja2")
        env = jinja2.Environment()
        env.filters["regex_replace"] = lambda s, a, b: __import__("re").sub(a, b, s)
        render = lambda on: env.from_string(self.hub["env"]["SOUND_SENDERS"]).render(
            endora_audio_senders_ports=self.defaults["endora_audio_senders_ports"],
            endora_audio_senders_enabled=on).strip()
        self.assertEqual(render(True), ",".join(f"http://host.docker.internal:{p}" for p in (3701, 3702, 3703, 3704)))
        self.assertEqual(render(False), "", "no senders: streams only")

    def test_spotify_and_the_senders_are_on_the_hosts_network_with_endoras_settings(self):
        self.assertEqual(self.spotify["network_mode"], "host")
        self.assertEqual(self.spotify["env"]["DEVICE"], "/pipes/spotify.pcm")
        self.assertEqual(self.spotify["env"]["BACKEND"], "pipe")
        self.assertEqual(self.spotify["env"]["FORMAT"], "S16")
        self.assertEqual(self.spotify["volumes"], [
            "{{ endora_audio_pipes_volume }}:/pipes",
            "{{ endora_audio_spotify_login_volume }}:/data/system-cache",
        ])
        self.assertEqual(self.senders["network_mode"], "host")
        self.assertEqual(self.senders["capabilities"], ["CHOWN", "SETUID", "SETGID", "NET_BIND_SERVICE", "KILL"])
        self.assertEqual(self.senders["tmpfs"], ["/run", "/tmp"])
        self.assertEqual(self.senders["volumes"], [
            "{{ endora_audio_pipes_volume }}:/pipes",
            "{{ endora_audio_senders_data_volume }}:/data",
            "{{ endora_audio_secret_volume }}:/secret",
        ])
        self.assertIn("endora_audio_airplay_enabled", self.senders["env"]["SOUND_AIRPLAY2"])

    def test_the_door_joins_an_existing_macvlan_with_its_fixed_address_and_mac(self):
        door = self.door
        self.assertEqual(door["network_mode"], "{{ endora_audio_airplay_network }}")
        self.assertEqual(door["networks"], [{"name": "{{ endora_audio_airplay_network }}", "ipv4_address": "{{ endora_audio_airplay_ip }}"}])
        self.assertEqual(door["mac_address"], "{{ endora_audio_airplay_mac }}")
        self.assertEqual(door["volumes"], ["{{ endora_audio_pipes_volume }}:/pipes"], "only the pipes")
        self.assertEqual(self.defaults["endora_audio_airplay_network"], "pihole_macvlan")
        self.assertFalse([t for t in self.tasks if "community.docker.docker_network" in t], "the network is never made here")
        info = [t for t in self.tasks if "community.docker.docker_network_info" in t]
        self.assertEqual(len(info), 1, "it is looked for")

    def test_it_refuses_the_senders_beside_owntone_and_a_door_without_its_values(self):
        asserts = [t["ansible.builtin.assert"]["that"] for t in self.tasks if "ansible.builtin.assert" in t]
        joined = "\n".join(str(a) for a in asserts)
        self.assertIn("owntone_enabled", joined)
        self.assertIn("endora_audio_airplay_ip | length > 0", joined)
        self.assertIn("endora_audio_airplay_mac is match", joined)

    def test_no_task_removes_a_volume(self):
        for t in self.tasks:
            vol = t.get("community.docker.docker_volume")
            if vol:
                self.assertEqual(vol.get("state"), "present")
        stop = [b for b in self.raw if b.get("when") == "endora_audio_enabled is false"]
        self.assertEqual(len(stop), 1)
        self.assertEqual(len(stop[0]["block"]), 1)
        self.assertEqual(stop[0]["block"][0]["community.docker.docker_container"]["state"], "absent")

    def test_every_variable_is_the_roles_own(self):
        for key in self.defaults:
            self.assertTrue(key.startswith("endora_audio_"), key)

    def test_it_is_in_the_playbook(self):
        nas = load(REPO / "nas.yml")
        roles = [r.get("role") for play in nas for r in play.get("roles", []) if isinstance(r, dict)]
        self.assertIn("endora_audio", roles)


if __name__ == "__main__":
    unittest.main()
