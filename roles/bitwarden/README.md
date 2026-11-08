# bitwarden

Runs Vaultwarden (`vaultwarden/server`), a lightweight Bitwarden-compatible password server, in a container, with a second container (`bruceforce/bw_backup`) that backs up its data.

Ports: the web vault on `19080` (`bitwarden_port_a`, container port 80) and the websocket on `3012` (`bitwarden_port_b`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `bitwarden_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `bitwarden_available_externally` | `false` | Lets Traefik route `bitwarden_hostname`.`ansible_nas_domain` to it. |
| `bitwarden_data_directory` | `"{{ docker_home }}/bitwarden"` | Vaultwarden's data, mounted at `/data`. |
| `bitwarden_port_a` | `"19080"` | Host port published to the container's port 80 (web vault). |
| `bitwarden_port_b` | `"3012"` | Host port published to the container's port 3012 (websocket). |
| `bitwarden_hostname` | `"bitwarden"` | Subdomain Traefik uses when it is available externally. |
| `bitwarden_ip_allowlist` | `"0.0.0.0/0"` | Source range for the Traefik IP allowlist middleware. |
| `bitwarden_admin_token` | `qwertyuiop1234567890poiuytrewq0987654321` | `ADMIN_TOKEN`, the password of the `/admin` area. The default is a placeholder: set a long random string in your own vars, never in git. |
| `bitwarden_allow_signups` | `false` | `SIGNUPS_ALLOWED`. Turn on, run the playbook, create your users, then turn it off and run again. |
| `bitwarden_memory` | `1g` | Memory limit of the Vaultwarden container. |
| `bitwarden_backup_memory` | `1g` | Memory limit of the backup container. |
| `bitwarden_container_name` | `bitwarden` | Name of the Docker container. |
| `bitwarden_backup_container_name` | `bitwarden-backup` | Name of the backup container. |

Both images (`vaultwarden/server:latest`, `bruceforce/bw_backup:latest`) are set in the tasks rather than in defaults. The play fails if the old `bitwarden_ip_whitelist` is still set: use `bitwarden_ip_allowlist`.

Application page: `website/docs/applications/other/bitwarden.md`.

Tests: a molecule scenario in `molecule/`.
