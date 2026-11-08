# organizr

Runs Organizr, an HTPC and home lab services organizer written in PHP, in a container.

Web interface: HTTP on `10081` (`organizr_port_http`) and HTTPS on `10444` (`organizr_port_https`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `organizr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `organizr_available_externally` | `false` | Lets Traefik route `organizr_hostname`.`ansible_nas_domain` to it. |
| `organizr_data_directory` | `"{{ docker_home }}/organizr"` | Organizr's configuration, mounted at `/config`. |
| `organizr_port_http` | `"10081"` | Host port published to the container's port 80. |
| `organizr_port_https` | `"10444"` | Host port published to the container's port 443. |
| `organizr_hostname` | `"organizr"` | Subdomain Traefik uses when it is available externally. |
| `organizr_container_name` | `"organizr"` | Name of the Docker container. |
| `organizr_image_name` | `"organizr/organizr"` | Docker image. |
| `organizr_image_version` | `"latest"` | Image tag. |
| `organizr_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `organizr_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `organizr_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/dashboards/organizr.md`.

Tests: a molecule scenario in `molecule/`.
