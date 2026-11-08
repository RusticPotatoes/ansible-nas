# gitea

Runs Gitea, a self-hosted Git service, in a container, with a MySQL database in a second container.

Web interface: port `3001` (`gitea_port_http`); Git over SSH: port `222` (`gitea_port_ssh`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `gitea_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `gitea_available_externally` | `false` | Lets Traefik route `gitea_hostname`.`ansible_nas_domain` to it. |
| `gitea_data_directory` | `"{{ docker_home }}/gitea"` | Holds `gitea/` (mounted at `/data`) and `mysql/` (the database files). |
| `gitea_hostname` | `"gitea"` | Subdomain Traefik uses when it is available externally. |
| `gitea_network_name` | `"gitea"` | Name kept for a Gitea network; the tasks do not use it. |
| `gitea_port_http` | `"3001"` | Host port published to the container's port 3000 (web interface). |
| `gitea_port_ssh` | `"222"` | Host port published to the container's port 22 (Git over SSH). |
| `gitea_memory` | `1g` | Container memory limit. |
| `gitea_mysql_memory` | `1g` | Memory limit of the MySQL container. |
| `gitea_container_name` | `gitea` | Name of the Docker container. |
| `gitea_image_name` | `gitea/gitea` | Docker image. |
| `gitea_image_version` | `latest` | Image tag. |
| `gitea_mysql_container_name` | `gitea-mysql` | Name of the MySQL container; Gitea links to it as `db`. |
| `gitea_mysql_image_name` | `mysql` | Docker image of the database. |
| `gitea_mysql_image_version` | `"5.7"` | Image tag of the database. |

The database name, user and passwords are set to `gitea` in the tasks, not in defaults.

Application page: `website/docs/applications/development-tools/gitea.md`.

Tests: a molecule scenario in `molecule/`.
