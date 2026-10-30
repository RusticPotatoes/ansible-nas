# minecraft-server

Runs a Minecraft (Java edition) server in a container.

Game: port `25565` (`minecraft_server_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `minecraft_server_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `minecraft_server_data_directory` | `"{{ docker_home }}/minecraft_server"` | Server data, mounted at `/data`. |
| `minecraft_server_port` | `"25565"` | Host port published to the container's port 25565. |
| `minecraft_server_container_name` | `"minecraft-server"` | Name of the Docker container. |
| `minecraft_server_image_name` | `"itzg/minecraft-server"` | Docker image. |
| `minecraft_server_image_version` | `"latest"` | Image tag. |

The tasks accept the Minecraft EULA (`EULA: TRUE`). The container has no memory limit and no Traefik route.

Application page: `website/docs/applications/gaming/minecraft-server.md`.

Tests: a molecule scenario in `molecule/`.
