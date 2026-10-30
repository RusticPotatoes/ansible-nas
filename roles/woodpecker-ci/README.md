# woodpecker-ci

Runs Woodpecker CI, a simple CI engine, in two containers: the server and an agent that runs the pipelines. It signs users in through Gitea, which must be set up first.

Web interface: port `8000` (`woodpecker_ci_port_ui`). The agent talks to the server over gRPC on `9000` (`woodpecker_ci_port_grpc`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `woodpecker_ci_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `woodpecker_ci_available_externally` | `false` | Lets Traefik route `woodpecker_ci_hostname`.`ansible_nas_domain` to it. |
| `woodpecker_ci_data_directory` | `"{{ docker_home }}/woodpecker-ci"` | The server's data, mounted at `/var/lib/woodpecker`. |
| `woodpecker_ci_port_ui` | `8000` | Host port published to the server's port 8000, the web interface. |
| `woodpecker_ci_port_grpc` | `9000` | Host port published to the server's port 9000, which the agent connects to. |
| `woodpecker_ci_address` | `"http://{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}:{{ woodpecker_ci_port_ui }}"` | The server's own URL (`WOODPECKER_HOST`). |
| `woodpecker_ci_hostname` | `woodpecker-ci` | Subdomain Traefik uses when it is available externally. |
| `woodpecker_ci_container_name` | `"woodpecker-ci"` | Name of the Docker container. |
| `woodpecker_ci_image_name` | `"woodpeckerci/woodpecker-server"` | Docker image. |
| `woodpecker_ci_image_version` | `"latest"` | Image tag. |
| `woodpecker_ci_agent_container_name` | `"woodpecker-ci-agent"` | Name of the Docker container. |
| `woodpecker_ci_agent_image_name` | `"woodpeckerci/woodpecker-agent"` | Docker image. |
| `woodpecker_ci_agent_image_version` | `"latest"` | Image tag. |
| `woodpecker_ci_memory` | `1g` | Container memory limit. |
| `woodpecker_ci_agent_memory` | `1g` | Container memory limit. |
| `woodpecker_ci_admin_user` | `david` | Users granted admin, comma separated (`WOODPECKER_ADMIN`). Upstream's default user, kept here as the example: change it to your own. |
| `woodpecker_ci_agent_secret` | (a sample value; set your own — see defaults/main.yml) | Secret shared by server and agent (`WOODPECKER_AGENT_SECRET`). The default is public: generate your own (`openssl rand -hex 32`) and set it in your vault, never in git. |
| `woodpecker_ci_log_level` | `info` | Log level of server and agent. |
| `woodpecker_ci_gitea_url` | `"http://{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}:{{ gitea_port_http }}"` | URL of the Gitea server (`WOODPECKER_GITEA_URL`); `gitea_port_http` comes from the `gitea` role. |
| `woodpecker_ci_gitea_client` | `notset` | Client ID of the OAuth2 application in Gitea. While it is `notset`, the role stops with an error. |
| `woodpecker_ci_gitea_secret` | `notset` | Client secret of that application. Set it in your vault, never in git. |

The role fails when `gitea_enabled` is false. Registration is open (`WOODPECKER_OPEN`). The agent mounts the Docker socket. The role also adds a `[webhook]` block to Gitea's `app.ini` (under `gitea_data_directory`) allowing private hosts. Turning the role off removes only the server container, not the agent.

Application page: `website/docs/applications/development-tools/woodpecker_ci.md`.

Tests: a molecule scenario in `molecule/`.
