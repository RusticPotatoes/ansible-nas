# jackett

Runs Jackett, a proxy that translates queries from apps such as Sonarr and Radarr into tracker-specific searches and returns the results, in a container.

Web interface: port `9117` (`jackett_port`). When `vpn_download_stack_enabled` is on, Jackett joins gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `jackett_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `jackett_available_externally` | `false` | Lets Traefik route `jackett_hostname`.`ansible_nas_domain` to it. |
| `jackett_data_directory` | `"{{ docker_home }}/jackett"` | Jackett's configuration, mounted at `/config`. |
| `jackett_torrents_root` | `"{{ torrents_root }}"` | Torrents folder, mounted at `/downloads`. |
| `jackett_hostname` | `"jackett"` | Subdomain Traefik uses when it is available externally. |
| `jackett_port` | `"9117"` | Host port published to the container's port 9117. |
| `jackett_container_name` | `"jackett"` | Name of the Docker container. |
| `jackett_image_name` | `"linuxserver/jackett"` | Docker image. |
| `jackett_image_version` | `"latest"` | Image tag. |
| `jackett_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/download-tools/jackett.md`.

Tests: a molecule scenario in `molecule/`.
