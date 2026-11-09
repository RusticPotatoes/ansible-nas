"""The disk_guard role: caps build output, prunes old logs and alerts before a disk fills.

    python3 -m unittest discover -s tests -p 'test_*.py'

The script is run for real against folders made in a temporary directory, with a fake `df`
and a fake ntfy server (a file the script's request lands in), so the tests show what it
deletes and when it alerts, not only how the role is wired.
"""

import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROLE = REPO / "roles" / "disk_guard"
SCRIPT = ROLE / "files" / "disk-guard"
CACHEDIR_TAG = "Signature: 8a477f597d28d172789f06886806bc55\n# cargo build output\n"
DAY = 86400


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def make_target(root, name, size_kb, age_days, tag=CACHEDIR_TAG):
    """A cargo target folder `root/name/target` whose files are `age_days` old."""
    target = Path(root) / name / "target"
    (target / "debug").mkdir(parents=True)
    if tag is not None:
        (target / "CACHEDIR.TAG").write_text(tag)
    (target / "debug" / "blob").write_bytes(b"x" * size_kb * 1024)
    when = time.time() - age_days * DAY
    for path in [*target.rglob("*"), target]:
        os.utime(path, (when, when))
    return target


class TheScript(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.root = self.dir / "repos"
        self.root.mkdir()
        self.logs = self.dir / "logs"
        self.logs.mkdir()
        self.state = self.dir / "state"
        self.sent = self.dir / "sent"

    def tearDown(self):
        self.tmp.cleanup()

    def run_guard(self, use_percent=50, **env):
        base = {
            "PATH": os.environ["PATH"],
            "DISK_GUARD_ROOTS": str(self.root),
            "DISK_GUARD_TARGET_MAX_AGE_DAYS": "3",
            "DISK_GUARD_TARGET_CAP_MB": "1000",
            "DISK_GUARD_ACTIVE_MINUTES": "30",
            "DISK_GUARD_LOG_DIRS": str(self.logs),
            "DISK_GUARD_LOG_MAX_AGE_DAYS": "30",
            "DISK_GUARD_MOUNTS": "/",
            "DISK_GUARD_ALERT_PERCENT": "80",
            "DISK_GUARD_ALERT_EVERY_HOURS": "6",
            "DISK_GUARD_NTFY_TOPIC": "",
            "DISK_GUARD_STATE": str(self.state),
            # Test hooks: the disk use to report, and a file instead of the ntfy server.
            "DISK_GUARD_FAKE_USE_PERCENT": str(use_percent),
            "DISK_GUARD_FAKE_NTFY_FILE": str(self.sent),
            "HOSTNAME": "testhost",
        }
        base.update(env)
        return subprocess.run(
            ["python3", str(SCRIPT)], env=base, capture_output=True, text=True, check=True
        )

    def test_old_build_output_is_deleted_and_recent_output_kept(self):
        old = make_target(self.root, "old", 10, age_days=5)
        recent = make_target(self.root, "recent", 10, age_days=1)
        self.run_guard()
        self.assertFalse(old.exists())
        self.assertTrue(recent.exists())

    def test_over_the_cap_the_least_recent_go_first_until_under_it(self):
        a = make_target(self.root, "a", 400, age_days=2.5)
        b = make_target(self.root, "b", 400, age_days=2)
        c = make_target(self.root, "c", 400, age_days=1)
        self.run_guard(DISK_GUARD_TARGET_CAP_MB="1")
        self.assertFalse(a.exists())
        self.assertTrue(b.exists() and c.exists())

    def test_a_folder_being_built_now_is_never_deleted(self):
        busy = make_target(self.root, "busy", 10, age_days=10)
        (busy / "debug" / "fresh").write_text("being written")
        self.run_guard(DISK_GUARD_TARGET_CAP_MB="0")
        self.assertTrue(busy.exists())

    def test_only_cargo_folders_are_touched(self):
        untagged = make_target(self.root, "mine", 10, age_days=30, tag=None)
        wrong = make_target(self.root, "other", 10, age_days=30, tag="not cargo\n")
        self.run_guard(DISK_GUARD_TARGET_CAP_MB="0")
        self.assertTrue(untagged.exists())
        self.assertTrue(wrong.exists())

    def test_nothing_outside_the_roots_is_touched(self):
        outside = self.dir / "elsewhere"
        outside.mkdir()
        far = make_target(outside, "far", 10, age_days=30)
        self.run_guard(DISK_GUARD_TARGET_CAP_MB="0")
        self.assertTrue(far.exists())

    def test_old_logs_are_deleted_and_new_ones_kept(self):
        old, new = self.logs / "old.log", self.logs / "new.log"
        old.write_text("a")
        new.write_text("b")
        when = time.time() - 40 * DAY
        os.utime(old, (when, when))
        self.run_guard()
        self.assertFalse(old.exists())
        self.assertTrue(new.exists())

    def test_no_alert_below_the_threshold(self):
        self.run_guard(use_percent=79, DISK_GUARD_NTFY_TOPIC="topic")
        self.assertFalse(self.sent.exists())

    def test_an_alert_names_the_host_mount_and_use_once_per_interval(self):
        self.run_guard(use_percent=95, DISK_GUARD_NTFY_TOPIC="topic")
        message = self.sent.read_text()
        self.assertIn("testhost", message)
        self.assertIn("/", message)
        self.assertIn("95%", message)
        self.sent.unlink()
        self.run_guard(use_percent=95, DISK_GUARD_NTFY_TOPIC="topic")
        self.assertFalse(self.sent.exists(), "a second alert within the interval")

    def test_without_a_topic_it_still_reports_in_its_output(self):
        out = self.run_guard(use_percent=95).stdout
        self.assertIn("95%", out)
        self.assertFalse(self.sent.exists())


class TheRole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defaults = load(ROLE / "defaults" / "main.yml")
        cls.tasks = load(ROLE / "tasks" / "main.yml")
        cls.play = load(REPO / "t3.yml")[0]

    def test_every_variable_is_named_for_the_role(self):
        for name in self.defaults:
            self.assertTrue(name.startswith("disk_guard_"), name)

    def test_the_t3_play_runs_it(self):
        roles = [r["role"] for r in self.play["roles"]]
        self.assertIn("disk_guard", roles)

    def test_only_growing_the_root_volume_needs_root(self):
        names = [t["name"] for t in self.tasks if t.get("become")]
        self.assertEqual(names, ["Grow the root volume into the volume group's free space"])

    def test_the_root_volume_is_never_shrunk(self):
        grow = [t for t in self.tasks if "community.general.lvol" in t][0]
        self.assertFalse(grow["community.general.lvol"]["shrink"])
        self.assertTrue(grow["community.general.lvol"]["resizefs"])

    def test_the_ntfy_topic_comes_from_the_environment_not_a_file(self):
        self.assertIn("lookup('env'", self.defaults["disk_guard_ntfy_topic"])

    def test_a_failed_or_changed_timer_is_restarted_not_only_reloaded(self):
        tasks = [t for b in self.tasks if "block" in b for t in b["block"]]
        repair = [t for t in tasks if t.get("name") == "Restart the timer when it has failed or stopped"]
        self.assertEqual(len(repair), 1)
        self.assertEqual(repair[0]["ansible.builtin.systemd_service"]["state"], "restarted")
        self.assertIn("ActiveState", repair[0]["when"])
        write = [t for t in tasks if t.get("name") == "Write its service and timer"][0]
        handlers = load(ROLE / "handlers" / "main.yml")
        self.assertEqual(write["notify"], handlers[0]["name"])
        self.assertEqual(handlers[0]["ansible.builtin.systemd_service"]["state"], "restarted")
        self.assertEqual(handlers[0]["ansible.builtin.systemd_service"]["name"], "disk-guard.timer")


if __name__ == "__main__":
    unittest.main()
