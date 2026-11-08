# calibreweb

Runs Calibre-Web, a web app for browsing, reading and downloading e-books from a Calibre library, in a container (`linuxserver/calibre-web:latest`).

Web interface: port `8084` (`calibreweb_port`), published to the container's port 8083.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `calibreweb_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `calibreweb_available_externally` | `false` | Lets Traefik route `calibreweb_hostname`.`ansible_nas_domain` to it. |
| `calibreweb_user_id` | `"0"` | User the container runs as (`PUID`). |
| `calibreweb_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `calibreweb_data_directory` | `"{{ docker_home }}/calibreweb"` | Calibre-Web's folder: `config` is mounted at `/config` and `data` at `/data`. |
| `calibreweb_books_root` | `"{{ books_root }}"` | Books, mounted at `/books`. |
| `calibreweb_ebook_conversion` | `"linuxserver/calibre-web:calibre"` | `DOCKER_MODS`: the image mod that adds Calibre's e-book conversion. |
| `calibreweb_port` | `"8084"` | Host port published to the container's port 8083. |
| `calibreweb_hostname` | `"calibreweb"` | Subdomain Traefik uses when it is available externally. |
| `calibreweb_memory` | `1g` | Container memory limit. |
| `calibreweb_container_name` | `calibreweb` | Name of the Docker container. |

The tasks also mount `{{ docker_home }}/calibre/data` (the `calibre` role's config) at `/data/calibre`. The image is `linuxserver/calibre-web:latest`, set in the tasks rather than in defaults.

Application page: none yet under `website/docs/applications/`.

Tests: a molecule scenario in `molecule/`.
