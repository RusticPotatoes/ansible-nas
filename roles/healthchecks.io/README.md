# healthchecks.io

Pings a [healthchecks.io](https://healthchecks.io/) check from the NAS with `curl`, so an outside service raises the alarm when the NAS stops pinging it. It runs no container: the ping is the `healthchecks-ping` scheduled job (a systemd timer) of the `nas_maintenance` role.

No port: the NAS only makes outgoing requests.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `healthchecks_enabled` | `false` | Turns on the `healthchecks-ping` job. |
| `healthchecks_ping_minutes` | `15` | Minutes between pings; match the period set on healthchecks.io. |
| `healthchecks_url` | `""` | The check's ping URL from healthchecks.io. Set it in your own vars. |

The role's own tasks are empty.

Application page: `website/docs/applications/system-tools/healthchecks.io.md`.

Tests: a molecule scenario in `molecule/`.
