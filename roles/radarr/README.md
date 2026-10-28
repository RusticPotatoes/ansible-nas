# radarr

Runs Radarr, the movie collection manager: it watches for wanted films, sends them to a
download client and files the finished downloads into the movie library. It runs in a
container.

Web interface: port `7878` (`radarr_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `radarr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `radarr_available_externally` | `false` | Lets Traefik route `radarr_hostname`.`ansible_nas_domain` to it. |
| `radarr_movies_directory` | `"{{ movies_root }}"` | The movie library, mounted at `/movies`. |
| `radarr_download_directory` | `"{{ downloads_root }}"` | Completed downloads, mounted at `/downloads`. |
| `radarr_data_directory` | `"{{ docker_home }}/radarr"` | Radarr's configuration, mounted at `/config`. |
| `radarr_user_id` | `"0"` | User the container runs as (`PUID`) and owner of its folders. |
| `radarr_group_id` | `"0"` | Group the container runs as (`PGID`) and group of its folders. |
| `radarr_port` | `"7878"` | Host port published to the container's port 7878. |
| `radarr_hostname` | `"radarr"` | Subdomain Traefik uses when it is available externally. |
| `radarr_container_name` | `"radarr"` | Name of the Docker container. |
| `radarr_image_name` | `"linuxserver/radarr"` | Docker image. |
| `radarr_image_version` | `"latest"` | Image tag. |
| `radarr_memory` | `1g` | Container memory limit. |

The tasks also read two optional variables that have no default here: `radarr_vpn_enabled`
(falls back to `vpn_download_stack_enabled`; when on, Radarr joins gluetun's network and
publishes no port of its own) and `radarr_api_key` (for the Homepage widget, empty if unset).

Application page: `website/docs/applications/download-tools/radarr.md`.

Tests: a molecule scenario in `molecule/`.
