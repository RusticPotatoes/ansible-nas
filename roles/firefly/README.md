# firefly

Runs Firefly III, a self-hosted personal finance manager, in a container (`fireflyiii/core:latest`), with a MariaDB 10.9 container for its database.

Web interface: port `8066` (`firefly_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `firefly_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `firefly_available_externally` | `false` | Lets Traefik route `firefly_hostname`.`ansible_nas_domain` to it. |
| `firefly_data_directory` | `"{{ docker_home }}/firefly"` | Firefly's folder: `mariadb` holds the database, `upload` and `export` are mounted into Firefly's storage. |
| `firefly_hostname` | `"firefly"` | Subdomain Traefik uses when it is available externally; also builds `APP_URL`. |
| `firefly_port` | `"8066"` | Host port published to the container's port 8080. |
| `firefly_memory` | `"1g"` | Memory limit of the Firefly container. |
| `firefly_mysql_memory` | `"1g"` | Memory limit of the database container. |
| `firefly_container_name` | `firefly` | Name of the Firefly container. |
| `firefly_mysql_container_name` | `firefly-mysql` | Name of the database container. |

The database name, user and passwords and Firefly's `APP_KEY` are fixed in the tasks, not variables. The play pauses 30 seconds after starting the database.

Application page: `website/docs/applications/other/firefly.md`.

Tests: a molecule scenario in `molecule/`.
