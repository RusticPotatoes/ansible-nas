# mealie

Runs Mealie, a self-hosted recipe manager and meal planner, in a container.

Web interface: port `9925` (`mealie_port`), published to the container's port 9000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mealie_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `mealie_available_externally` | `false` | Lets Traefik route `mealie_hostname`.`ansible_nas_domain` to it. |
| `mealie_data_directory` | `"{{ docker_home }}/mealie"` | Mealie's data, mounted at `/app/data`. |
| `mealie_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `mealie_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `mealie_hostname` | `"mealie"` | Subdomain Traefik uses when it is available externally. |
| `mealie_port` | `"9925"` | Host port published to the container's port 9000. |
| `mealie_container_name` | `"mealie"` | Name of the Docker container. |
| `mealie_image_name` | `"hkotel/mealie"` | Docker image. |
| `mealie_image_version` | `"latest"` | Image tag. |
| `mealie_memory` | `1g` | Container memory limit. |

Recipe display settings (public recipes, nutrition, assets, comments) are set in the tasks.

Application page: `website/docs/applications/other/mealie.md`.

Tests: a molecule scenario in `molecule/`.
