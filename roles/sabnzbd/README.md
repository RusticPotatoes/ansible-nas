# sabnzbd

Runs SABnzbd, a Usenet downloader, in a container.

Web interface: port `18080` (`sabnzbd_port`), published to the container's port 8080. When `vpn_download_stack_enabled` is on, SABnzbd joins gluetun's network and publishes no port of its own.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `sabnzbd_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `sabnzbd_available_externally` | `false` | Lets Traefik route `sabnzbd_hostname`.`ansible_nas_domain` to it. |
| `sabnzbd_data_directory` | `"{{ docker_home }}/sabnzbd"` | SABnzbd's configuration, mounted at `/config`. |
| `sabnzbd_downloads_directory` | `"{{ downloads_root }}"` | Completed downloads, mounted at `/downloads`. |
| `sabnzbd_incomplete_directory` | `"{{ downloads_root }}/sabnzbd-incomplete"` | Downloads in progress, mounted at `/incomplete-downloads`. |
| `sabnzbd_port` | `"18080"` | Host port published to the container's port 8080. |
| `sabnzbd_hostname` | `"sabnzbd"` | Subdomain Traefik uses when it is available externally. |
| `sabnzbd_memory` | `1g` | Memory limit. Not used by the tasks yet: the container has no memory limit. |
| `sabnzbd_user_id` | `"0"` | User the container runs as (`PUID`). |
| `sabnzbd_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `sabnzbd_container_name` | `"sabnzbd"` | Name of the Docker container. |
| `sabnzbd_image_name` | `"linuxserver/sabnzbd"` | Docker image. |
| `sabnzbd_image_version` | `"latest"` | Image tag. |

Application page: `website/docs/applications/download-tools/sabnzbd.md`.

Tests: a molecule scenario in `molecule/`.
