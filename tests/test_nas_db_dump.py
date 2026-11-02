"""The nas-db-dump job script, rendered from its template and run against a fake docker.

A failed dump must fail the job and leave the last good file and status alone, whatever
the container's shell does. Run with the other unit tests:

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import gzip
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    import jinja2
except ImportError:  # the fork's venv always has it (ansible needs it); skip otherwise
    jinja2 = None

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "roles/nas_maintenance/templates/jobs/nas-db-dump.sh.j2"

# The fakes are bash functions, sourced with the rendered script: no file on PATH has to be
# executable, so the test runs wherever a temporary directory is mounted noexec.
# docker: `inspect` reports the container running; `exec CONTAINER sh -c CMD` runs CMD in a
# shell here, with the container's tools (pg_dumpall, mongodump) as docker exec would.
FAKE_TOOLS = """
pg_dumpall() {
  if [ -n "${FAKE_PG_FAIL:-}" ]; then
    echo "-- partial dump"
    echo "pg_dumpall: connection lost" >&2
    return 1
  fi
  echo "-- PostgreSQL database cluster dump"
  echo "CREATE TABLE t (id int);"
}
mongodump() {
  echo "$@" > "$FAKE_LOG"
  echo "mongo archive bytes"
}
docker() {
  case "$1" in
    inspect) echo true ;;
    exec) eval "$5" ;;
    *) return 2 ;;
  esac
}
"""


def script_text(out, status, postgres="", mongodb=""):
    env = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
    return env.from_string(TEMPLATE.read_text()).render(
        nas_db_dump_directory=out,
        nas_status_directory=status,
        nas_db_dump_postgres_container=postgres,
        nas_db_dump_mongodb_container=mongodb,
    )


@unittest.skipIf(jinja2 is None, "jinja2 not installed")
class NasDbDumpTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.out = self.tmp / "dumps"
        self.status = self.tmp / "status"
        self.bin = self.tmp / "bin"
        for d in (self.out, self.status, self.bin):
            d.mkdir()
        self.script = self.tmp / "nas-db-dump.sh"
        self.runner = self.tmp / "runner.sh"
        self.log = self.tmp / "mongodump.args"

    def run_script(self, postgres="postgres", mongodb="", fail=False):
        self.script.write_text(script_text(self.out, self.status, postgres, mongodb))
        self.runner.write_text(f"{FAKE_TOOLS}\nsource {self.script}\n")
        env = dict(os.environ, FAKE_LOG=str(self.log), POSTGRES_USER="postgres",
                   MONGODB_INITDB_ROOT_USERNAME="root", MONGODB_INITDB_ROOT_PASSWORD="secret")
        env.pop("FAKE_PG_FAIL", None)
        if fail:
            env["FAKE_PG_FAIL"] = "1"
        return subprocess.run(
            ["bash", str(self.runner)], env=env, capture_output=True, text=True, check=False
        )

    def test_success_writes_gzip_sql_and_status(self):
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stderr)
        with gzip.open(self.out / "postgres.sql.gz", "rt") as f:
            self.assertIn("CREATE TABLE t", f.read())
        status = (self.status / "db_postgres.influx").read_text()
        self.assertRegex(status, r"^nas_db_dump,db=postgres last_success=\d+i\n$")
        self.assertFalse((self.out / "postgres.sql.gz.tmp").exists())

    def test_failed_dump_keeps_last_good_file_and_writes_no_status(self):
        good = self.out / "postgres.sql.gz"
        good.write_bytes(gzip.compress(b"-- last good dump\n"))
        before = good.read_bytes()
        r = self.run_script(fail=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(good.read_bytes(), before)
        self.assertFalse((self.status / "db_postgres.influx").exists())
        self.assertFalse((self.out / "postgres.sql.gz.tmp").exists())
        self.assertIn("postgres: dump failed", r.stderr)

    def test_failed_dump_does_not_replace_a_previous_status(self):
        status = self.status / "db_postgres.influx"
        status.write_text("nas_db_dump,db=postgres last_success=1i\n")
        r = self.run_script(fail=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(status.read_text(), "nas_db_dump,db=postgres last_success=1i\n")

    def test_mongodb_runs_the_same_command_and_writes_its_archive(self):
        r = self.run_script(postgres="", mongodb="mongodb")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            self.log.read_text().strip(),
            "--quiet --archive --gzip --authenticationDatabase admin "
            "-u root -p secret",
        )
        self.assertEqual((self.out / "mongodb.archive.gz").read_text(), "mongo archive bytes\n")
        self.assertIn("db=mongodb", (self.status / "db_mongodb.influx").read_text())


if __name__ == "__main__":
    unittest.main()
