# flaresolverr

Runs FlareSolverr, a proxy server that gets past Cloudflare and DDoS-GUARD protection for indexers that need it, in a container (`flaresolverr/flaresolverr`).

API: port `8191` (`flaresolverr_port`). When `vpn_download_stack_enabled` is on, FlareSolverr joins gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `flaresolverr_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `flaresolverr_available_externally` | `false` | Lets Traefik route `flaresolverr_hostname`.`ansible_nas_domain` to it. |
| `flaresolverr_config_directory` | `"{{ docker_home }}/flaresolverr"` | Configuration, mounted at `/config`. |
| `flaresolverr_port` | `"8191"` | Host port published to the container's port 8191. |
| `flaresolverr_memory` | `200m` | Container memory limit. |
| `flaresolverr_container_name` | `flaresolverr` | Name of the Docker container. |

The image is `flaresolverr/flaresolverr` (tag `latest`), set in the tasks rather than in defaults. There is no hostname variable: the Traefik route uses `flaresolverr`.

Application page: `website/docs/applications/download-tools/flaresolverr.md`.

Tests: a molecule scenario in `molecule/`.
