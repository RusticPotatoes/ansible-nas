# transmission

Runs Transmission, a BitTorrent client, in a container, connecting directly (the `transmission-with-openvpn` role is the same client through a VPN).

Web interface: port `9092` (`transmission_webui_port`), published to the container's port 9091. Peer port `51414` (`transmission_external_port`, TCP and UDP, to the container's 51413).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `transmission_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `transmission_available_externally` | `false` | Lets Traefik route `transmission_hostname`.`ansible_nas_domain` to it. |
| `transmission_config_directory` | `"{{ docker_home }}/transmission/config"` | Transmission's configuration, mounted at `/config`. |
| `transmission_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `transmission_watch_directory` | `"{{ torrents_root }}"` | Watch folder for `.torrent` files, mounted at `/watch`. |
| `transmission_user_id` | `"0"` | User the container runs as (`PUID`). |
| `transmission_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `transmission_webui_port` | `"9092"` | Host port published to the container's port 9091, the web interface. |
| `transmission_external_port` | `"51414"` | Host port published to the container's peer port 51413 (TCP and UDP). |
| `transmission_hostname` | `"transmission"` | Subdomain Traefik uses when it is available externally. |
| `transmission_timezone` | `"{{ ansible_nas_timezone }}"` | Container time zone (`TZ`). |
| `transmission_container_name` | `"transmission"` | Name of the Docker container. |
| `transmission_image_name` | `"linuxserver/transmission"` | Docker image. |
| `transmission_image_version` | `"latest"` | Image tag. |
| `transmission_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/download-tools/transmission.md`.

Tests: a molecule scenario in `molecule/`.
