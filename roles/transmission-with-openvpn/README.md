# transmission-with-openvpn

Runs Transmission, a BitTorrent client, in a container that tunnels its traffic through OpenVPN. It also runs a web proxy that goes through the tunnel.

Web interface: port `9091` (`transmission_openvpn_webui_port`). Peer port `51415` (`transmission_openvpn_external_port`, TCP and UDP, to the container's 51413) and the web proxy `3128` (`transmission_openvpn_proxy_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `transmission_with_openvpn_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `transmission_with_openvpn_available_externally` | `false` | Lets Traefik route `transmission_openvpn_hostname`.`ansible_nas_domain` to it. |
| `transmission_config_directory` | `"{{ docker_home }}/transmission/config"` | Transmission's configuration, mounted at `/config`. Shared with the `transmission` role's default. |
| `transmission_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads` (incomplete ones in `.incomplete`). |
| `transmission_watch_directory` | `"{{ torrents_root }}"` | Watch folder for `.torrent` files, mounted at `/watch`. |
| `transmission_openvpn_user_id` | `"0"` | User the container runs as (`PUID`). |
| `transmission_openvpn_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `transmission_openvpn_ratio_limit_enabled` | `true` | Stop seeding at the ratio limit (`TRANSMISSION_RATIO_LIMIT_ENABLED`). |
| `transmission_openvpn_ratio_limit` | `"2"` | Seed ratio limit (`TRANSMISSION_RATIO_LIMIT`). |
| `transmission_openvpn_local_network` | `"192.168.1.0/24"` | Local network that may still reach the container outside the tunnel (`LOCAL_NETWORK`). |
| `transmission_openvpn_webui_port` | `"9091"` | Host port published to the container's port 9091. |
| `transmission_openvpn_external_port` | `"51415"` | Host port published to the container's port 51413. |
| `transmission_openvpn_proxy_port` | `"3128"` | Host port published to the container's port 3128. |
| `transmission_openvpn_hostname` | `"transmission_openvpn"` | Subdomain Traefik uses when it is available externally. |
| `transmission_openvpn_container_name` | `"transmission-openvpn"` | Name of the Docker container. |
| `transmission_openvpn_image_name` | `"haugene/transmission-openvpn"` | Docker image. |
| `transmission_openvpn_image_version` | `"latest"` | Image tag. |
| `openvpn_username` | `leisure-suit-larry` | VPN account user name (`OPENVPN_USERNAME`). The default is a placeholder: set yours in your own vars, never in git. |
| `openvpn_password` | `secretpassword` | VPN account password (`OPENVPN_PASSWORD`). A placeholder: set yours in your own vars, never in git. |
| `openvpn_provider` | `AWESOMEVPNPROVIDER` | VPN provider (`OPENVPN_PROVIDER`), one the image supports. |
| `openvpn_config` | `United-Kingdom` | The provider's server configuration to use (`OPENVPN_CONFIG`). |
| `transmission_openvpn_memory` | `1g` | Container memory limit. |

The container gets `/dev/net/tun` and the `NET_ADMIN` capability, and mounts the host's `/etc/localtime` and `/etc/timezone`. The `transmission` role is the same client without the VPN.

Application page: `website/docs/applications/download-tools/transmission.md`.

Tests: a molecule scenario in `molecule/`.
