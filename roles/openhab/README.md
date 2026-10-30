# openhab

Runs openHAB, a vendor- and technology-agnostic open source home automation platform, in a container.

Web interface: HTTP on `7777` (`openhab_port_http`) and HTTPS on `7778` (`openhab_port_https`). The container uses the host's network, so these are the ports openHAB itself listens on.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `openhab_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `openhab_available_externally` | `false` | Lets Traefik route `openhab_hostname`.`ansible_nas_domain` to it. |
| `openhab_data_directory` | `"{{ docker_home }}/openhab"` | Holds `conf/`, `userdata/` and `addons/`, mounted under `/openhab`. Owned by the `openhab` user (uid and gid 9001), which the role creates. |
| `openhab_port_http` | `"7777"` | HTTP port (`OPENHAB_HTTP_PORT`). |
| `openhab_port_https` | `"7778"` | HTTPS port (`OPENHAB_HTTPS_PORT`). |
| `openhab_hostname` | `"openhab"` | Subdomain Traefik uses when it is available externally. |
| `openhab_container_name` | `"openhab"` | Name of the Docker container. |
| `openhab_image_name` | `"openhab/openhab"` | Docker image. |
| `openhab_image_version` | `"latest"` | Image tag. |
| `openhab_memory` | `1g` | Container memory limit. |

Traefik routes to port 7777, written in the tasks rather than read from `openhab_port_http`.

Application page: `website/docs/applications/home-automation/openhab.md`.

Tests: a molecule scenario in `molecule/`.
