# sonarr

Runs Sonarr, the TV series manager: it watches for new episodes, sends them to a download
client and files the finished downloads into the TV library. It runs in a container.

Web interface: port `8989` (`sonarr_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `sonarr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `sonarr_available_externally` | `false` | Lets Traefik route `sonarr_hostname`.`ansible_nas_domain` to it. |
| `sonarr_data_directory` | `"{{ docker_home }}/sonarr/config"` | Sonarr's configuration, mounted at `/config`. |
| `sonarr_tv_directory` | `"{{ tv_root }}"` | The TV library, mounted at `/tv`. |
| `sonarr_download_directory` | `"{{ downloads_root }}"` | Completed downloads, mounted at `/downloads`. |
| `sonarr_user_id` | `"0"` | User the container runs as (`PUID`) and owner of its folders. |
| `sonarr_group_id` | `"0"` | Group the container runs as (`PGID`) and group of its folders. |
| `sonarr_port` | `"8989"` | Host port published to the container's port 8989. |
| `sonarr_hostname` | `"sonarr"` | Subdomain Traefik uses when it is available externally. |
| `sonarr_container_name` | `"sonarr"` | Name of the Docker container. |
| `sonarr_image_name` | `"linuxserver/sonarr"` | Docker image. |
| `sonarr_image_version` | `"latest"` | Image tag. |
| `sonarr_memory` | `1g` | Container memory limit. |

The tasks also read two optional variables that have no default here: `sonarr_vpn_enabled`
(falls back to `vpn_download_stack_enabled`; when on, Sonarr joins gluetun's network and
publishes no port of its own) and `sonarr_api_key` (for the Homepage widget, empty if unset).

Application page: `website/docs/applications/download-tools/sonarr.md`.

Tests: a molecule scenario in `molecule/`.
