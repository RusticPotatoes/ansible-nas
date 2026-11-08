# prowlarr

Runs Prowlarr, an indexer manager for Usenet indexers and torrent trackers, in a container. It keeps the indexers in one place and hands them to Sonarr, Radarr, Lidarr and Readarr.

Web interface: port `9696` (`prowlarr_port`). When `vpn_download_stack_enabled` is on, Prowlarr joins gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `prowlarr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `prowlarr_available_externally` | `false` | Lets Traefik route `prowlarr_hostname`.`ansible_nas_domain` to it. |
| `prowlarr_data_directory` | `"{{ docker_home }}/prowlarr/config"` | Prowlarr's configuration, mounted at `/config`. |
| `prowlarr_user_id` | `"0"` | User the container runs as (`PUID`) and owner of its folder. |
| `prowlarr_group_id` | `"0"` | Group the container runs as (`PGID`) and group of its folder. |
| `prowlarr_port` | `"9696"` | Host port published to the container's port 9696. |
| `prowlarr_hostname` | `"prowlarr"` | Subdomain Traefik uses when it is available externally. |
| `prowlarr_container_name` | `"prowlarr"` | Name of the Docker container. |
| `prowlarr_image_name` | `"ghcr.io/linuxserver/prowlarr"` | Docker image. |
| `prowlarr_image_version` | `"develop"` | Image tag. |
| `prowlarr_memory` | `1g` | Container memory limit. |

The Homepage widget reads the optional `prowlarr_api_key` (no default here; empty if unset). Set it in your own vars, never in git.

Application page: `website/docs/applications/download-tools/prowlarr.md`.

Tests: a molecule scenario in `molecule/`.
