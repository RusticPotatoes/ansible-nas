# cloudflared

Runs `cloudflared`, Cloudflare's tunnel connector, in a container: it keeps an outbound connection to Cloudflare so that routes set in the Zero Trust dashboard reach services without an open port.

No port: the tunnel is outbound only.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `cloudflared_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `cloudflared_container_name` | `"cloudflared"` | Name of the Docker container. |
| `cloudflared_image_name` | `"cloudflare/cloudflared"` | Docker image. |
| `cloudflared_image_version` | `"latest"` | Image tag. |
| `cloudflared_memory` | `256m` | Container memory limit. |
| `cloudflared_tunnel_token` | `"{{ vault_cloudflared_tunnel_token \| default('') }}"` | Tunnel token from the Zero Trust dashboard, read from `vault_cloudflared_tunnel_token`. Set that in your vault, never in git; while it is empty the role deploys nothing and prints a reminder. |

Application page: `website/docs/applications/other/cloudflared.md`.
