# piwigo

Runs Piwigo, open source photo gallery software for the web, in a container, with a MySQL database in a second container.

Web interface: port `16923` (`piwigo_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `piwigo_enabled` | `false` | Starts both containers when `true`; removes both when `false`. |
| `piwigo_available_externally` | `false` | Lets Traefik route `piwigo_hostname`.`ansible_nas_domain` to it. |
| `piwigo_config_directory` | `"{{ docker_home }}/piwigo/config"` | Piwigo's configuration, mounted at `/config`. |
| `piwigo_data_directory` | `"{{ docker_home }}/piwigo/data"` | Its `mysql/` subfolder holds the database (`/var/lib/mysql`). |
| `piwigo_photos` | `"{{ photos_root }}/piwigo"` | The gallery's photos, mounted at `/gallery`. |
| `piwigo_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `piwigo_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `piwigo_mysql_user` | `"piwigo"` | Database user (`MYSQL_USER`); the database is `piwigo`. |
| `piwigo_mysql_password` | `"piwigo"` | Database user's password (`MYSQL_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `piwigo_mysql_root_password` | `"piwigo"` | Database root password (`MYSQL_ROOT_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `piwigo_photos_permission` | `"rw"` | Mount mode for the photos. Not used by the tasks yet: they mount the photos `rw`. |
| `piwigo_hostname` | `"piwigo"` | Subdomain Traefik uses when it is available externally. |
| `piwigo_network_name` | `"piwigo"` | Docker network both containers join. |
| `piwigo_port` | `"16923"` | Host port published to the container's port 80. |
| `piwigo_db_container_name` | `"piwigo-db"` | Name of the database container. |
| `piwigo_db_image_name` | `"mysql"` | Database image. |
| `piwigo_db_image_version` | `"5.7"` | Database image tag. |
| `piwigo_container_name` | `"piwigo"` | Name of the Docker container. |
| `piwigo_image_name` | `"linuxserver/piwigo"` | Docker image. |
| `piwigo_image_version` | `"latest"` | Image tag. |
| `piwigo_memory` | `"1g"` | Memory limit of the Piwigo container. |
| `piwigo_mysql_memory` | `"1g"` | Memory limit of the database container. |
| `piwigo_version` | `"docker"` | Passed to the image as `VERSION`. |

MySQL takes its credentials only when its data folder is empty, so set them before the first start.

Application page: `website/docs/applications/other/piwigo.md`.

Tests: a molecule scenario in `molecule/`.
