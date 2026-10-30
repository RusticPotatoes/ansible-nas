# freshrss

Runs FreshRSS, a self-hosted, multi-user RSS feed aggregator, in a container.

Web interface: port `8089` (`freshrss_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `freshrss_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `freshrss_available_externally` | `false` | Lets Traefik route `freshrss_hostname`.`ansible_nas_domain` to it. |
| `freshrss_data_directory` | `"{{ docker_home }}/freshrss"` | FreshRSS's folder; its `data` subfolder is mounted at `/var/www/FreshRSS/data`. |
| `freshrss_extensions_directory` | `"{{ docker_home }}/freshrss"` | Its `extensions` subfolder is mounted at `/var/www/FreshRSS/extensions`. |
| `freshrss_port` | `"8089"` | Host port published to the container's port 80. |
| `freshrss_hostname` | `"freshrss"` | Subdomain Traefik uses when it is available externally. |
| `freshrss_container_name` | `freshrss` | Name of the Docker container. |
| `freshrss_image_name` | `"freshrss/freshrss"` | Docker image. |
| `freshrss_image_version` | `latest` | Image tag. |
| `freshrss_memory` | `1g` | Container memory limit. |

Feeds are refreshed at minutes 1 and 31 of each hour (`CRON_MIN`, set in the tasks).

Application page: `website/docs/applications/news/freshrss.md`.

Tests: a molecule scenario in `molecule/`.
