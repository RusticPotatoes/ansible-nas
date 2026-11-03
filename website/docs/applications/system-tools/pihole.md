---
title: "Pi-hole"
---

Homepage: [https://pi-hole.net/](https://pi-hole.net/)

Pi-hole is a network-wide DNS ad blocker.

## Usage

Set `pihole_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file, and set `pihole_macvlan_address` to the LAN address Pi-hole should take. The role stops with a message naming it if it is unset while `pihole_enabled` is true.

The web interface is served on port 80 at `pihole_macvlan_address` (`/admin`); DNS on port 53 is served at the same address. Homepage links point there.

## Variables

| Variable | Default | What it sets |
| --- | --- | --- |
| `pihole_enabled` | `false` | Create and run the container (`true`), or remove it (`false`) |
| `pihole_macvlan_address` | none (must be set) | Pi-hole's address on the macvlan network; also used in the Homepage links |
| `pihole_container_name` | `pihole` | Name of the container |
| `pihole_config_directory` | `<docker_home>/pihole/config` | Config directory, mounted at `/etc/pihole` |
| `pihole_dnsmasq_directory` | `<docker_home>/pihole/dnsmasq` | dnsmasq directory, mounted at `/etc/dnsmasq.d` |
| `pihole_web_password` | taken from `vault_pihole_web_password`, else empty | Web interface password |
| `pihole_timezone` | `ansible_nas_timezone` | Container time zone |
| `pihole_memory` | `1g` | Memory limit |
| `pihole_dns_hosts` | `[]` | Local DNS records, `"<address> <name>"` each; empty leaves the list to the Pi-hole UI |
| `pihole_rev_servers` | `[]` | Router reverse-lookup forwarding, `"true,<LAN CIDR>,<router>,<domain>"` each; empty: none |

**For more info visit: [https://docs.pi-hole.net/](https://docs.pi-hole.net/)**
