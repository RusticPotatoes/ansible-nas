# n8n

Runs n8n, an extendable workflow automation tool that connects APIs to each other, in a container.

Web interface: port `5678` (`n8n_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `n8n_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `n8n_available_externally` | `false` | Lets Traefik route `n8n_hostname`.`ansible_nas_domain` to it. |
| `n8n_port` | `5678` | Host port published to the container's port 5678. |
| `n8n_hostname` | `"n8n"` | Subdomain Traefik uses when it is available externally. |
| `n8n_data_directory` | `"{{ docker_home }}/n8n"` | n8n's data, mounted at `/home/node/.n8n`. Created owned by 1000:1000. |
| `n8n_basic_auth_user` | `"n8n_user"` | Basic-auth user (`N8N_BASIC_AUTH_USER`); basic auth is always on. |
| `n8n_basic_auth_password` | `"n8n_change_me"` | Basic-auth password (`N8N_BASIC_AUTH_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `n8n_container_name` | `"n8n"` | Name of the Docker container. |
| `n8n_image_name` | `"docker.n8n.io/n8nio/n8n"` | Docker image. |
| `n8n_image_version` | `"latest"` | Image tag. |
| `n8n_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/home-automation/n8n.md`.

Tests: a molecule scenario in `molecule/`.
