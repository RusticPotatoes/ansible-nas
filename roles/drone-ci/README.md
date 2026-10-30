# drone-ci

Runs Drone, a self-service continuous integration platform, in two containers: the server (`drone/drone:2`) and a Docker runner (`drone/drone-runner-docker:1`). It signs in through Gitea, which must be enabled first.

Ports: the Drone server on `8001` (`drone_ci_port_http`, container port 80) and the runner on `8002` (`drone_ci_runner_port_http`, container port 3000).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `drone_ci_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `drone_ci_available_externally` | `false` | Lets Traefik route `drone_ci_hostname`.`ansible_nas_domain` to it. |
| `drone_ci_data_directory` | `"{{ docker_home }}/drone-ci"` | Drone's data, mounted at `/var/lib/drone`. |
| `drone_ci_port_http` | `8001` | Host port published to the server's port 80. |
| `drone_ci_runner_port_http` | `8002` | Host port published to the runner's port 3000. |
| `drone_ci_address` | `"http://{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}:{{ drone_ci_port_http }}"` | `DRONE_SERVER_HOST`: the address Drone is reached at. |
| `drone_ci_hostname` | `drone-ci` | Subdomain Traefik uses when it is available externally. |
| `drone_ci_memory` | `1g` | Memory limit of the server container. |
| `drone_ci_agent_memory` | `1g` | Memory limit of the runner container. |
| `drone_ci_container_name` | `drone-ci` | Name of the server container. |
| `drone_ci_runner_container_name` | `drone-ci-runner` | Name of the runner container. |
| `drone_ci_admin_user` | `david` | Gitea user (or comma-separated users) made a Drone admin. The default is an example: set your own. |
| `drone_ci_agent_secret` | `d052ab29a86a02c6b6ff1e5851ee15e1` | `DRONE_RPC_SECRET` shared by server and runner. The default is a placeholder: generate your own (`openssl rand -hex 16`) and set it in your own vars, never in git. |
| `drone_ci_debug_logging` | `false` | `DRONE_LOGS_DEBUG`. |
| `drone_ci_gitea_url` | `"http://{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}:{{ gitea_port_http }}"` | `DRONE_GITEA_SERVER`: the Gitea server Drone signs in through. |
| `drone_ci_gitea_client_id` | `notset` | Gitea OAuth2 client ID. The play fails while it is `notset`. |
| `drone_ci_gitea_client_secret` | `notset` | Gitea OAuth2 client secret. Set it in your own vars, never in git. |
| `drone_ci_runner_capacity` | `2` | `DRONE_RUNNER_CAPACITY`: how many builds the runner runs at once. |
| `drone_ci_runner_name` | `"{{ ansible_nas_hostname }}"` | `DRONE_RUNNER_NAME`. |

The play fails when `gitea_enabled` is false. The role also adds a `[webhook]` section to Gitea's `app.ini` (allowing private hosts) and restarts Gitea. The runner mounts the host's Docker socket.

Application page: `website/docs/applications/development-tools/drone_ci.md`.

Tests: a molecule scenario in `molecule/`.
