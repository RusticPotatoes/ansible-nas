# dashy

Runs Dashy, a customisable self-hosted dashboard, in a container (`lissy93/dashy:latest`).

Web interface: port `8082` (`dashy_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `dashy_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `dashy_available_externally` | `false` | Lets Traefik route `dashy_hostname`.`ansible_nas_domain` to it. |
| `dashy_data_directory` | `"{{ docker_home }}/dashy"` | Holds `conf.yml`, the dashboard's configuration, mounted at `/app/public/conf.yml`. A starter copy from the role's `files/` is written only if none exists. |
| `dashy_port` | `"8082"` | Host port published to the container's port 80. |
| `dashy_hostname` | `"dashy"` | Subdomain Traefik uses when it is available externally. |
| `dashy_memory` | `2g` | Container memory limit. |
| `dashy_container_name` | `dashy` | Name of the Docker container. |

The image is `lissy93/dashy:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/dashboards/dashy.md`.

Tests: a molecule scenario in `molecule/`.
