# nextcloud

Runs Nextcloud, a self-hosted file sync and share service, in a container, with a MySQL database in a second container.

Web interface: port `8080` (`nextcloud_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `nextcloud_enabled` | `false` | Starts both containers when `true`; removes both when `false`. |
| `nextcloud_available_externally` | `false` | Lets Traefik route `nextcloud_hostname`.`ansible_nas_domain` to it. |
| `nextcloud_data_directory` | `"{{ docker_home }}/nextcloud"` | Holds `nextcloud/` (mounted at `/var/www/html`) and `mysql/` (the database's `/var/lib/mysql`). |
| `nextcloud_port` | `"8080"` | Host port published to the container's port 80. |
| `nextcloud_hostname` | `"nextcloud"` | Subdomain Traefik uses when it is available externally. |
| `nextcloud_network_name` | `"nextcloud"` | Docker network both containers join. |
| `nextcloud_container_name` | `"nextcloud"` | Name of the Docker container. |
| `nextcloud_image_name` | `"nextcloud"` | Docker image. |
| `nextcloud_image_version` | `"stable"` | Image tag. |
| `nextcloud_db_container_name` | `"nextcloud-db"` | Name of the database container. |
| `nextcloud_db_image_name` | `"mysql"` | Database image. |
| `nextcloud_db_image_version` | `"5.7"` | Database image tag. |
| `nextcloud_sql_user` | `"nextcloud-user"` | Database user (`MYSQL_USER`); the database is `nextcloud`. |
| `nextcloud_sql_password` | `"nextcloud-pass"` | Database user's password. The default is a placeholder: set your own in your own vars, never in git. |
| `nextcloud_sql_root_password` | `"nextcloud-secret"` | Database root password (`MYSQL_ROOT_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `nextcloud_memory` | `1g` | Memory limit of the Nextcloud container. |
| `nextcloud_db_memory` | `1g` | Memory limit of the database container. |

`NEXTCLOUD_TRUSTED_DOMAINS` is set to `nextcloud_hostname`.`ansible_nas_domain`. MySQL takes its passwords only when its data folder is empty, so changing them later does not change the database.

Application page: `website/docs/applications/other/nextcloud.md`.

Tests: a molecule scenario in `molecule/`.
