# joomla

Runs Joomla, a content management system for building web sites, in a container, with a MySQL database in a second container on its own Docker network.

Web interface: port `8181` (`joomla_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `joomla_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `joomla_available_externally` | `false` | Lets Traefik route `joomla_hostname`.`ansible_nas_domain` to it. |
| `joomla_database_password` | `top_secret` | MySQL root password, which Joomla also logs in with. The default is a placeholder: set your own in your own vars, never in git. MySQL takes it only when its data folder is empty. |
| `joomla_data_directory` | `"{{ docker_home }}/joomla"` | Joomla's site, mounted at `/var/www/html`; `db/` under it holds the database files. |
| `joomla_port` | `"8181"` | Host port published to the container's port 80. |
| `joomla_hostname` | `"joomla"` | Subdomain Traefik uses when it is available externally. |
| `joomla_network_name` | `"joomla"` | Docker network the two containers share. |
| `joomla_container_name` | `"joomla"` | Name of the Docker container. |
| `joomla_image_name` | `"joomla"` | Docker image. |
| `joomla_image_version` | `"latest"` | Image tag. |
| `joomla_db_container_name` | `"joomla-db"` | Name of the MySQL container; Joomla reaches the database by this name. |
| `joomla_db_image_name` | `"mysql"` | Docker image of the database. |
| `joomla_db_image_version` | `"5.7"` | Image tag of the database. |
| `joomla_memory` | `1g` | Container memory limit. |
| `joomla_db_memory` | `1g` | Memory limit of the MySQL container. |

Application page: `website/docs/applications/content-management/joomla.md`.

Tests: a molecule scenario in `molecule/`.
