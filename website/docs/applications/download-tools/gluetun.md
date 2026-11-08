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
* Image: `qmcgaw/gluetun`, version `gluetun_image_version` (default `v3.41.3`, pinned: see [Updates](#updates))

Optional periodic restart of the whole stack: `gluetun_periodic_restart_enabled` (default `false`) with `gluetun_periodic_restart_interval` (default `2h`), one of the [scheduled jobs on the NAS](../../further-configuration/scheduled-jobs.md). Recovery through ansible is controlled by `gluetun_recover_with_ansible_enabled` (default `true`).

Available externally through Traefik only if `gluetun_available_externally: true`.

## Updates

Watchtower leaves the VPN stack alone, and the playbook updates it as one unit.

Gluetun carries the label `com.centurylinklabs.watchtower.enable: "false"`, and so does every
container on its network: the [VPN download stack](../stacks/vpn-download-stack.md)'s apps
(prowlarr, deluge, nzbget, radarr, sonarr, readarr, jackett, sabnzbd), flaresolverr, and gatus with
`gatus_use_vpn`. The label follows the same switch as the container's `network_mode`, so an app
off gluetun's network gets `"true"` (Watchtower's default) and is updated nightly as before.

Why: a container on gluetun's network joins it by gluetun's container id. When Watchtower
recreated gluetun with a newer image, those containers were left on a network that no longer
existed ("joining network namespace of container: No such container"), and downloads stalled.

How the stack is updated now: run the `gluetun` tag, `make run TAGS=gluetun` (or
`make run-remote TAGS=gluetun` from a laptop). It runs gluetun's role first, which stops the routed
containers and recreates gluetun if its image or settings changed, then every role that can join
its network. Each of those sees gluetun's new id and recreates its container on the new network.

The images are pinned to releases, so nothing changes until a tag is bumped. To bump one:

1. Find the new release tag on the registry (Docker Hub; ghcr.io for prowlarr and readarr). For
   linuxserver images prefer the full build tag, such as `1.2.3.4567-ls100`.
2. Set the app's `<app>_image_version` in your inventory (or change it in the role's
   `defaults/main.yml`): `gluetun_image_version`, `prowlarr_image_version`,
   `deluge_image_version`, `nzbget_image_version`, `radarr_image_version`,
   `sonarr_image_version`, `readarr_image_version`, `jackett_image_version`,
   `sabnzbd_image_version`, `flaresolverr_image_version`.
3. Run `make run TAGS=gluetun`.

Gatus is not pinned (`gatus_image_version` stays `latest`): off the VPN Watchtower updates it, and
on the VPN it takes the newest image whenever the `gluetun` tag runs.

**For more info visit: [https://github.com/qdm12/gluetun-wiki](https://github.com/qdm12/gluetun-wiki)**
