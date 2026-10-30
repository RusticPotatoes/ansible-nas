# loki

Runs Loki, a log aggregation system that stores and queries logs from your applications, in a container. It stores its data in MinIO and is searched from Grafana.

HTTP API: port `3100` (`loki_http_port`). Loki has no web interface of its own; the container's ports 7946 and 9095 are also published, on random host ports.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `loki_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `loki_available_externally` | `false` | Lets Traefik route `loki_hostname`.`ansible_nas_domain` to it. |
| `loki_data_directory` | `"{{ docker_home }}/loki"` | Holds the templated `config.yml` (mounted at `/etc/loki/config.yml`) and `rules/` (mounted at `/loki/rules`). |
| `loki_hostname` | `"loki"` | Subdomain Traefik uses when it is available externally. |
| `loki_network_name` | `"loki"` | Name kept for a Loki network; the tasks do not use it. |
| `loki_http_port` | `"3100"` | Host port published to the container's port 3100. |
| `loki_container_name` | `"loki"` | Name of the Docker container. |
| `loki_image_name` | `"grafana/loki"` | Docker image. |
| `loki_image_version` | `"latest"` | Image tag. |
| `loki_memory` | `"1g"` | Container memory limit. |
| `loki_log_retention` | `672h` | How long logs are kept, in the Loki config. |
| `loki_log_level` | `warn` | Loki's log level. |

The tasks fail unless `minio_enabled` and `grafana_enabled` are on (the `logging` role turns on all of them). They read the `stats` role's defaults, create Loki's buckets under `minio_data_directory`, log in to MinIO with `minio_admin_username` and `minio_admin_password`, add Loki as a Grafana data source and restart Grafana. A changed config restarts the container.

Application page: `website/docs/applications/system-tools/loki.md`.
