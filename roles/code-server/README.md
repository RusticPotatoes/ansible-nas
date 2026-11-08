# code-server

Runs code-server, VS Code in the browser, in a container (the `linuxserver/code-server` image).

Web interface: port `8443` (`code_server_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `code_server_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `code_server_available_externally` | `false` | Lets Traefik route `code_server_hostname`.`ansible_nas_domain` to it. |
| `code_server_config_directory` | `"{{ docker_home }}/code_server"` | code-server's configuration, mounted at `/config`. |
| `code_server_projects_directory` | `"{{ code_root }}"` | Projects folder, mounted at `/code` (the default workspace). |
| `code_server_user_id` | `"0"` | User the container runs as (`PUID`). |
| `code_server_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `code_server_port` | `"8443"` | Host port published to the container's port 8443. |
| `code_server_hostname` | `"code-server"` | Subdomain Traefik uses when it is available externally. |
| `code_server_memory` | `1g` | Container memory limit. |
| `code_server_container_name` | `code_server` | Name of the Docker container. |

The image is `linuxserver/code-server` (tag `latest`), set in the tasks rather than in defaults.

Application page: `website/docs/applications/development-tools/code-server.md`.

Tests: a molecule scenario in `molecule/`.
