# cloudflare_ddns

Runs a Cloudflare dynamic DNS updater (`joshava/cloudflare-ddns`) in a container: it keeps a Cloudflare DNS record pointed at your current public IP.

No port: the container only makes outbound calls to Cloudflare.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `cloudflare_ddns_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `cloudflare_data_directory` | `"{{ docker_home }}/cloudflare_ddns"` | Holds the templated `config.yml`, mounted at `/app/config.yaml`. |
| `cloudflare_zone` | `"{{ ansible_nas_domain }}"` | Cloudflare zone (your domain). |
| `cloudflare_host` | `"*.{{ cloudflare_zone }}"` | Record the container updates; by default a wildcard under the zone. |
| `cloudflare_token` | `"abcdabcdabcd123412341234"` | Scoped API token with DNS:Edit and Zone:Read. The default is a placeholder: set it in your own vars, never in git. |
| `cloudflare_proxy` | `false` | Send traffic through the Cloudflare CDN. Must stay `false` for a wildcard host. |
| `cloudflare_type` | `"A"` | Record type: `A` for IPv4, `AAAA` for IPv6. |
| `cloudflare_memory` | `512MB` | Container memory limit. |
| `cloudflare_container_name` | `cloudflare-ddns` | Name of the Docker container. |

The play fails if the deprecated `cloudflare_api_key` is set: global API keys are no longer supported. The image is `joshava/cloudflare-ddns:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/system-tools/cloudflare_ddns.md`.

Tests: a molecule scenario in `molecule/`.
