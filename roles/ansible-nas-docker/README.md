# ansible-nas-docker

Sets up Docker on the NAS for the other roles: installs the Python `docker` module in a virtual environment at `/opt/ansible-venv`, creates `docker_home`, adds `ansible_nas_user` to the `docker` group, and writes Docker's `daemon.json` and a systemd drop-in, restarting Docker when either changes. It runs no container itself.

No port.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ansible_nas_user` | `david` | Account added to the `docker` group. The default is upstream's example: set your own user. |
| `docker_home` | `/mnt/docker` | Where application data lives; most roles keep their folders under it. Worth backing up. |
| `docker_image_directory` | `"/mnt/docker/docker-data/"` | Where Docker stores images (`data-root`). Best on a fast disk; it need not be backed up. |
| `docker_storage_driver` | `overlay2` | Docker storage driver (`storage-driver`), for example `zfs` on a ZFS filesystem. |
| `docker_daemon_json` | see below | Content of `/etc/docker/daemon.json`, written as JSON. |
| `docker_systemd_environment` | see below | Environment variables for the Docker service, written to `/etc/systemd/system/docker.service.d/ansible-nas.conf`. |
| `docker_prune_enabled` | `false` | Turn on the periodic Docker clean-up, a scheduled job of the `nas_maintenance` role. |
| `docker_prune_interval` | `"weekly"` | How often the clean-up runs (systemd `OnCalendar`). |
| `docker_prune_script_path` | `"/usr/local/sbin/ansible-nas-docker-prune"` | Where the clean-up script is installed. |
| `docker_prune_until` | `"168h"` | Only prune objects older than this (`until` filter). |
| `docker_prune_images` | `true` | Prune unused images. |
| `docker_prune_containers` | `true` | Prune stopped containers. |
| `docker_prune_networks` | `true` | Prune unused networks. |
| `docker_prune_build_cache` | `true` | Prune the build cache. |
| `docker_prune_volumes` | `false` | Prune unused volumes. Off by default, since many apps keep state in volumes. |

Default of `docker_daemon_json`:

```yaml
docker_daemon_json:
  data-root: "{{ docker_image_directory }}"
  storage-driver: "{{ docker_storage_driver }}"
```

Default of `docker_systemd_environment`:

```yaml
docker_systemd_environment:
  GODEBUG: "netdns=cgo"
```

The `docker_prune_*` variables are read by the `nas_maintenance` role's prune job (`templates/jobs/ansible-nas-docker-prune.sh.j2` there), not by this role's tasks.

Application page: none yet under `website/docs/applications/`.
