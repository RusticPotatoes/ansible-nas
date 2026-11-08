# lidarr

Runs Lidarr, a music collection manager for Usenet and BitTorrent users: it watches for new tracks from your artists, grabs them, and sorts and renames them. It runs in a container.

Web interface: port `8686` (`lidarr_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `lidarr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `lidarr_available_externally` | `false` | Lets Traefik route `lidarr_hostname`.`ansible_nas_domain` to it. |
| `lidarr_data_directory` | `"{{ docker_home }}/lidarr/config"` | Lidarr's configuration, mounted at `/config`. |
| `lidarr_music_directory` | `"{{ music_root }}"` | Music library, mounted at `/music`. |
| `lidarr_downloads_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `lidarr_user_id` | `"0"` | User the container runs as (`PUID`). |
| `lidarr_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `lidarr_port` | `"8686"` | Host port published to the container's port 8686. |
| `lidarr_hostname` | `"lidarr"` | Subdomain Traefik uses when it is available externally. |
| `lidarr_container_name` | `"lidarr"` | Name of the Docker container. |
| `lidarr_image_name` | `"linuxserver/lidarr"` | Docker image. |
| `lidarr_image_version` | `"latest"` | Image tag. |
| `lidarr_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/download-tools/lidarr.md`.

Tests: a molecule scenario in `molecule/`.
