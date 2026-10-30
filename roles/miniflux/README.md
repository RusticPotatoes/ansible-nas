# miniflux

Runs Miniflux, a minimalist feed reader, in a container, with a PostgreSQL database in a second container on its own Docker network.

Web interface: port `8070` (`miniflux_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `miniflux_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `miniflux_available_externally` | `false` | Lets Traefik route `miniflux_hostname`.`ansible_nas_domain` to it. |
| `miniflux_data_directory` | `"{{ docker_home }}/miniflux"` | Holds `postgres/`, the database files. |
| `miniflux_admin_username` | `admin` | Admin user created on first start (`ADMIN_USERNAME`). |
| `miniflux_admin_password` | `supersecure` | That user's password (`ADMIN_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `miniflux_hostname` | `"miniflux"` | Subdomain Traefik uses when it is available externally. |
| `miniflux_network_name` | `"miniflux"` | Docker network the two containers share. |
| `miniflux_port` | `"8070"` | Host port published to the container's port 8080. |
| `miniflux_container_name` | `"miniflux"` | Name of the Docker container. |
| `miniflux_image_name` | `"miniflux/miniflux"` | Docker image. |
| `miniflux_image_version` | `"latest"` | Image tag. |
| `miniflux_db_container_name` | `"miniflux-postgres"` | Name of the PostgreSQL container; Miniflux reaches the database by this name. |
| `miniflux_db_image_name` | `"postgres"` | Docker image of the database. |
| `miniflux_db_image_version` | `"11.1"` | Image tag of the database. |
| `miniflux_memory` | `"1g"` | Container memory limit. |
| `miniflux_postgres_memory` | `"1g"` | Memory limit of the PostgreSQL container. |

The database user and password are set in the tasks (`POSTGRES_USER`, `POSTGRES_PASSWORD` and `DATABASE_URL`), not in defaults. Disabling the role removes the Miniflux container but not the database container.

Application page: `website/docs/applications/news/miniflux.md`.

Tests: a molecule scenario in `molecule/`.
