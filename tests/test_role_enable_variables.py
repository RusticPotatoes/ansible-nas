"""Every `<app>_enabled` a role's tasks test in `when:` is defined somewhere, so switching an
application on by the name its defaults and docs give does what it says.

    python3 -m unittest discover -s tests -p 'test_*.py'

Found when route53_ddns and speedtest-tracker read one name and defined another.
"""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROLES = REPO / "roles"

# Set by another role rather than by defaults: the logging stack includes loki with it.
SET_ELSEWHERE = {"grafana_enabled"}

TOP_LEVEL_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):", re.M)
WHEN = re.compile(r"^(?P<indent>\s*)(?:- )?when:\s*(?P<rest>.*)$")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)- (?P<rest>.*)$")
# An enable variable read bare: one followed by `| default(...)` may be undefined on purpose.
ENABLED = re.compile(r"\b([a-z0-9_]+_enabled)\b(?!\s*\|\s*default)")


def defined_variables():
    names = set()
    for defaults in ROLES.glob("*/defaults/main.yml"):
        names.update(TOP_LEVEL_KEY.findall(defaults.read_text()))
    return names


def conditions(tasks_file):
    """(line number, condition text) of every `when:` in a tasks file, list form included."""
    lines = tasks_file.read_text().splitlines()
    for number, line in enumerate(lines, start=1):
        match = WHEN.match(line)
        if not match:
            continue
        if match["rest"]:
            yield number, match["rest"]
            continue
        for offset, item in enumerate(lines[number:], start=number + 1):
            listed = LIST_ITEM.match(item)
            if not listed or len(listed["indent"]) < len(match["indent"]):
                break
            yield offset, listed["rest"]


class EnableVariables(unittest.TestCase):
    def test_every_enable_variable_read_is_defined(self):
        defined = defined_variables() | SET_ELSEWHERE
        undefined = []
        for tasks_file in sorted(ROLES.glob("*/tasks/*.yml")):
            for number, condition in conditions(tasks_file):
                for name in ENABLED.findall(condition):
                    if name not in defined:
                        where = tasks_file.relative_to(REPO)
                        undefined.append(f"{where}:{number}: {name}")
        self.assertEqual(undefined, [], "read in `when:` but defined in no role's defaults")


if __name__ == "__main__":
    unittest.main()
