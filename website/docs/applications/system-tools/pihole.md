---
title: "Pi-hole"
---

Homepage: [https://pi-hole.net/](https://pi-hole.net/)

Pi-hole is a network-wide DNS ad blocker.

## Usage

Set `pihole_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

* Web interface: port `8443` (`pihole_port`), hostname `pihole_hostname` (default `pihole`)
* Config directory: `pihole_config_directory` (default `<docker_home>/pihole/config`)
* dnsmasq directory: `pihole_dnsmasq_directory` (default `<docker_home>/pihole/dnsmasq`)
* Web password: `pihole_web_password`, taken from `vault_pihole_web_password` if set
* Log level: `pihole_log_level` (default `error`)
* Memory limit: `pihole_memory` (default `1g`)
* Container name: `pihole_container_name` (default `pihole`)

Available externally through Traefik only if `pihole_available_externally: true`.

**For more info visit: [https://docs.pi-hole.net/](https://docs.pi-hole.net/)**
