# deluge

Runs Deluge, a lightweight BitTorrent client, with its web interface, in a container.

Web interface: port `8112` (`deluge_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `deluge_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `deluge_available_externally` | `false` | Lets Traefik route `deluge_hostname`.`ansible_nas_domain` to it. |
| `deluge_config_directory` | `"{{ docker_home }}/deluge/config"` | Deluge's configuration, mounted at `/config`. |
| `deluge_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `deluge_watch_directory` | `"{{ torrents_root }}"` | Watch folder for `.torrent` files. Not used by the tasks yet. |
| `deluge_user_id` | `"0"` | User the container runs as (`PUID`) and owner of its folders. |
| `deluge_group_id` | `"0"` | Group the container runs as (`PGID`) and group of its folders. |
| `deluge_log_level` | `"error"` | Log level. Not used by the tasks yet. |
| `deluge_port` | `"8112"` | Host port published to the container's port 8112. |
| `deluge_hostname` | `"deluge"` | Subdomain Traefik uses when it is available externally. |
| `deluge_timezone` | `"{{ ansible_nas_timezone }}"` | Container time zone (`TZ`). |
| `deluge_memory` | `1g` | Container memory limit. |
| `deluge_container_name` | `deluge` | Name used to remove the container when disabled. The start task names it `deluge` directly. |

The image is `linuxserver/deluge` (tag `latest`), set in the tasks rather than in defaults.
When `vpn_download_stack_enabled` is on, Deluge joins gluetun's network and publishes no port
of its own. The Homepage widget reads the optional `deluge_web_password` (no default here; the
widget falls back to Deluge's stock first-login password, which should be changed on first use).

Application page: `website/docs/applications/download-tools/deluge.md`.

Tests: a molecule scenario in `molecule/`.
