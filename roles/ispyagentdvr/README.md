# ispyagentdvr

Runs iSpy Agent DVR, video surveillance software, in a container.

Ports: web interface `8097` (`ispyagentdvr_webui_port`, published to the container's port 8090), TURN `3478/udp` (`ispyagentdvr_turn_port`) and the UDP range `50000-50010` (`ispyagentdvr_agentdvr_host_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ispyagentdvr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `ispyagentdvr_available_externally` | `false` | Lets Traefik route `ispyagentdvr_hostname`.`ansible_nas_domain` to it. |
| `ispyagentdvr_config_directory` | `"{{ docker_home }}/ispyagentdvr/config"` | Configuration, mounted at `/AgentDVR/Media/XML`. |
| `ispyagentdvr_commands_directory` | `"{{ docker_home }}/ispyagentdvr/commands"` | Commands, mounted at `/AgentDVR/Commands`. |
| `ispyagentdvr_recordings_directory` | `"{{ downloads_root }}/recordings"` | Recordings, mounted at `/AgentDVR/Media/WebServerRoot/Media`. |
| `ispyagentdvr_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `ispyagentdvr_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `ispyagentdvr_webui_port` | `"8097"` | Host port published to the container's port 8090; also passed as `WEBUI_PORT`. |
| `ispyagentdvr_turn_port` | `"3478"` | Host port published to the container's port 3478/udp (TURN). |
| `ispyagentdvr_agentdvr_host_port` | `"50000-50010"` | Host UDP port range published to the container's 50000-50010/udp. |
| `ispyagentdvr_memory` | `1g` | Container memory limit. |
| `ispyagentdvr_container_name` | `ispyagentdvr` | Name of the Docker container. |

The image is `mekayelanik/ispyagentdvr:latest` and the Traefik hostname is `ispyagentdvr`, both set in the tasks rather than in defaults. The role's own `docs/ispyagentdvr.md` describes it.

Application page: none yet under `website/docs/applications/`.

Tests: a molecule scenario in `molecule/`.
