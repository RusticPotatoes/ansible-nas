# rssbridge

Runs RSS-Bridge, which generates RSS and Atom feeds for websites that do not have one, in a container. It is not a feed reader: its feeds are meant for a reader or aggregator.

Web interface: port `8091` (`rssbridge_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `rssbridge_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `rssbridge_available_externally` | `false` | Lets Traefik route `rssbridge_hostname`.`ansible_nas_domain` to it. |
| `rssbridge_data_directory` | `"{{ docker_home }}/rssbridge"` | Base folder; its `data` subfolder is mounted at `/config`. |
| `rssbridge_port` | `"8091"` | Host port published to the container's port 80. |
| `rssbridge_hostname` | `"rssbridge"` | Subdomain Traefik uses when it is available externally. |
| `rssbridge_container_name` | `"rssbridge"` | Name of the Docker container. |
| `rssbridge_image_name` | `"rssbridge/rss-bridge"` | Docker image. |
| `rssbridge_image_version` | `"latest"` | Image tag. |
| `rssbridge_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/news/rssbridge.md`.

Tests: a molecule scenario in `molecule/`.
