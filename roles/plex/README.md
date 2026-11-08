# plex

Runs Plex, a personal media server for movies, TV, music, photos and podcasts with apps for many devices, in a container.

Web interface: port `32400` (`/web`). The container uses the host's network, so Plex listens on its own ports directly; no port variable.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `plex_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `plex_available_externally` | `false` | Meant to route Plex through Traefik. Not used by the tasks yet. |
| `plex_config_directory` | `"{{ docker_home }}/plex/config"` | Plex's configuration, mounted at `/config`. |
| `plex_logs` | `"{{ docker_home }}/plex/logs"` | Plex's logs, mounted at `/opt/plex/Library/Application Support/Plex Media Server/Logs`. |
| `plex_movies_directory` | `"{{ movies_root }}"` | Mounted at `/movies`. |
| `plex_tv_directory` | `"{{ tv_root }}"` | Mounted at `/tv`. |
| `plex_photos_directory` | `"{{ photos_root }}"` | Mounted at `/photos`. |
| `plex_podcasts_directory` | `"{{ podcasts_root }}"` | Mounted at `/podcasts`. |
| `plex_music_directory` | `"{{ music_root }}"` | Mounted at `/music`. |
| `plex_audiobooks_directory` | `"{{ audiobooks_root }}"` | Mounted at `/audiobooks`. |
| `plex_user_id` | `"0"` | User the container runs as (`PUID`). |
| `plex_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `plex_movies_permissions` | `"rw"` | Mount mode of `/movies`; `ro` keeps Plex from deleting files. |
| `plex_tv_permissions` | `"rw"` | Mount mode of `/tv`. |
| `plex_photos_permissions` | `"rw"` | Mount mode of `/photos`. |
| `plex_podcasts_permissions` | `"rw"` | Mount mode of `/podcasts`. |
| `plex_music_permissions` | `"rw"` | Mount mode of `/music`. |
| `plex_audiobooks_permissions` | `"rw"` | Mount mode of `/audiobooks`. |
| `plex_hostname` | `"plex"` | Traefik hostname. Not used by the tasks yet. |
| `plex_container_name` | `"plex"` | Name of the Docker container. |
| `plex_image_name` | `"linuxserver/plex"` | Docker image. |
| `plex_image_version` | `"latest"` | Image tag. |
| `plex_memory` | `"4g"` | Container memory limit. |
| `plex_nvidia_gpu` | `false` | Passes the NVIDIA GPUs to the container for hardware transcoding (needs nvidia-container-toolkit). |
| `plex_version` | `"docker"` | Passed to the image as `VERSION` (see the linuxserver/plex image's docs). |

The tasks also read two optional variables with no default here: `plex_devices` (device mappings, e.g. `"/dev/dri:/dev/dri"` for hardware transcoding) and `plex_token` (for the Homepage widget, empty if unset; set it in your own vars, never in git).

Application page: `website/docs/applications/media-serving/plex.md`.

Tests: a molecule scenario in `molecule/`.
