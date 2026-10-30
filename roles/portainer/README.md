# portainer

Runs Portainer CE, a web interface to manage Docker containers, in a container, with read-only access to the Docker socket.

Web interface: port `9000` (`portainer_port`), in HTTP mode (`--http-enabled`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `portainer_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `portainer_available_externally` | `false` | Lets Traefik route `portainer_hostname`.`ansible_nas_domain` to it. |
| `portainer_data_directory` | `"{{ docker_home }}/portainer/config"` | Portainer's data, mounted at `/data`. |
| `portainer_port` | `"9000"` | Host port published to the container's port 9000. |
| `portainer_hostname` | `"portainer"` | Subdomain Traefik uses when it is available externally. |
| `portainer_ip_allowlist` | `"0.0.0.0/0"` | Source addresses Traefik lets through to Portainer (an IP allowlist middleware). The default lets everyone through. |
| `portainer_container_name` | `"portainer"` | Name of the Docker container. |
| `portainer_image_name` | `"portainer/portainer-ce"` | Docker image. |
| `portainer_image_version` | `"latest"` | Image tag. |
| `portainer_memory` | `1g` | Container memory limit. |

The old `portainer_ip_whitelist` is refused: the play fails if it is set, and asks for `portainer_ip_allowlist` instead.

Application page: `website/docs/applications/system-tools/portainer.md`.

Tests: a molecule scenario in `molecule/`.
