# calibre

Runs Calibre, the e-book manager, in a container (the `linuxserver/calibre` image), with its desktop interface in the browser.

Ports: the Calibre interface on `8093` (`calibre_port`, container port 8080) and Calibre's content server on `8094` (`calibre_webserver_port`, container port 8081), which must first be turned on inside Calibre.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `calibre_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `calibre_available_externally` | `"false"` | Lets Traefik route `calibre_hostname`.`ansible_nas_domain` to it. |
| `calibre_user_id` | `"0"` | User the container runs as (`PUID`). |
| `calibre_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `calibre_data_directory` | `"{{ docker_home }}/calibre"` | Calibre's folder; its `data` subfolder is mounted at `/config`. |
| `calibre_books_directory` | `"{{ books_root }}"` | Books, mounted at `/books`. |
| `calibre_comics_directory` | `"{{ comics_root }}"` | Comics, mounted at `/comics`. |
| `calibre_port` | `"8093"` | Host port published to the container's port 8080. |
| `calibre_webserver_port` | `"8094"` | Host port published to the container's port 8081. |
| `calibre_hostname` | `"calibre"` | Subdomain Traefik uses when it is available externally. |
| `calibre_password` | `""` | `PASSWORD` for the interface's user `abc`; empty means no password. |
| `calibre_cli_args` | `""` | `CLI_ARGS`, extra start arguments for Calibre. |
| `calibre_security_opts` | `"seccomp=unconfined"` | Docker security options for the container (see linuxserver/docker-calibre issue 102). |
| `calibre_memory` | `1g` | Container memory limit. |
| `calibre_container_name` | `calibre` | Name of the Docker container. |

The image is `linuxserver/calibre` (tag `latest`), set in the tasks rather than in defaults.

Application page: `website/docs/applications/media-serving/calibre.md`.

Tests: a molecule scenario in `molecule/`.
