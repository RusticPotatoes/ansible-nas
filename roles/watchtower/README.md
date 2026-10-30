# watchtower

Runs Watchtower, which watches the Docker containers and updates and restarts them when their image is refreshed, in a container. The image is `nickfedor/watchtower`, the maintained fork of the archived `containrrr/watchtower`.

Metrics API: port `8094` (`watchtower_metrics_port`), published to the container's port 8080 only when `watchtower_api_token` is set. Otherwise no port.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `watchtower_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `watchtower_cron_schedule` | `0 0 3 * * *` | Six-field cron schedule of the checks and updates. |
| `watchtower_command` | `"--schedule '{{ watchtower_cron_schedule }}' --cleanup"` | Watchtower's command line. The default checks on `watchtower_cron_schedule` and removes old images (`--cleanup`); `defaults/main.yml` shows commented examples with email or Slack notifications. |
| `watchtower_metrics_port` | `"8094"` | Host port published to the container's port 8080 (metrics API), when a token is set. |
| `watchtower_api_token` | `""` | Token of the metrics API (used by the Homepage widget). Empty turns the API off. Set it in your vault, never in git. |
| `watchtower_memory` | `1g` | Container memory limit. |
| `watchtower_container_name` | `"watchtower"` | Name of the Docker container. |
| `watchtower_image_name` | `"nickfedor/watchtower"` | Docker image. |
| `watchtower_image_version` | `"latest"` | Image tag. |
| `watchtower_docker_api_version` | `"1.40"` | Docker API version Watchtower uses (`DOCKER_API_VERSION`). |

The container mounts the Docker socket. It has no Traefik labels.

Application page: `website/docs/applications/system-tools/watchtower.md`.

Tests: a molecule scenario in `molecule/`.
