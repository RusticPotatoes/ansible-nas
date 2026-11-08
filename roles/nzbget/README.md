# nzbget

Runs NZBGet, a Usenet downloader written in C++ for speed with few system resources, in a container.

Web interface: port `6789` (`nzbget_port`). When `vpn_download_stack_enabled` is on, NZBGet joins gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `nzbget_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `nzbget_available_externally` | `false` | Lets Traefik route `nzbget_hostname`.`ansible_nas_domain` to it. |
| `nzbget_data_directory` | `"{{ docker_home }}/nzbget"` | NZBGet's configuration, mounted at `/config`. |
| `nzbget_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `nzbget_user_id` | `"0"` | User the container runs as (`PUID`) and owner of its folders. |
| `nzbget_group_id` | `"0"` | Group the container runs as (`PGID`) and group of its folders. |
| `nzbget_port` | `"6789"` | Host port published to the container's port 6789. |
| `nzbget_hostname` | `"nzbget"` | Subdomain Traefik uses when it is available externally. |
| `nzbget_container_name` | `"nzbget"` | Name of the Docker container. |
| `nzbget_image_name` | `"linuxserver/nzbget"` | Docker image. |
| `nzbget_image_version` | `"latest"` | Image tag. |
| `nzbget_memory` | `"1g"` | Container memory limit. |

The Homepage widget reads the optional `nzbget_user` and `nzbget_pass` (no default here; empty if unset). Set them in your own vars, never in git.

Application page: `website/docs/applications/download-tools/nzbget.md`.

Tests: a molecule scenario in `molecule/`.
