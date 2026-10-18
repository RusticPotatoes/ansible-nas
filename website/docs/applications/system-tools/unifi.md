---
title: "UniFi Network Application"
---

Homepage: [https://ui.com/](https://ui.com/)

The UniFi Network Application manages UniFi network devices.

## Usage

Set `unifi_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

* Web interface: port `8443` (`unifi_port`), hostname `unifi_hostname` (default `unifi`)
* Config directory: `unifi_config_directory` (default `<docker_home>/unifi/config`)
* Image: `lscr.io/linuxserver/unifi-network-application`, version `unifi_image_version` (default `latest`)
* Log level: `unifi_log_level` (default `error`)
* Memory limit: `unifi_memory` (default `1g`)
* Container name: `unifi_container_name` (default `unifi`)

Available externally through Traefik only if `unifi_available_externally: true`.

**For more info visit: [https://docs.linuxserver.io/images/docker-unifi-network-application/](https://docs.linuxserver.io/images/docker-unifi-network-application/)**
