# glances

Runs Glances, a cross-platform system monitoring tool, in web mode in a container. It sees the host's processes (`pid_mode: host`) and the Docker socket, read-only.

Ports: web interface `61208` (`glances_port_one`) and `61209` (`glances_port_two`), each published to the same container port.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `glances_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `glances_available_externally` | `false` | Lets Traefik route `glances_hostname`.`ansible_nas_domain` to it. |
| `glances_hostname` | `"glances"` | Subdomain Traefik uses when it is available externally. |
| `glances_port_one` | `"61208"` | Host port published to the container's port 61208 (web interface). |
| `glances_port_two` | `"61209"` | Host port published to the container's port 61209. |
| `glances_security_options` | see below | Docker security options of the container. |
| `glances_container_name` | `"glances"` | Name of the Docker container. |
| `glances_image_name` | `"nicolargo/glances"` | Docker image. |
| `glances_image_version` | `"latest"` | Image tag. |
| `glances_memory` | `1g` | Container memory limit. |

Default of `glances_security_options`:

```yaml
glances_security_options:
  - "apparmor=unconfined"
```

Application page: `website/docs/applications/monitoring/glances.md`.

Tests: a molecule scenario in `molecule/`.
