# backrest

Runs Backrest, a web interface and scheduler for restic backups, in a container. The role seeds its first configuration: one restic repository, the backup plans below, and prune and check schedules.

Web interface: port `9898` (`backrest_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `backrest_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `backrest_available_externally` | `false` | Lets Traefik route `backrest_hostname`.`ansible_nas_domain` to it. |
| `backrest_data_directory` | `"{{ docker_home }}/backrest"` | Backrest's folder: `config`, `data` and `cache` are mounted at `/config`, `/data` and `/cache`. |
| `backrest_repo_directory` | `"/mnt/archive/backups/restic"` | The restic repository, mounted at `/repos`. Best on a different disk from the sources. |
| `backrest_status_directory` | `"{{ docker_home }}/nas-status"` | Mounted at `/status`; each successful snapshot writes `backrest_<plan>.influx` here for staleness alerts. |
| `backrest_sources` | see below | Host paths to back up: each `host` is mounted read-only at its `container` path. |
| `backrest_plans` | see below | Backup plans: `id`, container `paths`, `excludes`, a `cron` schedule and restic time-bucket `retention`. |
| `backrest_prune_cron` | `"0 5 * * 0"` | Schedule of the repository prune. |
| `backrest_check_cron` | `"0 6 1 * *"` | Schedule of the repository check. |
| `backrest_check_read_percent` | `5` | Percent of the repository's data read by each check. |
| `backrest_repo_password` | `""` | Password of the restic repository. Required: set it in your vault, never in git. |
| `backrest_ui_username` | `"admin"` | User of the web interface (and of the Homepage widget). |
| `backrest_ui_password` | `""` | Password of that user. Required: set it in your vault, never in git. |
| `backrest_hostname` | `"backrest"` | Subdomain Traefik uses when it is available externally. |
| `backrest_port` | `"9898"` | Host port published to the container's port 9898. |
| `backrest_container_name` | `"backrest"` | Name of the Docker container. |
| `backrest_image_name` | `"garethgeorge/backrest"` | Docker image. |
| `backrest_image_version` | `"latest"` | Image tag. |
| `backrest_memory` | `"2g"` | Container memory limit. |

Default of `backrest_sources`:

```yaml
backrest_sources:
  - host: "{{ docker_home }}"
    container: /sources/docker
```

Default of `backrest_plans`:

```yaml
backrest_plans:
  - id: docker
    paths:
      - /sources/docker
    excludes: []
    cron: "0 2 * * *"
    retention:
      daily: 14
      weekly: 8
      monthly: 12
```

The play stops unless `backrest_repo_password` and `backrest_ui_password` are set. The configuration (`config/config.json`) is written only when none exists; after that Backrest owns it, and changes to these variables need the file deleted first.

Application page: none yet under `website/docs/applications/`.
