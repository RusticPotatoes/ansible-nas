# ubooquity

Runs Ubooquity, a lightweight home server for comics and ebooks, in a container.

Web interface: port `2202` (`ubooquity_port_webui`), at `/ubooquity`. Admin portal: port `2203` (`ubooquity_port_admin`), at `/ubooquity/admin`; it is not routed through Traefik.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ubooquity_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `ubooquity_available_externally` | `false` | Lets Traefik route `ubooquity_hostname`.`ansible_nas_domain` to it. |
| `ubooquity_user_id` | `"0"` | User the container runs as (`PUID`). |
| `ubooquity_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `ubooquity_data_directory` | `"{{ docker_home }}/ubooquity"` | Base folder; its `config` subfolder is mounted at `/config` and its `files` subfolder at `/files`. |
| `ubooquity_port_webui` | `"2202"` | Host port published to the container's port 2202, the web interface. |
| `ubooquity_port_admin` | `"2203"` | Host port published to the container's port 2203, the admin portal. |
| `ubooquity_hostname` | `ubooquity` | Subdomain Traefik uses when it is available externally. |
| `ubooquity_memory` | `1g` | Container memory limit. |
| `ubooquity_container_name` | `"ubooquity"` | Name of the Docker container. |
| `ubooquity_image_name` | `"linuxserver/ubooquity"` | Docker image. |
| `ubooquity_image_version` | `"latest"` | Image tag. |

The tasks also mount `comics_root` at `/comics` and `books_root` at `/books`, and set `MAXMEM` to `1024`. To reach Ubooquity through Traefik without the `/ubooquity` suffix, set the reverse proxy prefix to blank in the admin portal, as the docs page explains.

Application page: `website/docs/applications/media-serving/ubooquity.md`.

Tests: a molecule scenario in `molecule/`.
