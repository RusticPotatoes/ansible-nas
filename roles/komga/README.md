# komga

Runs Komga, a media server for comics, mangas, BDs and magazines, in a container.

Web interface: port `8088` (`komga_port_http`), published to the container's port 25600.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `komga_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `komga_available_externally` | `false` | Lets Traefik route `komga_hostname`.`ansible_nas_domain` to it. |
| `komga_data_directory` | `"{{ docker_home }}/komga"` | Komga's data, mounted at `/data`; `config/` under it is mounted at `/config`. |
| `komga_books_directory` | `"{{ books_root }}"` | Book library, mounted read-only at `/books`. |
| `komga_comics_directory` | `"{{ comics_root }}"` | Comics library, mounted read-only at `/comics`. |
| `komga_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `komga_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `komga_hostname` | `"komga"` | Subdomain Traefik uses when it is available externally. |
| `komga_port_http` | `"8088"` | Host port published to the container's port 25600. |
| `komga_container_name` | `"komga"` | Name of the Docker container. |
| `komga_image_name` | `"gotson/komga"` | Docker image. |
| `komga_image_version` | `"latest"` | Image tag. |
| `komga_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/media-serving/komga.md`.

Tests: a molecule scenario in `molecule/`.
