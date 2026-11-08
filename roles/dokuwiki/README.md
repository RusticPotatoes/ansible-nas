# dokuwiki

Runs DokuWiki, a wiki that needs no database, in a container (`linuxserver/dokuwiki:latest`).

Web interface: port `8085` (`dokuwiki_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `dokuwiki_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `dokuwiki_available_externally` | `false` | Lets Traefik route `dokuwiki_hostname`.`ansible_nas_domain` to it. |
| `dokuwiki_data_directory` | `"{{ docker_home }}/dokuwiki"` | Wiki data, mounted at `/config/dokuwiki/data`. |
| `dokuwiki_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `dokuwiki_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `dokuwiki_hostname` | `"dokuwiki"` | Subdomain Traefik uses when it is available externally. |
| `dokuwiki_port` | `"8085"` | Host port published to the container's port 80. |
| `dokuwiki_memory` | `1g` | Container memory limit. |
| `dokuwiki_container_name` | `dokuwiki` | Name of the Docker container. |

The image is `linuxserver/dokuwiki:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/content-management/dokuwiki.md`.

Tests: a molecule scenario in `molecule/`.
