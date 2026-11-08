# nas_maintenance

Host-level upkeep that keeps the NAS healthy without manual work: btrfs scrubs, holding the NVIDIA driver back from unattended upgrades, nightly database dumps, and every job that runs on the NAS by itself (systemd services and timers). It runs no container.

No port: nothing in this role listens.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `nas_btrfs_scrub_mountpoints` | `[]` | btrfs mount points to scrub, written to `BTRFS_SCRUB_MOUNTPOINTS` in `/etc/default/btrfsmaintenance`. Empty leaves that file alone. |
| `nas_btrfs_scrub_period` | `monthly` | How often btrfsmaintenance scrubs (`BTRFS_SCRUB_PERIOD`). |
| `nas_hold_nvidia_driver` | `false` | When `true`, writes `/etc/apt/apt.conf.d/51nas-hold-nvidia` so unattended-upgrades skips the NVIDIA packages; `false` removes that file. |
| `nas_nvidia_hold_patterns` | see below | Package patterns held back when `nas_hold_nvidia_driver` is on. |
| `nas_db_dumps_enabled` | `false` | Turns on the nightly `nas-db-dump` job and creates its folders. |
| `nas_db_dump_directory` | `"{{ docker_home }}/db-dumps"` | Where the dumps are written (mode `0700`). |
| `nas_db_dump_time` | `"*-*-* 01:30:00"` | When the dump job runs (systemd `OnCalendar`). |
| `nas_db_dump_postgres_container` | `""` | PostgreSQL container to dump with `pg_dumpall`; empty skips it. |
| `nas_db_dump_mongodb_container` | `""` | MongoDB container to dump; empty skips it. |
| `nas_status_directory` | `"{{ docker_home }}/nas-status"` | A successful dump writes `db_<name>.influx` here, for Telegraf to alert on. |
| `nas_scheduled_jobs` | see below | Every job that runs on the NAS by itself: its unit name, what it does, why, whether it is on, its schedule (`on_calendar`, or `every` from boot and last run) and its script from `templates/jobs/`. A job that is on gets a script, a service and a timer; a job that is off has its timer stopped and disabled. |

Default of `nas_nvidia_hold_patterns`:

```yaml
nas_nvidia_hold_patterns:
  - "^nvidia-(driver|dkms|kernel|utils|compute-utils|firmware)-"
  - "^libnvidia-(cfg|common|compute|decode|encode|extra|fbc|gl)"
  - "^xserver-xorg-video-nvidia-"
```

Default of `nas_scheduled_jobs`:

```yaml
nas_scheduled_jobs:
  - name: ansible-nas-docker-prune
    description: Prune unused Docker resources
    why: Unused images, stopped containers and build cache fill the Docker disk; volumes are kept.
    enabled: "{{ docker_prune_enabled | default(false) | bool }}"
    on_calendar: "{{ docker_prune_interval | default('weekly') }}"
    script: ansible-nas-docker-prune.sh.j2
    script_path: "{{ docker_prune_script_path | default('/usr/local/sbin/ansible-nas-docker-prune') }}"
  - name: ebook2audiobook-auto-convert
    description: Convert new ebooks to audiobooks
    why: Ebooks dropped in the books folder become audiobooks without anyone starting a conversion.
    enabled: "{{ (ebook2audiobook_enabled | default(false) | bool) and (ebook2audiobook_auto_convert_enabled | default(false) | bool) }}"
    every: "{{ ebook2audiobook_auto_convert_interval | default('30m') }}"
    timeout: "{{ ebook2audiobook_auto_convert_timeout | default('0') }}"
    script: ebook2audiobook-auto-convert.sh.j2
    script_path: "{{ ebook2audiobook_auto_convert_script_path | default('/usr/local/sbin/ebook2audiobook-auto-convert') }}"
  - name: gluetun-stack-restart
    description: Restart gluetun and the containers routed through it
    why: >-
      A workaround for VPN stalls: gluetun and its routed containers (deluge, nzbget, prowlarr)
      are restarted on a fixed interval. Whether it is still needed is being measured (Endora
      #796); keep this reason true when that ends.
    enabled: "{{ (gluetun_enabled | default(false) | bool) and (gluetun_periodic_restart_enabled | default(false) | bool) }}"
    every: "{{ gluetun_periodic_restart_interval | default('2h') }}"
    script: gluetun-stack-restart.sh.j2
    script_path: "{{ gluetun_periodic_restart_script_path | default('/usr/local/sbin/gluetun-stack-restart') }}"
  - name: nas-db-dump
    description: Dump container databases for backup
    why: Backups copy files; a logical dump gives them a consistent copy of each database.
    enabled: "{{ nas_db_dumps_enabled | bool }}"
    on_calendar: "{{ nas_db_dump_time }}"
    script: nas-db-dump.sh.j2
    script_path: /usr/local/sbin/nas-db-dump
    mode: "0750"
  - name: healthchecks-ping
    description: Ping healthchecks.io
    why: An outside service raises the alarm when the NAS stops pinging it.
    enabled: "{{ healthchecks_enabled | default(false) | bool }}"
    on_calendar: "*:0/{{ healthchecks_ping_minutes | default(15) }}"
    needs_docker: false
    script: healthchecks-ping.sh.j2
    script_path: /usr/local/sbin/healthchecks-ping
    mode: "0700"
```

The jobs' scripts are in `templates/jobs/` (Docker prune, ebook2audiobook auto-convert, gluetun stack restart, database dump, healthchecks.io ping); each job is switched by the variables of the app it serves. The tasks also remove the old `healthchecks.io` entry from root's crontab, which the ping job replaced. The fork's lint rule `nas-scheduled-job` keeps jobs in this list.

Application page: `website/docs/further-configuration/scheduled-jobs.md`.
