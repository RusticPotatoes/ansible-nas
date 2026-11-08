# paperless_ng

Runs Paperless-ng, which indexes your scanned documents so you can search them and keep metadata with them, in a container, with PostgreSQL and Redis in two more containers.

Web interface: port `16922` (`paperless_ng_port`), published to the container's port 8000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `paperless_ng_enabled` | `false` | Starts the three containers when `true`; removes them when `false`. |
| `paperless_ng_available_externally` | `false` | Lets Traefik route `paperless_ng_hostname`.`ansible_nas_domain` to it. |
| `paperless_ng_config_directory` | `"{{ docker_home }}/paperless_ng"` | Parent of the database, data and export folders. |
| `paperless_ng_files_directory` | `"{{ documents_root }}/paperless"` | Parent of the media and consume folders. |
| `paperless_ng_postgres_directory` | `"{{ paperless_ng_config_directory }}/postgres"` | Database files, mounted at `/var/lib/postgresql/data`. |
| `paperless_ng_data_directory` | `"{{ paperless_ng_config_directory }}/data"` | Mounted at `/usr/src/paperless/data`. |
| `paperless_ng_export_directory` | `"{{ paperless_ng_config_directory }}/export"` | Mounted at `/usr/src/paperless/export`. |
| `paperless_ng_media_directory` | `"{{ paperless_ng_files_directory }}/media"` | Stored documents, mounted at `/usr/src/paperless/media`. |
| `paperless_ng_consume_directory` | `"{{ paperless_ng_files_directory }}/consume"` | Documents dropped here are taken in; mounted at `/usr/src/paperless/consume`. |
| `paperless_ng_port` | `"16922"` | Host port published to the container's port 8000. |
| `paperless_ng_hostname` | `"paperless_ng"` | Subdomain Traefik uses when it is available externally. |
| `paperless_ng_network_name` | `"paperless_ng"` | Docker network the three containers join. |
| `paperless_ng_postgres_db` | `"paperless"` | Database name (`POSTGRES_DB`). |
| `paperless_ng_postgres_user` | `"paperless"` | Database user (`POSTGRES_USER`). |
| `paperless_ng_postgres_password` | `"paperless"` | Database password (`POSTGRES_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `paperless_ng_redis_container_name` | `"paperless-redis"` | Name of the Redis container. |
| `paperless_ng_redis_image_name` | `"redis"` | Redis image. |
| `paperless_ng_redis_image_version` | `"6.0"` | Redis image tag. |
| `paperless_ng_db_container_name` | `"paperless-db"` | Name of the PostgreSQL container. |
| `paperless_ng_db_image_name` | `"postgres"` | PostgreSQL image. |
| `paperless_ng_db_image_version` | `"13"` | PostgreSQL image tag. |
| `paperless_ng_uiserver_container_name` | `"paperless-uiserver"` | Name of the Paperless-ng container. |
| `paperless_ng_uiserver_image_name` | `"jonaswinkler/paperless-ng"` | Paperless-ng image. |
| `paperless_ng_uiserver_image_version` | `"latest"` | Paperless-ng image tag. |
| `paperless_ng_user_id` | `"1000"` | User ID Paperless-ng maps to (`USERMAP_UID`). |
| `paperless_ng_group_id` | `"1000"` | Group ID Paperless-ng maps to (`USERMAP_GID`). |
| `paperless_ng_languages` | `"deu eng"` | OCR languages (`PAPERLESS_OCR_LANGUAGES`). |
| `paperless_ng_ui_memory` | `1g` | Memory limit of the Paperless-ng container. |
| `paperless_ng_postgres_memory` | `1g` | Memory limit of the PostgreSQL container. |
| `paperless_ng_redis_memory` | `1g` | Memory limit of the Redis container. |

Traefik routes to container port 8080, while the app is published from port 8000. PostgreSQL takes its credentials only when its data folder is empty. To log in, create a superuser as the docs page shows.

Application page: `website/docs/applications/other/paperless_ng.md`.

Tests: a molecule scenario in `molecule/`.
