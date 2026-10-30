# stats

Runs a metrics stack for the NAS in containers: Prometheus, Grafana, Telegraf and a few exporters (smartctl, hddtemp, and optionally an internet speed test). Telegraf also exposes an InfluxDB endpoint for applications that need one. Grafana is provisioned with the Ansible-NAS dashboards and alert rules.

Ports: Grafana `3000` (`stats_grafana_port`), Prometheus `9090` (`stats_prometheus_port`), Telegraf's Prometheus endpoint `9273` (`stats_telegraf_port`) and InfluxDB endpoint `8086` (`stats_telegraf_influxdb_port`), the smartctl exporter `9902` (`stats_prometheus_smartctl_port`), hddtemp `7634` (`stats_hddtemp_port`) and the speed test exporter `9798` (`stats_speedtest_exporter_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `stats_enabled` | `false` | Starts the stack when `true`; removes the containers when `false`. |
| `stats_internet_speed_test_enabled` | `false` | Runs the speed test exporter and adds it to Prometheus's scrape jobs. |
| `stats_prometheus_available_externally` | `false` | Lets Traefik route `stats_prometheus_hostname`.`ansible_nas_domain` to Prometheus. |
| `stats_grafana_available_externally` | `false` | Lets Traefik route `grafana`.`ansible_nas_domain` to Grafana. |
| `stats_telegraf_config_directory` | `"{{ docker_home }}/stats/telegraf/config"` | Holds the templated `telegraf.conf`, mounted at `/etc/telegraf/`. |
| `stats_prometheus_data_directory` | `"{{ docker_home }}/stats/prometheus/data"` | Prometheus's database, mounted at `/prometheus`. |
| `stats_prometheus_config_directory` | `"{{ docker_home }}/stats/prometheus/config"` | Holds the templated `prometheus.yml` and `alert_rules.yml`. |
| `stats_grafana_data_directory` | `"{{ docker_home }}/stats/grafana/data"` | Grafana's data, mounted at `/var/lib/grafana`. |
| `stats_grafana_config_directory` | `"{{ docker_home }}/stats/grafana/config"` | Holds Grafana's provisioning (data source, dashboards, alerting) and the dashboard files. |
| `stats_prometheus_port` | `"9090"` | Host port published to the container's port 9090. |
| `stats_telegraf_port` | `"9273"` | Host port published to the container's port 9273. |
| `stats_telegraf_influxdb_port` | `"8086"` | Host port published to the container's port 8086. |
| `stats_prometheus_smartctl_port` | `"9902"` | Host port published to the container's port 9902. |
| `stats_speedtest_exporter_port` | `"9798"` | Host port published to the container's port 9798. |
| `stats_hddtemp_port` | `"7634"` | Host port published to the container's port 7634. |
| `stats_prometheus_hostname` | `"prometheus"` | Subdomain Traefik uses when it is available externally. |
| `stats_grafana_port` | `"3000"` | Host port published to the container's port 3000. |
| `stats_grafana_hostname` | `"grafana"` | Grafana's hostname. Not used by the tasks: the Traefik rule names `grafana` directly. |
| `stats_grafana_container_name` | `"stats-grafana"` | Name of the Docker container. |
| `stats_grafana_image_name` | `"grafana/grafana"` | Docker image. |
| `stats_grafana_image_version` | `"latest"` | Image tag. |
| `stats_prometheus_container_name` | `"stats-prometheus"` | Name of the Docker container. |
| `stats_prometheus_image_name` | `"prom/prometheus"` | Docker image. |
| `stats_prometheus_image_version` | `"latest"` | Image tag. |
| `stats_telegraf_container_name` | `"stats-telegraf"` | Name of the Docker container. |
| `stats_telegraf_image_name` | `"telegraf"` | Docker image. |
| `stats_telegraf_image_version` | `"latest"` | Image tag. |
| `stats_smartctl_container_name` | `"stats-smartctl"` | Name of the Docker container. |
| `stats_smartctl_docker_image_name` | `"matusnovak/prometheus-smartctl"` | Docker image. |
| `stats_smartctl_docker_image_version` | `"latest"` | Image tag. |
| `stats_speedtest_container_name` | `"stats-speedtest"` | Name of the Docker container. |
| `stats_speedtest_docker_image_name` | `"miguelndecarvalho/speedtest-exporter"` | Docker image. |
| `stats_speedtest_docker_image_version` | `"latest"` | Image tag. |
| `stats_hddtemp_docker_container_name` | `"stats-hddtemp"` | Name of the Docker container. |
| `stats_hddtemp_docker_image_name` | `"modem7/hddtemp-docker"` | Docker image. |
| `stats_hddtemp_docker_image_tag` | `"latest"` | Image tag of the hddtemp container. |
| `stats_telegraf_memory` | `1g` | Memory limit. Not used by the tasks: they set `1g` directly. |
| `stats_prometheus_memory` | `1g` | Container memory limit. |
| `stats_prometheus_smartctl_memory` | `1g` | Container memory limit. |
| `stats_hddtemp_memory` | `128m` | Container memory limit. |
| `stats_speedtest_exporter_memory` | `256m` | Container memory limit. |
| `stats_grafana_memory` | `1g` | Memory limit. Not used by the tasks: they set `1g` directly. |
| `stats_telegram_bot_token` | `"{{ vault_ansible_nas_telegram_bot_token }}"` | Bot token of Grafana's Telegram contact point. Set `vault_ansible_nas_telegram_bot_token` in your vault, never in git. |
| `stats_telegram_chat_id` | `"{{ vault_ansible_nas_telegram_chat_id }}"` | Chat ID of that contact point, from `vault_ansible_nas_telegram_chat_id`. |
| `stats_loki_logs_error_threshold` | `60` | Alert when the logs hold more than this many errors in 5 minutes. |
| `stats_loki_container_logs_error_threshold` | `120` | Alert when one container logs more than this many errors in 5 minutes. |
| `stats_loki_container_logs_error_anomaly_floor` | `30` | Error-anomaly alert: the least errors in 5 minutes a container must log to count. |
| `stats_loki_container_logs_error_anomaly_stddev_multiplier` | `4` | Error-anomaly alert: how many standard deviations above its baseline a container must be. |
| `stats_gatus_endpoint_alert_window` | `3m` | Alert when Gatus has reported an endpoint down for this whole window. |
| `stats_gatus_endpoint_alert_for` | `2m` | How long that condition holds before the alert fires. |
| `stats_prometheus_retention_time` | `365d` | How long Prometheus keeps data (`--storage.tsdb.retention.time`). |
| `stats_prometheus_retention_size` | `30GB` | Most disk Prometheus uses (`--storage.tsdb.retention.size`). |
| `stats_collection_interval` | `15s` | Prometheus scrape interval and Telegraf collection interval. |
| `stats_speedtest_collection_interval` | `1h` | Scrape interval of the speed test exporter. |
| `stats_prometheus_scrape_jobs` | `[]` | Extra Prometheus scrape jobs: each has a `name` and `targets`, and optionally `metrics_path`, `scheme`, `scrape_interval`, `scrape_timeout`, `bearer_token` or `authorization`. |

The templates also read two optional variables with no default: `stats_prometheus_additional_hosts` (more `host:port` targets to scrape, for example `192.168.1.10:9100`) and `stats_hass_long_lived_access_token` (scrapes Home Assistant when `homeassistant_enabled` is on; set it in your own vars, never in git). Grafana also gets a Loki data source (port `loki_http_port`, default 3100), which the log alerts query, so they need the `loki` role; Prometheus scrapes Gatus when `gatus_enabled` is on, which the endpoint alert needs. The hddtemp container mounts `/dev` read-only.

Application page: `website/docs/applications/monitoring/stats.md`.

Tests: a molecule scenario in `molecule/`.
