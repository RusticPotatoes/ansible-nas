# minecraft-bedrock-server

Runs a Minecraft Bedrock edition server in a container.

Game: port `19132/udp` (`minecraft_bedrock_server_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `minecraft_bedrock_server_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `minecraft_bedrock_server_data_directory` | `"{{ docker_home }}/minecraft_bedrock_server"` | Server data, mounted at `/data`. |
| `minecraft_bedrock_server_port` | `"19132"` | Host port published to the container's port 19132/udp. |
| `minecraft_bedrock_server_container_name` | `minecraft-bedrock-server` | Name of the Docker container. |
| `minecraft_bedrock_server_image` | `itzg/minecraft-bedrock-server` | Docker image (no tag, so `latest`). |
| `minecraft_bedrock_server_name` | `"Ansible-NAS Minecraft Server"` | Server name (`SERVER_NAME`). |
| `minecraft_bedrock_server_game_mode` | `"creative"` | Game mode (`GAMEMODE`). |
| `minecraft_bedrock_server_difficulty` | `"normal"` | Difficulty (`DIFFICULTY`). |
| `minecraft_bedrock_server_online_mode` | `"false"` | Online mode (`ONLINE_MODE`). |
| `minecraft_bedrock_server_ops` | `""` | Comma-separated XUIDs of server operators (`OPS`). |
| `minecraft_bedrock_server_members` | `""` | Comma-separated list of server members (`MEMBERS`). |
| `minecraft_bedrock_server_visitors` | `""` | Comma-separated list of server visitors (`VISITORS`). |

The tasks accept the Minecraft EULA (`EULA: TRUE`). The container has no memory limit and no Traefik route.

Application page: `website/docs/applications/gaming/minecraft-bedrock-server.md`.
