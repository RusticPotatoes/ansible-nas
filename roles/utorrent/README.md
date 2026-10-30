# utorrent

Runs uTorrent, a BitTorrent client, with its web interface, in a container.

Web interface: port `8111` (`utorrent_port_http`), at `/gui`, published to the container's port 8080. Peer port `6881` (`utorrent_port_bt`, TCP and UDP).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `utorrent_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `utorrent_available_externally` | `false` | Lets Traefik route `utorrent_hostname`.`ansible_nas_domain` to it. |
| `utorrent_config_directory` | `"{{ docker_home }}/utorrent/config"` | uTorrent's settings, mounted at `/utorrent/settings`. |
| `utorrent_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/data`; completed downloads land there. |
| `utorrent_download_directory_active` | `"{{ downloads_root }}/.incomplete"` | Downloads in progress. The role creates it; the container uses `/data/.incomplete`, which is this folder with the default value. |
| `utorrent_user_id` | `"0"` | User the container runs as (`UID`). |
| `utorrent_group_id` | `"0"` | Group the container runs as (`GID`). |
| `utorrent_port_http` | `"8111"` | Host port published to the container's port 8080, the web interface. |
| `utorrent_port_bt` | `"6881"` | Host port published to the container's port 6881 (TCP and UDP). |
| `utorrent_hostname` | `"utorrent"` | Subdomain Traefik uses when it is available externally. |
| `utorrent_container_name` | `"utorrent"` | Name of the Docker container. |
| `utorrent_image_name` | `"ekho/utorrent"` | Docker image. |
| `utorrent_image_version` | `"latest"` | Image tag. |
| `utorrent_memory` | `1g` | Container memory limit. |

The tasks also mount `torrents_root` at `/utorrent/torrents`.

Application page: `website/docs/applications/download-tools/utorrent.md`.

Tests: a molecule scenario in `molecule/`.
