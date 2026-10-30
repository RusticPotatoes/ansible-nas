# threadfin

Runs Threadfin, an M3U proxy server for Plex, Emby, Jellyfin and other clients, in a container. It emulates an HDHomeRun tuner so IPTV channels can be used by software that would not otherwise support them.

Web interface: port `34400` (`threadfin_port`), at `/web`.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `threadfin_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `threadfin_data_directory` | `"{{ docker_home }}/threadfin"` | Threadfin's configuration, mounted at `/home/threadfin/conf`. |
| `threadfin_port` | `34400` | Host port published to the container's port 34400. |
| `threadfin_container_name` | `"threadfin"` | Name of the Docker container. |
| `threadfin_image_name` | `"fyb3roptik/threadfin"` | Docker image. |
| `threadfin_image_version` | `"latest"` | Image tag. |
| `threadfin_memory` | `1g` | Container memory limit. |

The role sets no Traefik labels, so Threadfin is not routed externally.

Application page: `website/docs/applications/media-serving/threadfin.md`.

Tests: a molecule scenario in `molecule/`.
