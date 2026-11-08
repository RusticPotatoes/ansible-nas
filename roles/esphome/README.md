# esphome

Runs ESPHome, which configures and controls ESP8266/ESP32 boards through simple configuration files, in a container (`esphome/esphome:latest`).

Web interface: port `6052` (`esphome_port`). ESPHome has no security of its own, so making it available externally is not advised.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `esphome_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `esphome_available_externally` | `false` | Lets Traefik route `esphome_hostname`.`ansible_nas_domain` to it. |
| `esphome_data_directory` | `"{{ docker_home }}/esphome"` | ESPHome's configuration, mounted at `/config`. |
| `esphome_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `esphome_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `esphome_hostname` | `"esphome"` | Subdomain Traefik uses when it is available externally. |
| `esphome_port` | `"6052"` | Host port published to the container's port 6052. |
| `esphome_memory` | `1g` | Container memory limit. |
| `esphome_container_name` | `esphome` | Name of the Docker container. |

The image is `esphome/esphome:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/home-automation/esphome.md`.

Tests: a molecule scenario in `molecule/`.
