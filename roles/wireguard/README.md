# wireguard

Runs WireGuard, a fast, modern VPN server, in a container, so clients (peers) can reach the home network from outside.

VPN: UDP port `51820`, set directly in the tasks (`wireguard_udp_port` is not read). Forward it on your router.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `wireguard_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `wireguard_available_externally` | `false` | Lets Traefik route `wireguard_hostname`.`ansible_nas_domain` to it. |
| `wireguard_data_directory` | `"{{ docker_home }}/wireguard"` | Base folder; its `config` subfolder is mounted at `/config` and receives the peer configs and QR codes. |
| `wireguard_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `wireguard_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `wireguard_hostname` | `"wireguard"` | Subdomain Traefik uses when it is available externally. |
| `wireguard_subnet` | `"10.0.0.0"` | Base address of the VPN subnet (`INTERNAL_SUBNET`); the server takes `.1` and the peers `.2` and up. |
| `wireguard_peers` | `"3"` | Number of peers (VPN clients) to create (`PEERS`). |
| `wireguard_allowed_ips` | `"0.0.0.0/0"` | Meant for the peers' allowed IPs. Not used by the tasks: they set `ALLOWEDIPS` to `0.0.0.0/0` directly. |
| `wireguard_container_name` | `"wireguard"` | Name of the Docker container. |
| `wireguard_image_name` | `"linuxserver/wireguard"` | Docker image. |
| `wireguard_image_version` | `"latest"` | Image tag. |
| `wireguard_memory` | `"512m"` | Container memory limit. |
| `wireguard_udp_port` | `"51820"` | Meant for the VPN port. Not used by the tasks: they publish `51820/udp` directly. |

The container gets the `NET_ADMIN` and `SYS_MODULE` capabilities, the host's `/lib/modules`, and turns on IP forwarding. Peer DNS is `auto`.

Application page: `website/docs/applications/system-tools/wireguard.md`.

Tests: a molecule scenario in `molecule/`.
