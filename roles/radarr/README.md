# radarr

Runs Radarr, the movie collection manager, in a container (`linuxserver/radarr`).

Variables (from `defaults/main.yml`):

| Variable | Default | Purpose |
|---|---|---|
| `radarr_enabled` | `false` | Deploy the container |
| `radarr_available_externally` | `false` | Expose through Traefik (`traefik.enable` label) |
| `radarr_movies_directory` | `{{ movies_root }}` | Movie library |
| `radarr_download_directory` | `{{ downloads_root }}` | Downloads |
| `radarr_data_directory` | `{{ docker_home }}/radarr` | Config directory |
| `radarr_user_id` | `"0"` | PUID |
| `radarr_group_id` | `"0"` | PGID |
| `radarr_port` | `"7878"` | Host port published for the web UI |
| `radarr_hostname` | `"radarr"` | Hostname for the Traefik route |
| `radarr_container_name` | `"radarr"` | Container name |
| `radarr_image_name` | `"linuxserver/radarr"` | Image |
| `radarr_image_version` | `"latest"` | Image tag |
| `radarr_memory` | `1g` | Container memory limit |

Port: the web UI listens on 7878 inside the container; it is published on `radarr_port` (default 7878) unless the VPN download stack is enabled, in which case the container shares the gluetun network and no port is published here.
