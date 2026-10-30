# gotify

Runs Gotify, a server for sending and receiving messages in real time over WebSocket, with a web UI, in a container.

Web interface: port `2346` (`gotify_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `gotify_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `gotify_available_externally` | `false` | Lets Traefik route `gotify_hostname`.`ansible_nas_domain` to it. |
| `gotify_data_directory` | `"{{ docker_home }}/gotify"` | Gotify's data, mounted at `/app/data`. |
| `gotify_port` | `"2346"` | Host port published to the container's port 80. |
| `gotify_hostname` | `"gotify"` | Subdomain Traefik uses when it is available externally. |
| `gotify_container_name` | `"gotify"` | Name of the Docker container. |
| `gotify_image_name` | `"gotify/server"` | Docker image. |
| `gotify_image_version` | `"latest"` | Image tag. |
| `gotify_user_id` | `"0"` | User the container runs as (`PUID`). |
| `gotify_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `gotify_memory` | `200m` | Container memory limit. |

The container also mounts the Docker socket (`/var/run/docker.sock`).

Application page: `website/docs/applications/other/gotify.md`.

Tests: a molecule scenario in `molecule/`.
