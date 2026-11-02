"""The application docs pages name the ports their roles really publish.

Every web address on a page under website/docs/applications (`ansible_nas_host_or_ip:PORT`)
must name a host port that the page's role sets in its defaults/main.yml. The pages are
corrected, never the ports: a role's defaults are the truth.

    python3 -m unittest discover -s tests -p 'test_*.py'
"""

import re
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DOCS = REPO / "website" / "docs" / "applications"
ROLES = REPO / "roles"

ADDRESS = re.compile(r"ansible_nas_host_or_ip:(\d+)")

# Pages whose role does not carry the page's name. A page may cover more than one role.
PAGE_ROLES = {
    "monitoring/speedtest.md": ["speedtest-tracker"],
    "observability/grafana.md": ["stats"],
    "download-tools/transmission.md": ["transmission", "transmission-with-openvpn"],
}


def normal(name):
    """A name with its case, dashes and underscores taken away, to match a page to its role."""
    return re.sub(r"[-_]", "", name).lower()


def role_ports(role):
    """The port numbers a role's defaults name (host side or container side of a mapping)."""
    defaults = ROLES / role / "defaults" / "main.yml"
    values = yaml.safe_load(defaults.read_text()) or {}
    ports = set()
    for key, value in values.items():
        if "port" in key.lower():
            ports.update(re.findall(r"\d+", str(value)))
    return ports


def roles_of(page):
    """The role directories a page documents."""
    relative = page.relative_to(DOCS).as_posix()
    if relative in PAGE_ROLES:
        return PAGE_ROLES[relative]
    stem = page.stem
    return [
        role.name for role in ROLES.iterdir()
        if role.is_dir() and normal(role.name) == normal(stem)
    ]


def disagreements(text, ports):
    """The addresses in a page whose port is not one of the given ports."""
    return sorted({port for port in ADDRESS.findall(text) if port not in ports})


class TheApplicationDocs(unittest.TestCase):
    def test_every_address_names_a_port_its_role_defaults_to(self):
        pages = sorted(DOCS.rglob("*.md"))
        self.assertTrue(pages, "no application pages found")
        for page in pages:
            text = page.read_text()
            if not ADDRESS.search(text):
                continue
            with self.subTest(page=page.relative_to(REPO).as_posix()):
                roles = roles_of(page)
                self.assertTrue(roles, "no role for this page")
                ports = set()
                for role in roles:
                    ports |= role_ports(role)
                wrong = disagreements(text, ports)
                self.assertEqual(
                    wrong, [],
                    f"addresses on ports {wrong} are not defaults of {roles}",
                )

    def test_a_page_with_a_wrong_port_is_caught(self):
        text = "Open [http://ansible_nas_host_or_ip:8080](http://ansible_nas_host_or_ip:8080)."
        self.assertEqual(disagreements(text, {"9382"}), ["8080"])
        self.assertEqual(disagreements(text, {"8080"}), [])


if __name__ == "__main__":
    unittest.main()
