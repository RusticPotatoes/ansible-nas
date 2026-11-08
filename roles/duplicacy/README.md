# duplicacy

Runs the Duplicacy web UI (`saspus/duplicacy-web:mini`), a cloud backup tool with client-side encryption and deduplication, in a container.

Web interface: port `3875` (`duplicacy_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `duplicacy_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `duplicacy_available_externally` | `false` | Lets Traefik route `duplicacy_hostname`.`ansible_nas_domain` to it. |
| `duplicacy_config_directory` | `"{{ docker_home }}/duplicacy/config"` | Duplicacy's configuration, mounted at `/config`. |
| `duplicacy_logs_directory` | `"{{ docker_home }}/duplicacy/logs"` | Logs, mounted at `/logs`. |
| `duplicacy_cache_directory` | `"{{ docker_home }}/duplicacy/cache"` | Cache, mounted at `/cache`. |
| `duplicacy_data_permissions` | `"ro"` | Mode of the `samba_shares_root` mount at `/backuproot`: `ro`, or `rw` to let the UI restore data. |
| `duplicacy_web_version` | `"Stable"` | `DUPLICACY_WEB_VERSION`: which Duplicacy web release to run. |
| `duplicacy_user_id` | `"0"` | User the container runs as (`USR_ID`). |
| `duplicacy_group_id` | `"0"` | Group the container runs as (`GRP_ID`). |
| `duplicacy_port` | `"3875"` | Host port published to the container's port 3875. |
| `duplicacy_hostname` | `"duplicacy"` | Container hostname, and the subdomain Traefik uses when it is available externally. |
| `duplicacy_memory` | `1g` | Container memory limit. |
| `duplicacy_container_name` | `duplicacy` | Name of the Docker container. |

The image is `saspus/duplicacy-web:mini`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/system-tools/duplicacy.md`.

Tests: a molecule scenario in `molecule/`.
