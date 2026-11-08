# mylar

Runs Mylar, an automated comic book (cbr/cbz) downloader for use with SABnzbd, NZBGet and torrents, in a container.

Web interface: port `8585` (`mylar_port_http`), published to the container's port 8090.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mylar_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `mylar_available_externally` | `false` | Lets Traefik route `mylar_hostname`.`ansible_nas_domain` to it. |
| `mylar_data_directory` | `"{{ docker_home }}/mylar"` | Its `config/` subfolder is mounted at `/config`. |
| `mylar_comics_directory` | `"{{ comics_root }}"` | Comics library, mounted at `/comics`. |
| `mylar_downloads_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `mylar_user_id` | `"0"` | User the container runs as (`PUID`). |
| `mylar_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `mylar_hostname` | `"mylar"` | Subdomain Traefik uses when it is available externally. |
| `mylar_port_http` | `"8585"` | Host port published to the container's port 8090. |
| `mylar_container_name` | `"mylar"` | Name of the Docker container. |
| `mylar_image_name` | `"linuxserver/mylar"` | Docker image. |
| `mylar_image_version` | `"latest"` | Image tag. |
| `mylar_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/download-tools/mylar.md`.

Tests: a molecule scenario in `molecule/`.
