# heimdall

Runs Heimdall, an application dashboard of links to your web applications (or anything else), in a container.

Web interface: port `11112` (`heimdall_port_http`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `heimdall_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `heimdall_available_externally` | `false` | Lets Traefik route `heimdall_hostname`.`ansible_nas_domain` to it. |
| `heimdall_docker_image` | `linuxserver/heimdall:latest` | Docker image and tag. |
| `heimdall_data_directory` | `"{{ docker_home }}/heimdall"` | Heimdall's configuration, mounted at `/config`. |
| `heimdall_port_http` | `"11112"` | Host port published to the container's port 80. |
| `heimdall_hostname` | `heimdall` | Subdomain Traefik uses when it is available externally. |
| `heimdall_memory` | `1g` | Container memory limit. |
| `heimdall_container_name` | `heimdall` | Name of the Docker container. |

Application page: `website/docs/applications/dashboards/heimdall.md`.

Tests: a molecule scenario in `molecule/`.
