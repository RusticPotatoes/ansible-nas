# guacamole

Runs Apache Guacamole, a clientless remote desktop gateway for VNC, RDP and SSH, in a container.

Web interface: port `8090` (`guacamole_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `guacamole_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `guacamole_available_externally` | `false` | Lets Traefik route `guacamole_hostname`.`ansible_nas_domain` to it. |
| `guacamole_data_directory` | `"{{ docker_home }}/guacamole"` | Holds `config/`, mounted at `/config`. |
| `guacamole_port` | `"8090"` | Host port published to the container's port 8080. |
| `guacamole_hostname` | `"guacamole"` | Subdomain Traefik uses when it is available externally. |
| `guacamole_container_name` | `"guacamole"` | Name of the Docker container. |
| `guacamole_image_name` | `"oznu/guacamole"` | Docker image. |
| `guacamole_image_version` | `"latest"` | Image tag. |
| `guacamole_memory` | `1g` | Container memory limit. |

The tasks remove the old `guacamole-mysql` and `guacamole-guacd` containers and the old `mysql/` folder of earlier versions of this role, and restart the container after starting it.

Application page: `website/docs/applications/other/guacamole.md`.

Tests: a molecule scenario in `molecule/`.
