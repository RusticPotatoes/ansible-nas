# tautulli

Runs Tautulli, which monitors a Plex Media Server, in a container.

Web interface: port `8185` (`tautulli_port`), published to the container's port 8181.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `tautulli_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `tautulli_available_externally` | `false` | Lets Traefik route `tautulli_hostname`.`ansible_nas_domain` to it. |
| `tautulli_config_directory` | `"{{ docker_home }}/tautulli/config"` | Tautulli's configuration, mounted at `/config`. |
| `tautulli_user_id` | `"0"` | User the container runs as (`PUID`). |
| `tautulli_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `tautulli_hostname` | `"tautulli"` | Subdomain Traefik uses when it is available externally. |
| `tautulli_port` | `"8185"` | Host port published to the container's port 8181. |
| `tautulli_container_name` | `"tautulli"` | Name of the Docker container. |
| `tautulli_image_name` | `"linuxserver/tautulli"` | Docker image. |
| `tautulli_image_version` | `"latest"` | Image tag. |
| `tautulli_memory` | `"1g"` | Container memory limit. |

The tasks also mount Plex's logs from `plex_logs` (a variable of the `plex` role) read-only at `/logs`, and create that folder if it is missing.

Application page: `website/docs/applications/media-serving/tautulli.md`.

Tests: a molecule scenario in `molecule/`.
