# bazarr

Runs Bazarr, a companion to Sonarr and Radarr that manages and downloads subtitles for your TV shows and movies, in a container.

Web interface: port `6767` (`bazarr_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `bazarr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `bazarr_available_externally` | `false` | Lets Traefik route `bazarr_hostname`.`ansible_nas_domain` to it. |
| `bazarr_data_directory` | `"{{ docker_home }}/bazarr/config"` | Bazarr's configuration, mounted at `/config`. |
| `bazarr_tv_directory` | `"{{ tv_root }}"` | TV library, mounted at `/tv`. |
| `bazarr_movies_directory` | `"{{ movies_root }}"` | Movie library, mounted at `/movies`. |
| `bazarr_user_id` | `"0"` | User the container runs as (`PUID`). |
| `bazarr_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `bazarr_port` | `"6767"` | Host port published to the container's port 6767. |
| `bazarr_hostname` | `"bazarr"` | Subdomain Traefik uses when it is available externally. |
| `bazarr_memory` | `1g` | Container memory limit. |
| `bazarr_container_name` | `bazarr` | Name of the Docker container. |

The image is `linuxserver/bazarr` (tag `latest`), set in the tasks rather than in defaults.

Application page: `website/docs/applications/download-tools/bazarr.md`.

Tests: a molecule scenario in `molecule/`.
