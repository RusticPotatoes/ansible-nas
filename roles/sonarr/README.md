# sonarr

Runs Sonarr, the TV series automation tool, in a container. Port: **8989**.

## Variables (defaults/main.yml)

| Variable | Default | Purpose |
|---|---|---|
| `sonarr_enabled` | `false` | Turn the role on |
| `sonarr_available_externally` | `false` | Allow access from outside the network |
| `sonarr_data_directory` | `{{ docker_home }}/sonarr/config` | Config directory on the host |
| `sonarr_tv_directory` | `{{ tv_root }}` | TV library directory |
| `sonarr_download_directory` | `{{ downloads_root }}` | Download directory |
| `sonarr_user_id` | `"0"` | UID the container runs as |
| `sonarr_group_id` | `"0"` | GID the container runs as |
| `sonarr_port` | `"8989"` | Web port |
| `sonarr_hostname` | `"sonarr"` | Container hostname |
| `sonarr_container_name` | `"sonarr"` | Container name |
| `sonarr_image_name` | `"linuxserver/sonarr"` | Image name |
| `sonarr_image_version` | `"latest"` | Image tag |
| `sonarr_memory` | `1g` | Memory limit |
