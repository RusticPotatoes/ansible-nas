# postgres

Runs PostgreSQL, an open source relational database, in a container on the `postgres_net` Docker network.

Port: `5432` (`postgres_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `postgres_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `postgres_available_externally` | `false` | Meant to route PostgreSQL through Traefik. Not used by the tasks yet. |
| `postgres_data_directory` | `"{{ docker_home }}/postgres"` | Database files, mounted at `/var/lib/postgresql/data`. |
| `postgres_port` | `"5432"` | Host port published to the container's port 5432. |
| `postgres_hostname` | `"postgres"` | Traefik hostname. Not used by the tasks yet. |
| `postgres_ip_allowlist` | `"0.0.0.0/0"` | Allowed client addresses. Not used by the tasks yet. |
| `postgres_container_name` | `"postgres"` | Name of the Docker container. |
| `postgres_image_name` | `"postgres"` | Docker image. |
| `postgres_image_version` | `"16-alpine"` | Image tag. Pin it: data on disk cannot jump major versions. |
| `postgres_memory` | `1g` | Memory limit. Not used by the tasks yet. |

The tasks also read `postgres_user`, `postgres_password` and `postgres_db`, which have no default here and fall back to stock values in the tasks. Set them in your own vars, never in git. PostgreSQL takes them only when its data folder is empty; changing them later does not change the database.

Application page: `website/docs/applications/system-tools/postgres.md`.

Tests: a molecule scenario in `molecule/`.
