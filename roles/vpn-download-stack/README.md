# vpn-download-stack

Turns on a set of download tools that run through the shared Gluetun VPN container. It runs no container of its own: it switches the other roles on or off and tells the `gluetun` role which containers to route, so Gluetun publishes their ports while they share its network.

No port of its own. Gluetun publishes each routed app's port: Prowlarr `9696`, Deluge `8112`, Radarr `7878`, Sonarr `8989`, NZBGet `6789`, Readarr `8787`, Jackett `9117` and SABnzbd `8080` inside the container (each app's `<app>_port` on the host).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `vpn_download_stack_enabled` | `false` | When `true`, turns on `gluetun` and the apps chosen below and builds `gluetun_routed_containers`. When `false`, turns off gluetun and all eight apps and empties `gluetun_routed_containers`. |
| `vpn_download_stack_prowlarr_enabled` | `true` | Turn on Prowlarr with the stack. |
| `vpn_download_stack_deluge_enabled` | `true` | Turn on Deluge with the stack. |
| `vpn_download_stack_radarr_enabled` | `true` | Turn on Radarr with the stack. |
| `vpn_download_stack_sonarr_enabled` | `true` | Turn on Sonarr with the stack. |
| `vpn_download_stack_nzbget_enabled` | `true` | Turn on NZBGet with the stack. |
| `vpn_download_stack_readarr_enabled` | `false` | Turn on Readarr with the stack. |
| `vpn_download_stack_jackett_enabled` | `false` | Turn on Jackett with the stack. |
| `vpn_download_stack_sabnzbd_enabled` | `false` | Turn on SABnzbd with the stack. |

An app already enabled by its own `<app>_enabled` stays on and is routed too. Radarr and Sonarr are routed only while `radarr_vpn_enabled` / `sonarr_vpn_enabled` (default `true`) are on. Note that turning the stack off also sets `<app>_enabled` to `false` for all eight apps, whatever their own setting.

Application page: `website/docs/applications/stacks/vpn-download-stack.md`.
