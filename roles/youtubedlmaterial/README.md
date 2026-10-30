# youtubedlmaterial

Runs YoutubeDL-Material, a Material Design web front end for youtube-dl, in a container.

Web interface: port `8998` (`youtubedlmaterial_port_http`), published to the container's port 17442.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `youtubedlmaterial_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `youtubedlmaterial_available_externally` | `false` | Lets Traefik route `youtubedlmaterial_hostname`.`ansible_nas_domain` to it. |
| `youtubedlmaterial_data_directory` | `"{{ docker_home }}/youtubedlmaterial"` | Base folder; its `appdata` subfolder is mounted at `/app/appdata`. |
| `youtubedlmaterial_dl_audio_directory` | `"{{ downloads_root }}/youtube/audio"` | Audio downloads, mounted at `/app/audio`. |
| `youtubedlmaterial_dl_video_directory` | `"{{ downloads_root }}/youtube/video"` | Video downloads, mounted at `/app/video`. |
| `youtubedlmaterial_dl_subscriptions_directory` | `"{{ downloads_root }}/youtube/subscriptions"` | Subscription downloads, mounted at `/app/subscriptions`. |
| `youtubedlmaterial_hostname` | `"youtubedlmaterial"` | Subdomain Traefik uses when it is available externally. |
| `youtubedlmaterial_port_http` | `"8998"` | Host port published to the container's port 17442. |
| `youtubedlmaterial_container_name` | `"youtubedlmaterial"` | Name of the Docker container. |
| `youtubedlmaterial_image_name` | `"tzahi12345/youtubedl-material"` | Docker image. |
| `youtubedlmaterial_image_version` | `"latest"` | Image tag. |
| `youtubedlmaterial_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/download-tools/youtubedlmaterial.md`.

Tests: a molecule scenario in `molecule/`.
