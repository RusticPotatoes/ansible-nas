# wireshark

Runs Wireshark, the network protocol analyzer, in a container, with its desktop served in the browser.

Web interface: port `3000`. The container uses the host's network, so the port is the container's own; no port variable.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `wireshark_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `wireshark_available_externally` | `false` | Lets Traefik route `wireshark_hostname`.`ansible_nas_domain` to it. |
| `wireshark_data_directory` | `"{{ docker_home }}/wireshark"` | Base folder; its `config` subfolder is mounted at `/config`. |
| `wireshark_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `wireshark_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `wireshark_hostname` | `"wireshark"` | Subdomain Traefik uses when it is available externally. |
| `wireshark_container_name` | `"wireshark"` | Name of the Docker container. |
| `wireshark_image_name` | `"linuxserver/wireshark"` | Docker image. |
| `wireshark_image_version` | `"latest"` | Image tag. |
| `wireshark_memory` | `"512m"` | Container memory limit. |

The container gets the `NET_ADMIN` capability, to capture on the host's interfaces.

Application page: `website/docs/applications/monitoring/wireshark.md`.

Tests: a molecule scenario in `molecule/`.
