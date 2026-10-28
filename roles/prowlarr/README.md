# prowlarr

Runs Prowlarr, an indexer manager for Usenet indexers and torrent trackers, in a container. It
keeps the indexers in one place and hands them to Sonarr, Radarr, Lidarr and Readarr.

Port: the web UI on `9696` (`prowlarr_port`). When `vpn_download_stack_enabled` is true,
Prowlarr runs in gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it does |
| --- | --- | --- |
| `prowlarr_enabled` | `false` | Start Prowlarr; `false` removes the container. |
| `prowlarr_available_externally` | `false` | Route `prowlarr_hostname` through Traefik. |
| `prowlarr_data_directory` | `"{{ docker_home }}/prowlarr/config"` | Config, mounted at `/config`. |
| `prowlarr_user_id` | `"0"` | UID the app runs as (`PUID`). |
| `prowlarr_group_id` | `"0"` | GID the app runs as (`PGID`). |
| `prowlarr_port` | `"9696"` | Host port of the web UI. |
| `prowlarr_hostname` | `"prowlarr"` | Traefik hostname, under `ansible_nas_domain`. |
| `prowlarr_container_name` | `"prowlarr"` | Container name. |
| `prowlarr_image_name` | `"ghcr.io/linuxserver/prowlarr"` | Image. |
| `prowlarr_image_version` | `"develop"` | Image tag. |
| `prowlarr_memory` | `1g` | Memory limit. |

The Homepage widget reads `prowlarr_api_key` (default empty). Set it in your own vars, never in
git.

Application page: `website/docs/applications/download-tools/prowlarr.md`.

Tests: a molecule scenario in `molecule/`.
