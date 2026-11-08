# whisperlive

Runs WhisperLive, a live speech-to-text server based on Whisper, in a container on the NVIDIA GPU (the `cuda` image).

Ports: WebSocket streaming on `9091` (`whisperlive_ws_port`, to the container's 9090) and the REST API with its Swagger UI at `/docs` on `8001` (`whisperlive_rest_port`, to the container's 8000).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `whisperlive_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `whisperlive_data_directory` | `"{{ docker_home }}/whisper-live"` | Server data, mounted at `/var/lib/whisper-live`. |
| `whisperlive_ws_port` | `"9091"` | Host port published to the container's port 9090 (WebSocket streaming). |
| `whisperlive_rest_port` | `"8001"` | Host port published to the container's port 8000 (REST API). |
| `whisperlive_container_name` | `"whisper-live"` | Name of the Docker container. |
| `whisperlive_image_name` | `"hwdsl2/whisper-live-server"` | Docker image. |
| `whisperlive_image_version` | `"cuda"` | Image tag. |
| `whisperlive_model` | `"large-v3"` | Whisper model to load (`WHISPERLIVE_MODEL`). |
| `whisperlive_api_key` | `""` | API key (`WHISPERLIVE_API_KEY`); empty turns authentication off, for LAN-only use. Set it in your vault, never in git. |
| `whisperlive_memory` | `6g` | Container memory limit. |

The container requests all NVIDIA GPUs, so the NAS needs the NVIDIA container runtime. It has no Traefik labels.

Application page: none yet under `website/docs/applications/`.
