# get_iplayer

Runs get_iplayer, which downloads TV and radio programmes from BBC iPlayer, with its web interface, in a container.

Web interface: port `8182` (`get_iplayer_port`), published to the container's port 8181.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `get_iplayer_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `get_iplayer_config_directory` | `"{{ docker_home }}/get_iplayer"` | get_iplayer's configuration, mounted at `/root/.get_iplayer`. |
| `get_iplayer_download_directory` | `"{{ tv_root }}/iplayer_downloads"` | Downloaded programmes, mounted at `/root/output`. |
| `get_iplayer_port` | `"8182"` | Host port published to the container's port 8181. |
| `get_iplayer_container_name` | `"get_iplayer"` | Name of the Docker container. |
| `get_iplayer_image_name` | `"kolonuk/get_iplayer"` | Docker image. |
| `get_iplayer_image_version` | `"latest"` | Image tag. |
| `get_iplayer_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/download-tools/get_iplayer.md`.

Tests: a molecule scenario in `molecule/`.
