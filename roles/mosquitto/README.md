# mosquitto

Runs Mosquitto, a lightweight open source MQTT message broker, in a container.

Ports: MQTT on `1883` (`mosquitto_port_a`) and `9001` (`mosquitto_port_b`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mosquitto_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `mosquitto_data_directory` | `"{{ docker_home }}/mosquitto"` | Holds `config/mosquitto.conf`, `data/` and `log/`, mounted under `/mosquitto`. |
| `mosquitto_user_id` | `"0"` | User ID. Not used by the tasks yet. |
| `mosquitto_group_id` | `"0"` | Group ID. Not used by the tasks yet. |
| `mosquitto_port_a` | `"1883"` | Host port published to the container's port 1883 (MQTT). |
| `mosquitto_port_b` | `"9001"` | Host port published to the container's port 9001. |
| `mosquitto_container_name` | `"mosquitto"` | Name of the Docker container. |
| `mosquitto_image_name` | `"eclipse-mosquitto"` | Docker image. |
| `mosquitto_image_version` | `"latest"` | Image tag. |
| `mosquitto_memory` | `1g` | Memory limit. Not used by the tasks yet: the container's limit is set to `1g` in the tasks. |

The role copies `files/mosquitto.conf` into the config folder: it keeps data in `/mosquitto/data/`, logs to a file and to stdout, listens on 1883 and allows anonymous clients. The container restarts when that file changes.

Application page: `website/docs/applications/home-automation/mosquitto.md`.

Tests: a molecule scenario in `molecule/`.
