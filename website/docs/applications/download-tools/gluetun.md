---
title: "Gluetun"
---

Homepage: [https://github.com/qdm12/gluetun](https://github.com/qdm12/gluetun)

Gluetun is a VPN client container that other containers can route their traffic through.

## Usage

Set `gluetun_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

Containers listed in `gluetun_routed_containers` run in gluetun's network, so they stop when gluetun restarts and come back with it.

* Web UI / control server (optional): port `8000` (`gluetun_http_port`, default `8000:8000`)
* Internal DNS: port `53` (`gluetun_dns_port`)
* Traefik hostname: `gluetun_hostname` (default `vpn`) under `ansible_nas_domain`
* Config directory: `gluetun_config_directory` (default `<docker_home>/gluetun`)
* Memory limit: `gluetun_memory` (default `512m`)
* Image: `qmcgaw/gluetun`, version `gluetun_image_version` (default `latest`)

Optional periodic restart of the whole stack: `gluetun_periodic_restart_enabled` (default `false`) with `gluetun_periodic_restart_interval` (default `2h`). Recovery through ansible is controlled by `gluetun_recover_with_ansible_enabled` (default `true`).

Available externally through Traefik only if `gluetun_available_externally: true`.

**For more info visit: [https://github.com/qdm12/gluetun-wiki](https://github.com/qdm12/gluetun-wiki)**
