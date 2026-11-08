# newspaper

Runs the `newspaper` app from the `rusticpotato/newspaper` image in a container. Homepage lists it under Download Tools.

Port: `7000` (`newspaper_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `newspaper_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `newspaper_available_externally` | `false` | Lets Traefik route `newspaper_hostname`.`ansible_nas_domain` to it. |
| `newspaper_data_directory` | `"{{ docker_home }}/newspaper"` | App data, mounted at `/config`. |
| `newspaper_user_id` | `"0"` | User the container runs as (`PUID`). |
| `newspaper_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `newspaper_port` | `"7000"` | Host port published to the container's port 8080. |
| `newspaper_hostname` | `"newspaper"` | Subdomain Traefik uses when it is available externally. |
| `newspaper_container_name` | `"newspaper"` | Name of the Docker container. |
| `newspaper_image_name` | `"rusticpotato/newspaper"` | Docker image. |
| `newspaper_image_version` | `"latest"` | Image tag. |
| `newspaper_memory` | `1g` | Container memory limit. |

Traefik's route points at container port 8787, while the container's published port is 8080. `defaults/main.yml` also has commented-out books and download directories; the tasks do not use them.

Application page: none yet under `website/docs/applications/`.

Tests: a molecule scenario in `molecule/`.
