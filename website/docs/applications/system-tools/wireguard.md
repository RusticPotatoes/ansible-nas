---
title: "WireGuard"
---

Homepage: [https://www.wireguard.com/](https://www.wireguard.com/)

WireGuard is a fast, modern VPN.

## Usage

Set `wireguard_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

* UDP port: `51820` (`wireguard_udp_port`); forward it on your router
* Data directory: `wireguard_data_directory` (default `<docker_home>/wireguard`)
* Peers (clients): `wireguard_peers` (default `3`)
* VPN subnet: `wireguard_subnet` (default `10.0.0.0`; server is .1, peers .2 and up)
* Allowed IPs: `wireguard_allowed_ips` (default `0.0.0.0/0`, all traffic through the VPN)
* Image: `linuxserver/wireguard`, version `wireguard_image_version` (default `latest`)
* Memory limit: `wireguard_memory` (default `512m`)
* Container name: `wireguard_container_name` (default `wireguard`)

Peer configs and QR codes are written under the data directory.

**For more info visit: [https://docs.linuxserver.io/images/docker-wireguard/](https://docs.linuxserver.io/images/docker-wireguard/)**
