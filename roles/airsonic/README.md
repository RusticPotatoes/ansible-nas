# airsonic

Runs Airsonic, a free, web-based media streamer for your music library, in a container.

Web interface: port `4040` (`airsonic_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `airsonic_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `airsonic_available_externally` | `false` | Lets Traefik route `airsonic_hostname`.`ansible_nas_domain` to it. |
| `airsonic_data_directory` | `"{{ docker_home }}/airsonic"` | Airsonic's own folder: its `data` and `playlists` subfolders are mounted at `/airsonic/data` and `/airsonic/playlists`. |
| `airsonic_music_directory` | `"{{ music_root }}"` | Music library, mounted at `/airsonic/music`. |
| `airsonic_podcasts_directory` | `"{{ podcasts_root }}"` | Podcasts, mounted at `/airsonic/podcasts`. |
| `airsonic_port` | `"4040"` | Host port published to the container's port 4040. |
| `airsonic_hostname` | `"airsonic"` | Subdomain Traefik uses when it is available externally. |
| `airsonic_memory` | `1g` | Container memory limit. |
| `airsonic_container_name` | `airsonic` | Name of the Docker container. |

The image is `airsonic/airsonic:latest`, set in the tasks rather than in defaults. The default login is `admin` / `admin`; change it right after the first login.

Application page: `website/docs/applications/media-serving/airsonic.md`.

Tests: a molecule scenario in `molecule/`.
