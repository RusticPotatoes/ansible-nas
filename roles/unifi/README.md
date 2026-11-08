# unifi

Runs the UniFi Network Application, which manages UniFi network devices, in a container. It stores its data in the MongoDB server of the `mongodb` role.

Web interface: port `8443` (`unifi_port`, HTTPS). The tasks also publish the controller's fixed ports: `8080`, `8843` and `8880` (TCP) and `3478`, `10001` and `5514` (UDP).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `unifi_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `unifi_available_externally` | `false` | Meant for Traefik routing. Not used by the tasks yet: the container has no Traefik labels. |
| `unifi_config_directory` | `"{{ docker_home }}/unifi/config"` | The application's configuration, mounted at `/config`. |
| `unifi_download_directory` | `"{{ downloads_root }}"` | Mounted at `/downloads`. |
| `unifi_watch_directory` | `"{{ torrents_root }}"` | Not used by the tasks yet. |
| `unifi_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `unifi_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `unifi_log_level` | `"error"` | Log level. Not used by the tasks yet. |
| `unifi_port` | `"8443"` | Host port published to the container's port 8443. |
| `unifi_hostname` | `"unifi"` | Hostname kept for Traefik. Not used by the tasks yet. |
| `unifi_timezone` | `"{{ ansible_nas_timezone }}"` | Container time zone (`TZ`). |
| `unifi_memory` | `1g` | Container memory limit. |
| `unifi_container_name` | `unifi` | Name of the Docker container. |
| `unifi_image_name` | `lscr.io/linuxserver/unifi-network-application` | Docker image. |
| `unifi_image_version` | `latest` | Image tag. |
| `unifi_image_pull_retries` | `5` | How often the image pull is retried before the role fails. |
| `unifi_image_pull_delay` | `30` | Seconds between those retries. |

The tasks pull the image in a step of its own, then start the container without pulling. They log in to MongoDB on the NAS's address, port 27017, with `mongodb_user` and `mongodb_password` (variables of the `mongodb` role; set the password in your vault, never in git), using the `unifi` database. MongoDB takes its first credentials once, when its data folder is empty.

Application page: `website/docs/applications/system-tools/unifi.md`.

Tests: a molecule scenario in `molecule/`.
