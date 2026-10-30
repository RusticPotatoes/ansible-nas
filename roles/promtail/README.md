# promtail

Runs Promtail, an agent that ships logs to Grafana Loki, in a container. It discovers the Docker containers through the Docker socket and pushes their logs, labelled by container name, to Loki.

Web interface: port `9080` (`promtail_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `promtail_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `promtail_available_externally` | `false` | Lets Traefik route `promtail_hostname`.`ansible_nas_domain` to it. |
| `promtail_data_directory` | `"{{ docker_home }}/promtail"` | Holds `config/config.yml` (mounted at `/etc/promtail/config.yml`) and `data/` (mounted at `/data`). |
| `promtail_hostname` | `"promtail"` | Subdomain Traefik uses when it is available externally. |
| `promtail_network_name` | `"promtail"` | Docker network name. Not used by the tasks yet. |
| `promtail_port` | `"9080"` | Host port published to the container's port 9080. |
| `promtail_container_name` | `"promtail"` | Name of the Docker container. |
| `promtail_image_name` | `"grafana/promtail"` | Docker image. |
| `promtail_image_version` | `"latest"` | Image tag. |
| `promtail_memory` | `"1g"` | Container memory limit. |
| `promtail_loki_url` | `http://{{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}:{{ loki_http_port }}/loki/api/v1/push` | Loki push URL written into the config. |

Promtail needs Loki: the play fails when `loki_enabled` is false, and the role loads the `loki` role's defaults for `loki_http_port`.

Application page: `website/docs/applications/system-tools/promtail.md`.
