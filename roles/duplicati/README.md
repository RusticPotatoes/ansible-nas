# duplicati

Runs Duplicati, free backup software that stores encrypted backups online, in a container (the `linuxserver/duplicati` image).

Web interface: port `8200` (`duplicati_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `duplicati_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `duplicati_available_externally` | `false` | Lets Traefik route `duplicati_hostname`.`ansible_nas_domain` to it. |
| `duplicati_data_directory` | `"{{ docker_home }}/duplicati/config"` | Duplicati's configuration, mounted at `/config`. |
| `duplicati_data_permissions` | `"ro"` | Mode of the backup sources (`samba_shares_root` at `/source/shares`, `docker_home` at `/source/docker`): `ro`, or `rw` to allow restores. |
| `duplicati_user_id` | `"0"` | User the container runs as (`PUID`). |
| `duplicati_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `duplicati_port` | `"8200"` | Host port published to the container's port 8200. |
| `duplicati_hostname` | `"duplicati"` | Subdomain Traefik uses when it is available externally. |
| `duplicati_memory` | `1g` | Container memory limit. |
| `duplicati_container_name` | `duplicati` | Name of the Docker container. |

The image is `linuxserver/duplicati` (tag `latest`), set in the tasks rather than in defaults.

Application page: `website/docs/applications/system-tools/duplicati.md`.
