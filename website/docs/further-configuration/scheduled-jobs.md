---
title: "Scheduled jobs on the NAS"
---

Everything that runs on the NAS by itself is one of `nas_maintenance`'s scheduled jobs, listed in
`nas_scheduled_jobs` (`roles/nas_maintenance/defaults/main.yml`) with what it does and why. No
other role installs a systemd timer or a cron job: the fork's lint rule `nas-scheduled-job` fails
one that does, so nothing runs on a schedule without a reason written beside it.

| Job (systemd unit) | Switch | Schedule | Why |
|---|---|---|---|
| `ansible-nas-docker-prune` | `docker_prune_enabled` | `docker_prune_interval` (weekly) | Unused images, stopped containers and build cache fill the Docker disk; volumes are kept. |
| `ebook2audiobook-auto-convert` | `ebook2audiobook_auto_convert_enabled` (and the app on) | every `ebook2audiobook_auto_convert_interval` (30m) | New ebooks become audiobooks without anyone starting a conversion. |
| `gluetun-stack-restart` | `gluetun_periodic_restart_enabled` (and gluetun on) | every `gluetun_periodic_restart_interval` (2h) | A workaround for VPN stalls; whether it is still needed is being measured. |
| `nas-db-dump` | `nas_db_dumps_enabled` | `nas_db_dump_time` (01:30 nightly) | A consistent logical copy of each database for backups. |
| `healthchecks-ping` | `healthchecks_enabled` | every `healthchecks_ping_minutes` (15) | An outside service raises the alarm when the NAS stops pinging it. |

Each job keeps its app's switch: set it in your inventory as before. A job that is off has its
timer stopped and disabled. Running an app's tag (`make run TAGS=gluetun`) brings its job in line
too, as does `TAGS=nas_maintenance` for all of them.

To see them on the NAS: `systemctl list-timers 'ansible-nas-*' 'ebook2audiobook-*' 'gluetun-*' 'nas-*' 'healthchecks-*'`.

## Adding one

Add the job to `nas_scheduled_jobs` with its `name`, `description`, `why`, `enabled`, a schedule
(`on_calendar`, or `every` for an interval) and its script under
`roles/nas_maintenance/templates/jobs/`; add its row here.
