# traefik

Runs Traefik, the reverse proxy that gives outside access to the NAS's applications, in a container. It requests and renews a wildcard Let's Encrypt certificate for `ansible_nas_domain` through a DNS challenge, and routes each application whose `<app>_available_externally` is `true`.

Ports: HTTP `80` (`traefik_port_http`, redirected to HTTPS), HTTPS `443` (`traefik_port_https`) and the dashboard `8083` (`traefik_port_ui`). The container uses the host's network, so these are the host's ports. Ports 80 and 443 must be forwarded from your router to the NAS.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `traefik_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `traefik_data_directory` | `"{{ docker_home }}/traefik"` | Holds the templated `traefik.toml` and the `letsencrypt` folder with the certificates (`acme.json`). |
| `traefik_port_http` | `"80"` | Port of the `web` entry point, which redirects to HTTPS. |
| `traefik_port_https` | `"443"` | Port of the `websecure` entry point. |
| `traefik_port_ui` | `"8083"` | Port of the dashboard and API (insecure mode, not routed through TLS). |
| `traefik_container_name` | `"traefik"` | Name of the Docker container. |
| `traefik_image_name` | `"traefik"` | Docker image. |
| `traefik_image_version` | `"latest"` | Image tag. |
| `traefik_log_level` | `"INFO"` | Traefik's log level. |
| `traefik_dns_provider` | `cloudflare` | DNS provider for the ACME DNS challenge (a lego provider name). |
| `traefik_environment_variables` | see below | Environment of the container: the credentials your DNS provider needs. The default token is a placeholder: set yours in your own vars, never in git. |
| `traefik_acme_server` | `"https://acme-v02.api.letsencrypt.org/directory"` | ACME server; the default is Let's Encrypt production. `defaults/main.yml` notes the staging URL. |
| `traefik_memory` | `1g` | Container memory limit. |

Default of `traefik_environment_variables`:

```yaml
traefik_environment_variables:
  CF_DNS_API_TOKEN: "abcdabcd123412341234"
```

The certificate's email comes from `ansible_nas_email`. The container mounts the Docker socket read-only to discover containers; only those with `traefik.enable` set are exposed. It also exposes Prometheus metrics.

Application page: `website/docs/applications/other/traefik.md`.

Tests: a molecule scenario in `molecule/`.
