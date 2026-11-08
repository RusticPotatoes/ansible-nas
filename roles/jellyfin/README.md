# jellyfin

Runs Jellyfin, a free software media system that streams your movies, TV, music, photos and books to apps on other devices, in a container.

Web interface: port `8096` (`jellyfin_port_http`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `jellyfin_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `jellyfin_available_externally` | `false` | Lets Traefik route `jellyfin_hostname`.`ansible_nas_domain` to it. |
| `jellyfin_config_directory` | `"{{ docker_home }}/jellyfin/config"` | Jellyfin's configuration, mounted at `/config`. |
| `jellyfin_movies_directory` | `"{{ movies_root }}"` | Movie library, mounted at `/movies`. |
| `jellyfin_music_directory` | `"{{ music_root }}"` | Music library, mounted at `/music`. |
| `jellyfin_photos_directory` | `"{{ photos_root }}"` | Photo library, mounted at `/photos`. |
| `jellyfin_tv_directory` | `"{{ tv_root }}"` | TV library, mounted at `/tv`. |
| `jellyfin_books_directory` | `"{{ books_root }}"` | Book library, mounted at `/books`. |
| `jellyfin_audiobooks_directory` | `"{{ audiobooks_root }}"` | Audiobook library, mounted at `/audiobooks`. |
| `jellyfin_movies_permissions` | `"rw"` | Mount mode of the movie library (`rw` or `ro`). |
| `jellyfin_music_permissions` | `"rw"` | Mount mode of the music library. |
| `jellyfin_photos_permissions` | `"rw"` | Mount mode of the photo library. |
| `jellyfin_tv_permissions` | `"rw"` | Mount mode of the TV library. |
| `jellyfin_books_permissions` | `"rw"` | Mount mode of the book library. |
| `jellyfin_audiobooks_permissions` | `"rw"` | Mount mode of the audiobook library. |
| `jellyfin_user_id` | `"0"` | User the container runs as (`PUID`). |
| `jellyfin_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `jellyfin_hostname` | `"jellyfin"` | Subdomain Traefik uses when it is available externally. |
| `jellyfin_port_http` | `"8096"` | Host port published to the container's port 8096. |
| `jellyfin_container_name` | `"jellyfin"` | Name of the Docker container. |
| `jellyfin_image_name` | `"linuxserver/jellyfin"` | Docker image. |
| `jellyfin_image_version` | `"latest"` | Image tag. |
| `jellyfin_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/media-serving/jellyfin.md`.

Tests: a molecule scenario in `molecule/`.
