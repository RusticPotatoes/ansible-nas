# faster-whisper

Runs faster-whisper, a speech-to-text server speaking the Wyoming protocol (the `linuxserver/faster-whisper` image), in a container with access to the NVIDIA GPU.

Wyoming protocol: port `10300` (`faster_whisper_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `faster_whisper_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `faster_whisper_config_directory` | `"{{ docker_home }}/whisper"` | Configuration and models, mounted at `/config`. |
| `faster_whisper_port` | `"10300"` | Host port published to the container's port 10300. |
| `faster_whisper_container_name` | `"wyoming-faster-whisper"` | Name of the Docker container. |
| `faster_whisper_image_name` | `"lscr.io/linuxserver/faster-whisper"` | Docker image. |
| `faster_whisper_image_version` | `"latest"` | Image tag. |
| `faster_whisper_model` | `"small"` | `WHISPER_MODEL`: the Whisper model to load. |
| `faster_whisper_language` | `"en"` | `WHISPER_LANG`: language of the speech. |
| `faster_whisper_memory` | `4g` | Container memory limit. |

The container runs as `PUID`/`PGID` 1000, set in the tasks, and requests every NVIDIA GPU, so the NVIDIA container toolkit must be installed. It has no Traefik route.

Application page: none yet under `website/docs/applications/`.
