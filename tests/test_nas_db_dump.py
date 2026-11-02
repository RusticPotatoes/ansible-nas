"""The nas-db-dump job, rendered from its template and run against a fake docker.

    python3 -m unittest discover -s tests -p 'test_*.py'

A failed Postgres dump must keep the last good postgres.sql.gz, record no success status and
exit non-zero; a good run must leave the same files as before.
"""

import gzip
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import jinja2

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "roles/nas_maintenance/templates/jobs/nas-db-dump.sh.j2"

# The dump commands and docker are bash functions the script inherits, so no executable file
# is needed (the temp directory may be mounted noexec). docker exec runs its command through
# a subshell with the script's options cleared, so the pipeline the script builds is the one
# under test, run as a container shell without pipefail would run it.
FAKE_DOCKER = """
pg_dumpall() {
  if [ "$FAKE_PG_FAIL" = 1 ]; then printf 'partial'; return 1; fi
  printf 'CREATE TABLE t (id int);\\n'
}
mongodump() { printf 'mongo-archive'; }
docker() {
  case "$1" in
    inspect) echo true ;;
    exec) ( set +eu +o pipefail; eval "$5" ) ;;  # the container shell: no pipefail
    *) return 2 ;;
  esac
}
export -f pg_dumpall mongodump docker
bash "$FAKE_SCRIPT"
"""


def render(out, status):
    return jinja2.Template(TEMPLATE.read_text()).render(
        nas_db_dump_directory=str(out),
        nas_status_directory=str(status),
        nas_db_dump_postgres_container="pg",
        nas_db_dump_mongodb_container="mongodb",
    )


class NasDbDump(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.out = root / "dumps"
        self.status = root / "status"
        self.out.mkdir()
        self.status.mkdir()
        self.script = root / "nas-db-dump"
        self.script.write_text(render(self.out, self.status))
        # the last good dumps, which a failed run must not touch
        (self.out / "postgres.sql.gz").write_bytes(gzip.compress(b"GOOD POSTGRES\n"))
        (self.out / "mongodb.archive.gz").write_bytes(b"GOOD MONGO")

    def tearDown(self):
        self.tmp.cleanup()

    def run_job(self, pg_fail):
        env = dict(os.environ, FAKE_PG_FAIL="1" if pg_fail else "0", FAKE_SCRIPT=str(self.script),
                   POSTGRES_USER="postgres", MONGODB_INITDB_ROOT_USERNAME="root",
                   MONGODB_INITDB_ROOT_PASSWORD="x")
        return subprocess.run(["bash", "-c", FAKE_DOCKER], env=env, capture_output=True, text=True)

    def test_failed_postgres_dump_keeps_last_good_and_fails(self):
        before = (self.out / "postgres.sql.gz").read_bytes()
        result = self.run_job(pg_fail=True)
        self.assertIn("postgres: dump failed", result.stderr)
        self.assertNotEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.out / "postgres.sql.gz").read_bytes(), before)
        self.assertFalse((self.out / "postgres.sql.gz.tmp").exists())
        self.assertFalse((self.status / "db_postgres.influx").exists())

    def test_failed_postgres_dump_leaves_prior_status_alone(self):
        (self.status / "db_postgres.influx").write_text("old\n")
        self.run_job(pg_fail=True)
        self.assertEqual((self.status / "db_postgres.influx").read_text(), "old\n")

    def test_good_run_writes_same_files(self):
        result = self.run_job(pg_fail=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(gzip.decompress((self.out / "postgres.sql.gz").read_bytes()),
                         b"CREATE TABLE t (id int);\n")
        self.assertTrue((self.status / "db_postgres.influx").read_text()
                        .startswith("nas_db_dump,db=postgres last_success="))
        self.assertEqual((self.out / "mongodb.archive.gz").read_bytes(), b"mongo-archive")
        self.assertTrue((self.status / "db_mongodb.influx").read_text()
                        .startswith("nas_db_dump,db=mongodb last_success="))


if __name__ == "__main__":
    unittest.main()
