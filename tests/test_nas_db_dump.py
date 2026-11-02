"""The nas-db-dump job's script, rendered from its template and run against a fake docker.

    python3 -m unittest discover -s tests -p 'test_*.py'

The fake docker runs each `docker exec CONTAINER sh -c CMD` in the host's sh, with fake
pg_dumpall and mongodump defined as shell functions in front of CMD, so a failing pg_dumpall
inside a pipeline behaves as it does in a container whose shell has no pipefail. Only shell
functions are faked: nothing has to be executable on the test's disk.
"""

import gzip
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import jinja2

TEMPLATE = Path(__file__).resolve().parent.parent / "roles/nas_maintenance/templates/jobs/nas-db-dump.sh.j2"

# Defined in the container's sh before each command the job execs there.
CONTAINER_PRELUDE = """
pg_dumpall() {
  if [ -n "$FAKE_PG_FAIL" ]; then echo "pg_dumpall: connection refused" >&2; return 1; fi
  echo "CREATE TABLE t (id int);"
}
mongodump() {
  if [ -n "$FAKE_MONGO_FAIL" ]; then return 1; fi
  printf 'MONGO-ARCHIVE'
}
"""

# Put in front of the rendered script: the prelude as a variable, and docker inspect says running;
# docker exec runs its command in a sh that starts with the prelude.
FAKE_DOCKER = """
FAKE_PRELUDE=$(cat <<'PRELUDE'
%s
PRELUDE
)
docker() {
  case "$1" in
    inspect) echo true ;;
    exec) sh -c "$FAKE_PRELUDE
$5" ;;   # docker exec CONTAINER sh -c CMD
    *) return 2 ;;
  esac
}
""" % CONTAINER_PRELUDE

PREVIOUS = b"previous good dump"
PREVIOUS_STATUS = "nas_db_dump,db=postgres last_success=1000i\n"


def render(postgres="postgres", mongodb=""):
    source = TEMPLATE.read_text()
    script = jinja2.Template(source).render(
        nas_db_dump_directory="{out}",
        nas_status_directory="{status}",
        nas_db_dump_postgres_container=postgres,
        nas_db_dump_mongodb_container=mongodb,
    )
    shebang, rest = script.split("\n", 1)
    return shebang + "\n" + FAKE_DOCKER + rest


class DumpJob(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.out = root / "db-dumps"
        self.status = root / "nas-status"
        self.out.mkdir()
        self.status.mkdir()
        (self.out / "postgres.sql.gz").write_bytes(PREVIOUS)
        (self.status / "db_postgres.influx").write_text(PREVIOUS_STATUS)
        self.script = root / "job.sh"

    def tearDown(self):
        self.tmp.cleanup()

    def run_job(self, postgres="postgres", mongodb="", env=None):
        text = render(postgres, mongodb).replace("{out}", str(self.out)).replace(
            "{status}", str(self.status))
        self.script.write_text(text)
        return subprocess.run(["bash", str(self.script)], env={**os.environ, **(env or {})},
                              capture_output=True, text=True, check=False)

    def test_a_failed_postgres_dump_keeps_the_last_good_one_and_fails(self):
        ran = self.run_job(env={"FAKE_PG_FAIL": "1"})
        self.assertNotEqual(ran.returncode, 0, ran.stderr)
        self.assertIn("postgres: dump failed", ran.stderr)
        self.assertEqual((self.out / "postgres.sql.gz").read_bytes(), PREVIOUS)
        self.assertEqual((self.status / "db_postgres.influx").read_text(), PREVIOUS_STATUS)
        self.assertFalse((self.out / "postgres.sql.gz.tmp").exists())

    def test_a_failed_postgres_dump_writes_no_success_status_when_none_existed(self):
        (self.status / "db_postgres.influx").unlink()
        ran = self.run_job(env={"FAKE_PG_FAIL": "1"})
        self.assertNotEqual(ran.returncode, 0, ran.stderr)
        self.assertFalse((self.status / "db_postgres.influx").exists())

    def test_a_successful_postgres_dump_is_gzipped_sql_with_a_status_line(self):
        ran = self.run_job()
        self.assertEqual(ran.returncode, 0, ran.stderr)
        with gzip.open(self.out / "postgres.sql.gz", "rt") as f:
            self.assertEqual(f.read(), "CREATE TABLE t (id int);\n")
        status = (self.status / "db_postgres.influx").read_text()
        self.assertRegex(status, r"^nas_db_dump,db=postgres last_success=\d+i\n$")

    def test_a_failed_mongodb_dump_keeps_the_last_good_one_and_fails(self):
        (self.out / "mongodb.archive.gz").write_bytes(PREVIOUS)
        ran = self.run_job(postgres="", mongodb="mongodb", env={"FAKE_MONGO_FAIL": "1"})
        self.assertNotEqual(ran.returncode, 0, ran.stderr)
        self.assertEqual((self.out / "mongodb.archive.gz").read_bytes(), PREVIOUS)

    def test_a_successful_mongodb_dump_is_written_as_it_comes(self):
        ran = self.run_job(postgres="", mongodb="mongodb")
        self.assertEqual(ran.returncode, 0, ran.stderr)
        self.assertEqual((self.out / "mongodb.archive.gz").read_bytes(), b"MONGO-ARCHIVE")
        self.assertTrue((self.status / "db_mongodb.influx").exists())


if __name__ == "__main__":
    unittest.main()
