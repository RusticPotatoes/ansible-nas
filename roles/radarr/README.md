# radarr

Runs Radarr, the movie collection manager, in a container. Port: **7878**.

## Variables (defaults/main.yml)

| Variable | Default | Purpose |
|---|---|---|
| `radarr_enabled` | `false` | Turn the role on |
| `radarr_available_externally` | `false` | Allow access from outside the network |
| `radarr_movies_directory` | `{{ movies_root }}` | Movie library directory |
| `radarr_download_directory` | `{{ downloads_root }}` | Download directory |
| `radarr_data_directory` | `{{ docker_home }}/radarr` | Config directory on the host |
| `radarr_user_id` | `"0"` | UID the container runs as |
| `radarr_group_id` | `"0"` | GID the container runs as |
| `radarr_port` | `"7878"` | Web port |
| `radarr_hostname` | `"radarr"` | Container hostname |
| `radarr_container_name` | `"radarr"` | Container name |
| `radarr_image_name` | `"linuxserver/radarr"` | Image name |
| `radarr_image_version` | `"latest"` | Image tag |
| `radarr_memory` | `1g` | Memory limit |
