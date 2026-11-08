# mymediaforalexa

Runs My Media for Alexa, which streams your music collection to an Amazon Echo or Dot without uploading it to the cloud, in a container.

Port: the container uses the host's network (`network_mode: host`), so it publishes no port of its own; the docs page gives the web interface at port `52051`.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mymediaforalexa_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `mymediaforalexa_media_directory` | `"{{ music_root }}"` | Music library, mounted at `/medialibrary`. |
| `mymediaforalexa_data_directory` | `"{{ docker_home }}/mymediaforalexa"` | App data, mounted at `/datadir`. |
| `mymediaforalexa_container_name` | `"mymediaforalexa"` | Name of the Docker container. |
| `mymediaforalexa_image_name` | `"bizmodeller/mymediaforalexa"` | Docker image. |
| `mymediaforalexa_image_version` | `"latest"` | Image tag. |
| `mymediaforalexa_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/media-serving/mymediaforalexa.md`.

Tests: a molecule scenario in `molecule/`.
