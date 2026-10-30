# logging

Turns the logging stack on or off as one: application logs captured by Promtail, stored by Loki in MinIO, and searched in Grafana. It runs no container of its own.

No port of its own: see the `loki`, `minio`, `promtail` and Grafana (`stats`) roles.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `logging_stack_enabled` | `false` | When `true`, sets `grafana_enabled`, `minio_enabled`, `loki_enabled` and `promtail_enabled` to `true`; when `false`, sets them all to `false`. |

Because the role sets those four variables whenever it runs, they follow `logging_stack_enabled` rather than their own settings.

Application page: `website/docs/applications/stacks/logging.md`.
