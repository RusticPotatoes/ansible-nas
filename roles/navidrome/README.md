# navidrome

Runs Navidrome, an open source web-based music server and streamer compatible with Subsonic/Airsonic, in a container.

Web interface: port `4533` (`navidrome_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `navidrome_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `navidrome_available_externally` | `false` | Lets Traefik route `navidrome_hostname`.`ansible_nas_domain` to it. |
| `navidrome_data_directory` | `"{{ docker_home }}/navidrome"` | Its `data/` subfolder is mounted at `/navidrome/data`; a `playlists/` subfolder is created too. |
| `navidrome_music_directory` | `"{{ music_root }}"` | Music library, mounted at `/navidrome/music`. |
| `navidrome_port` | `"4533"` | Host port published to the container's port 4533. |
| `navidrome_hostname` | `"navidrome"` | Subdomain Traefik uses when it is available externally. |
| `navidrome_container_name` | `"navidrome"` | Name of the Docker container. |
| `navidrome_image_name` | `"deluan/navidrome"` | Docker image. |
| `navidrome_image_version` | `"latest"` | Image tag. |
| `navidrome_memory` | `1g` | Container memory limit. |
| `navidrome_scan_schedule` | `"@every 1m"` | How often the library is scanned (`ND_SCANSCHEDULE`). |
| `navidrome_log_level` | `"info"` | Log level (`ND_LOGLEVEL`). |
| `navidrome_session_timeout` | `"24h"` | How long a login session lasts (`ND_SESSIONTIMEOUT`). |

Application page: `website/docs/applications/media-serving/navidrome.md`.

Tests: a molecule scenario in `molecule/`.
