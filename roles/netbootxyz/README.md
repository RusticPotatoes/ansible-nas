# netbootxyz

Runs netboot.xyz, which PXE boots operating system installers and utilities from one menu (iPXE), in a container.

Ports: web interface on `3002` (`netbootxyz_port_http`), HTTP for boot assets on `5803` (`netbootxyz_port_http2`) and TFTP on `69`/udp (`netbootxyz_port_tftp`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `netbootxyz_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `netbootxyz_available_externally` | `false` | Lets Traefik route `netbootxyz_hostname`.`ansible_nas_domain` to it. |
| `netbootxyz_config_directory` | `"{{ docker_home }}/netbootxyz/config"` | Configuration, mounted at `/config`. |
| `netbootxyz_assets_directory` | `"{{ docker_home }}/netbootxyz/assets"` | Boot assets, mounted at `/assets`. |
| `netbootxyz_hostname` | `netbootxyz` | Subdomain Traefik uses when it is available externally. |
| `netbootxyz_port_http` | `"3002"` | Host port published to the container's port 3000 (web interface). |
| `netbootxyz_port_http2` | `"5803"` | Host port published to the container's port 80. |
| `netbootxyz_port_tftp` | `"69"` | Host UDP port published to the container's port 69 (TFTP). |
| `netbootxyz_container_name` | `"netbootxyz"` | Name of the Docker container. |
| `netbootxyz_image_name` | `"linuxserver/netbootxyz"` | Docker image. |
| `netbootxyz_image_version` | `"latest"` | Image tag. |
| `netbootxyz_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `netbootxyz_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `netbootxyz_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/system-tools/netbootxyz.md`.

Tests: a molecule scenario in `molecule/`.
