# gatus

Runs Gatus, a synthetic monitoring tool: it health-checks services, shows a status dashboard and can alert when checks fail. It runs in a container.

Web interface: port `9382` (`gatus_port`), published to the container's port 8080. With `gatus_use_vpn` on, Gatus joins gluetun's network and publishes no port of its own.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `gatus_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `gatus_available_externally` | `false` | Lets Traefik route `gatus_hostname`.`ansible_nas_domain` to it. |
| `gatus_data_directory` | `"{{ docker_home }}/gatus"` | Folder that holds the generated config. |
| `gatus_config_file` | `"{{ gatus_data_directory }}/config.yml"` | Config written from `templates/config.yml.j2`, mounted read-only at `/config/config.yaml`. A change restarts the container. |
| `gatus_port` | `"9382"` | Host port published to the container's port 8080. |
| `gatus_hostname` | `"gatus"` | Subdomain Traefik uses when it is available externally. |
| `gatus_use_vpn` | `false` | Runs Gatus in gluetun's network (`gluetun_name`) instead of publishing a port. |
| `gatus_memory` | `"512m"` | Container memory limit. |
| `gatus_container_name` | `gatus` | Name of the Docker container. |
| `gatus_image_name` | `twinproduction/gatus` | Docker image. |
| `gatus_image_version` | `latest` | Image tag. |

The config template checks other services of the NAS (for example Sonarr's API, using `sonarr_api_key`); edit `templates/config.yml.j2` to add your own checks and notifications.

Application page: `website/docs/applications/monitoring/gatus.md`.
