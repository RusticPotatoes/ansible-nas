"""The nas-db-dump job (nas_maintenance), rendered from its template and run with bash.

docker and the database tools are bash functions in front of the rendered script, so the
test needs no executables on the PATH (some sandboxes mount /tmp without exec). `docker exec`
runs its command with `sh -c`, as a container's shell would (no pipefail), so a failed
pg_dumpall shows up as the exit status of `docker exec`.

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import gzip
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import jinja2

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "roles" / "nas_maintenance" / "templates" / "jobs" / "nas-db-dump.sh.j2"

FAKES = r"""
docker() {
  case "$1" in
    inspect) echo true ;;
    exec) shift 4; (set +u +o pipefail; eval "$1") ;;
  esac
}
pg_dumpall() {
  if [ -n "${FAKE_PG_FAIL:-}" ]; then echo "partial"; echo "pg_dumpall: boom" >&2; return 1; fi
  echo "CREATE TABLE t (id int);"
  echo "INSERT INTO t VALUES (1);"
}
mongodump() { echo "mongo-archive-bytes"; }
"""


def render(**extra):
    values = {
        "nas_db_dump_directory": "OUT",
        "nas_status_directory": "STATUS",
        "nas_db_dump_postgres_container": "pg",
        "nas_db_dump_mongodb_container": "mongo",
    }
    values.update(extra)
    env = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
    return env.from_string(TEMPLATE.read_text()).render(**values)


class DumpJob(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.out = self.tmp / "dumps"
        self.status = self.tmp / "status"
        self.out.mkdir()
        self.status.mkdir()
        self.wrapper = self.tmp / "run.sh"
        self.wrapper.write_text(FAKES + "\n" + render(
            nas_db_dump_directory=str(self.out), nas_status_directory=str(self.status)))

    def run_job(self, **env):
        full = dict(os.environ, POSTGRES_USER="postgres", MONGODB_INITDB_ROOT_USERNAME="root",
                    MONGODB_INITDB_ROOT_PASSWORD="secret", **env)
        return subprocess.run(["bash", str(self.wrapper)], env=full,
                              capture_output=True, text=True, check=False)

    def test_a_failed_postgres_dump_keeps_the_last_good_dump_and_fails(self):
        good = self.out / "postgres.sql.gz"
        good.write_bytes(b"previous good dump")
        result = self.run_job(FAKE_PG_FAIL="1")
        self.assertEqual(good.read_bytes(), b"previous good dump", result.stderr)
        self.assertFalse((self.out / "postgres.sql.gz.tmp").exists())
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_a_failed_postgres_dump_writes_no_success_status(self):
        result = self.run_job(FAKE_PG_FAIL="1")
        self.assertFalse((self.status / "db_postgres.influx").exists(),
                         result.stdout + result.stderr)
        self.assertNotEqual(result.returncode, 0)

    def test_a_good_run_writes_gzipped_sql_and_the_status_line(self):
        result = self.run_job()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        sql = gzip.decompress((self.out / "postgres.sql.gz").read_bytes()).decode()
        self.assertIn("CREATE TABLE t", sql)
        line = (self.status / "db_postgres.influx").read_text()
        self.assertRegex(line, r"^nas_db_dump,db=postgres last_success=\d+i\n$")
        self.assertEqual((self.out / "mongodb.archive.gz").read_text(), "mongo-archive-bytes\n")

    def test_the_mongodb_command_is_the_same_as_before(self):
        rendered = render()
        self.assertIn(
            "'mongodump --quiet --archive --gzip --authenticationDatabase admin "
            "-u \"$MONGODB_INITDB_ROOT_USERNAME\" -p \"$MONGODB_INITDB_ROOT_PASSWORD\"'",
            rendered)
        self.assertEqual(len(re.findall(r"^dump mongodb ", rendered, re.M)), 1)


if __name__ == "__main__":
    unittest.main()
