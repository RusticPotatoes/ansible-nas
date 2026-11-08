# homeassistant

Runs Home Assistant, open source home automation that puts local control first, in a container.

Web interface: port `8123` (`homeassistant_port`). The container uses the host's network (`network_mode: host`), so Home Assistant listens on the host directly.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `homeassistant_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `homeassistant_available_externally` | `false` | Lets Traefik route `homeassistant_hostname`.`ansible_nas_domain` to it. |
| `homeassistant_data_directory` | `"{{ docker_home }}/homeassistant"` | Holds `config/`, mounted at `/config`. |
| `homeassistant_port` | `"8123"` | Port of the web interface (container port 8123). The tasks publish it, but on the host's network the container's own port is what listens. |
| `homeassistant_hostname` | `"homeassistant"` | Subdomain Traefik uses when it is available externally. |
| `homeassistant_container_name` | `"homeassistant"` | Name of the Docker container. |
| `homeassistant_image_name` | `"homeassistant/home-assistant"` | Docker image. |
| `homeassistant_image_version` | `latest` | Image tag. |
| `homeassistant_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/home-automation/homeassistant.md`.

Tests: a molecule scenario in `molecule/`.
