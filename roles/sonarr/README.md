# sonarr

Runs Sonarr, the TV show collection manager, in a container (`linuxserver/sonarr`).

Variables (from `defaults/main.yml`):

| Variable | Default | Purpose |
|---|---|---|
| `sonarr_enabled` | `false` | Deploy the container |
| `sonarr_available_externally` | `false` | Expose through Traefik (`traefik.enable` label) |
| `sonarr_data_directory` | `{{ docker_home }}/sonarr/config` | Config directory, mounted at `/config` |
| `sonarr_tv_directory` | `{{ tv_root }}` | TV library, mounted at `/tv` |
| `sonarr_download_directory` | `{{ downloads_root }}` | Downloads, mounted at `/downloads` |
| `sonarr_user_id` | `"0"` | PUID |
| `sonarr_group_id` | `"0"` | PGID |
| `sonarr_port` | `"8989"` | Host port published for the web UI |
| `sonarr_hostname` | `"sonarr"` | Hostname for the Traefik route |
| `sonarr_container_name` | `"sonarr"` | Container name |
| `sonarr_image_name` | `"linuxserver/sonarr"` | Image |
| `sonarr_image_version` | `"latest"` | Image tag |
| `sonarr_memory` | `1g` | Container memory limit |

Port: the web UI listens on 8989 inside the container; it is published on `sonarr_port` (default 8989) unless the VPN download stack is enabled (`sonarr_vpn_enabled`, which defaults to `vpn_download_stack_enabled`), in which case the container shares the gluetun network and no port is published here.
