# wallabag

Runs wallabag, a self-hosted read-it-later application that saves web pages and extracts their content to read later, in a container.

Web interface: port `7780` (`wallabag_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `wallabag_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `wallabag_available_externally` | `false` | Lets Traefik route `wallabag_hostname`.`ansible_nas_domain` to it. |
| `wallabag_data_directory` | `"{{ docker_home }}/wallabag"` | Base folder; its `data` subfolder (with the database in `data/db`) is mounted at `/var/www/wallabag/data` and its `images` subfolder at `/var/www/wallabag/web/assets/images`. The role creates them owned by UID/GID 65534. |
| `wallabag_port` | `"7780"` | Host port published to the container's port 80. |
| `wallabag_hostname` | `wallabag` | Subdomain Traefik uses when it is available externally; also sets wallabag's domain name (`https://<hostname>.<ansible_nas_domain>`). |
| `wallabag_memory` | `1g` | Container memory limit. |
| `wallabag_container_name` | `"wallabag"` | Name of the Docker container. |
| `wallabag_image_name` | `"wallabag/wallabag"` | Docker image. |
| `wallabag_image_version` | `"latest"` | Image tag. |

The first login is wallabag's stock account, as the docs page says: change its password on first use.

Application page: `website/docs/applications/other/wallabag.md`.

Tests: a molecule scenario in `molecule/`.
