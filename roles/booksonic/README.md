# booksonic

Runs Booksonic, a server that streams your audiobooks to a browser, an Android phone or a Subsonic app, in a container (the `linuxserver/booksonic-air` image).

Web interface: port `4041` (`booksonic_port`), published to the container's port 4040.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `booksonic_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `booksonic_available_externally` | `false` | Lets Traefik route `booksonic_hostname`.`ansible_nas_domain` to it. |
| `booksonic_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `booksonic_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `booksonic_data_directory` | `"{{ docker_home }}/booksonic"` | Booksonic's own folder: its `data` and `playlists` subfolders are mounted at `/booksonic/data` and `/booksonic/playlists`. |
| `booksonic_audiobooks_directory` | `"{{ audiobooks_root }}"` | Audiobooks, mounted at `/booksonic/audiobooks`. |
| `booksonic_podcasts_directory` | `"{{ podcasts_root }}"` | Podcasts, mounted at `/booksonic/podcasts`. |
| `booksonic_port` | `"4041"` | Host port published to the container's port 4040. |
| `booksonic_hostname` | `"booksonic"` | Subdomain Traefik uses when it is available externally. |
| `booksonic_memory` | `1g` | Container memory limit. |
| `booksonic_container_name` | `booksonic` | Name of the Docker container. |

The image is `linuxserver/booksonic-air:latest`, set in the tasks rather than in defaults. The default login is `admin` / `admin`; change it right after the first login.

Application page: `website/docs/applications/media-serving/booksonic.md`.

Tests: a molecule scenario in `molecule/`.
