# romm

Runs RomM (ROM Manager), a web-based game library manager focused on retro gaming, in a container, with MariaDB and Redis in two more containers.

Web interface: port `8484` (`romm_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `romm_enabled` | `false` | Starts the three containers when `true`; removes the RomM and database containers when `false`. |
| `romm_available_externally` | `false` | Lets Traefik route `romm_hostname`.`ansible_nas_domain` to it. |
| `romm_database_username` | `romm_user` | Database user (`MYSQL_USER` / `DB_USER`); the database is `romm`. |
| `romm_database_password` | `top_secret` | Database user's password. The default is a placeholder: set your own in your own vars, never in git. |
| `romm_database_root_password` | `top_top_secret` | MariaDB root password (`MYSQL_ROOT_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `romm_home` | `"{{ docker_home }}/romm"` | Parent of the RomM and database folders. |
| `romm_data_directory` | `"{{ romm_home }}/romm"` | Its `resources/` subfolder is mounted at `/romm/resources`. |
| `romm_db_data_directory` | `"{{ romm_home }}/db"` | Its `db/` subfolder holds the database (`/var/lib/mysql`). |
| `romm_roms_directory` | `"{{ roms_root }}"` | ROM library, mounted at `/romm/library/roms`. |
| `romm_port` | `"8484"` | Host port published to the container's port 8080. |
| `romm_hostname` | `"romm"` | Subdomain Traefik uses when it is available externally. |
| `romm_container_name` | `"romm"` | Name of the RomM container. |
| `romm_image_name` | `"rommapp/romm"` | Docker image. |
| `romm_image_version` | `"latest"` | Image tag. |
| `romm_db_container_name` | `"romm-db"` | Name of the MariaDB container, linked to RomM as `db`. |
| `romm_db_image_name` | `"mariadb"` | Database image. |
| `romm_db_image_version` | `"11.2"` | Database image tag. |
| `romm_redis_container_name` | `"romm-redis"` | Name of the Redis container, linked to RomM as `redis`. |
| `romm_redis_image_name` | `"redis"` | Redis image. |
| `romm_redis_image_version` | `"alpine"` | Redis image tag. |
| `romm_memory` | `1g` | Memory limit of the RomM container. |
| `romm_db_memory` | `1g` | Memory limit of the database container. |
| `romm_redis_memory` | `1g` | Memory limit of the Redis container. |
| `romm_igdb_client_id` | `"abcd"` | IGDB client ID, for game metadata (`IGDB_CLIENT_ID`). The default is a placeholder: set your own in your own vars, never in git. |
| `romm_igdb_client_secret` | `"abcd"` | IGDB client secret (`IGDB_CLIENT_SECRET`). The default is a placeholder: set your own in your own vars, never in git. |
| `romm_mobygames_client_id` | `"abcd"` | MobyGames API key (`MOBYGAMES_API_KEY`). The default is a placeholder: set your own in your own vars, never in git. |
| `romm_steamgriddb_client_id` | `"abcd"` | SteamGridDB API key (`STEAMGRIDDB_API_KEY`). The default is a placeholder: set your own in your own vars, never in git. |
| `romm_auth_secret_key` | `"aaaabbbbccccdddd"` | Auth secret key (`ROMM_AUTH_SECRET_KEY`); generate one with `openssl rand -hex 32`. The default is a placeholder: set your own in your own vars, never in git. |
| `romm_auth_username` | `"admin"` | Login user (`ROMM_AUTH_USERNAME`); auth is always on. |
| `romm_auth_password` | `"admin"` | Login password (`ROMM_AUTH_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |

MariaDB takes its credentials only when its data folder is empty. Disabling the role removes the RomM and database containers; the Redis container is left running.

Application page: `website/docs/applications/media-serving/romm.md`.

Tests: a molecule scenario in `molecule/`.
