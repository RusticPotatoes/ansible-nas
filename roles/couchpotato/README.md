# couchpotato

Runs CouchPotato, which downloads movies automatically as soon as they are available, in a container (the `linuxserver/couchpotato` image).

Web interface: port `5050` (`couchpotato_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `couchpotato_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `couchpotato_available_externally` | `false` | Lets Traefik route `couchpotato_hostname`.`ansible_nas_domain` to it. |
| `couchpotato_config_directory` | `"{{ docker_home }}/couchpotato/config"` | CouchPotato's configuration, mounted at `/config`. |
| `couchpotato_movies_directory` | `"{{ movies_root }}"` | Movie library, mounted at `/movies`. |
| `couchpotato_downloads_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `couchpotato_torrents_directory` | `"{{ torrents_root }}"` | Torrent files, mounted at `/torrents`. |
| `couchpotato_user_id` | `"0"` | User the container runs as (`PUID`). |
| `couchpotato_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `couchpotato_port` | `"5050"` | Host port published to the container's port 5050. |
| `couchpotato_memory` | `1g` | Container memory limit. |
| `couchpotato_container_name` | `couchpotato` | Name of the Docker container. |

The image is `linuxserver/couchpotato` (tag `latest`), set in the tasks rather than in defaults. The tasks create `{{ docker_home }}/couchpotato/config` directly, whatever `couchpotato_config_directory` says. There is no hostname variable: the Traefik route uses `couchpotato`.

Application page: `website/docs/applications/download-tools/couchpotato.md`.

Tests: a molecule scenario in `molecule/`.
