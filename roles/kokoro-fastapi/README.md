# kokoro-fastapi

Runs Kokoro-FastAPI, a text-to-speech API server for the Kokoro model, in a container on the NVIDIA GPU (all GPUs are requested).

API: port `8881` (`kokoro_fastapi_port`), published to the container's port 8880.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `kokoro_fastapi_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `kokoro_fastapi_port` | `"8881"` | Host port published to the container's port 8880. |
| `kokoro_fastapi_container_name` | `"kokoro-fastapi"` | Name of the Docker container. |
| `kokoro_fastapi_image_name` | `"ghcr.io/remsky/kokoro-fastapi-gpu"` | Docker image. |
| `kokoro_fastapi_image_version` | `"latest"` | Image tag. |
| `kokoro_fastapi_memory` | `4g` | Container memory limit. |

The role has no Traefik route and no data folder. It needs the NVIDIA container runtime on the host.

Application page: none yet under `website/docs/applications/`.
