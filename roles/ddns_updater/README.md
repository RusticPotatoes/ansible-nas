# ddns_updater

Runs DDNS Updater (`qmcgaw/ddns-updater`), a light container with a web UI that updates DNS A and/or AAAA records periodically for many DNS providers.

Web interface: port `8202` (`ddns_updater_port`), published to the container's port 8000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ddns_updater_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `ddns_updater_available_externally` | `"false"` | Value of the container's `traefik.enable` label. |
| `ddns_updater_data_directory` | `"{{ docker_home }}/ddns_updater"` | Holds the generated `config.json`, mounted at `/updater/data`. |
| `ddns_updater_port` | `8202` | Host port published to the container's port 8000. |
| `ddns_updater_hostname` | `"ddns-updater"` | Subdomain Traefik uses when it is available externally. |
| `ddns_updater_container_name` | `ddns_updater` | Name of the Docker container. |
| `ddns_updater_memory` | `1g` | Container memory limit. |
| `ddns_updater_period` | `5m` | `PERIOD`: how often the public IP is checked. |
| `ddns_updater_cooldown_period` | `5m` | `UPDATE_COOLDOWN_PERIOD`: wait between updates of one record, to avoid rate limits. |
| `ddns_updater_http_timeout` | `10s` | `HTTP_TIMEOUT` for all HTTP requests. |

You must set `ddns_updater_config` (no default here): the updater's settings, written as `config.json`; the play fails without it. See the commented example in `defaults/main.yml` and the application page. Optional, with no default here: `ddns_updater_gotify_token` and `gotify_url` for Gotify notifications. The image is `qmcgaw/ddns-updater:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/system-tools/ddns_updater.md`.
