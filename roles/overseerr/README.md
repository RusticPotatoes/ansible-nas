# overseerr

Runs Overseerr, an application for managing requests for your media library that works with Sonarr, Radarr and Plex, in a container.

Web interface: port `5055` (`overseerr_webui_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `overseerr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `overseerr_available_externally` | `false` | Lets Traefik route `overseerr_hostname`.`ansible_nas_domain` to it. |
| `overseerr_data_directory` | `"{{ docker_home }}/overseerr"` | Its `config/` subfolder is mounted at `/app/config`. |
| `overseerr_container_name` | `"overseerr"` | Name of the Docker container. |
| `overseerr_image_name` | `"sctx/overseerr"` | Docker image. |
| `overseerr_image_version` | `"latest"` | Image tag. |
| `overseerr_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `overseerr_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `overseerr_webui_port` | `"5055"` | Host port published to the container's port 5055. |
| `overseerr_hostname` | `"overseerr"` | Subdomain Traefik uses when it is available externally. |
| `overseerr_memory` | `1g` | Container memory limit. |

The Homepage widget reads the optional `overseerr_api_key` (no default here; empty if unset). Set it in your own vars, never in git.

Application page: `website/docs/applications/download-tools/overseerr.md`.

Tests: a molecule scenario in `molecule/`.
