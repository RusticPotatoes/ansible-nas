# deluge

Runs Deluge, the BitTorrent client, in a container (`linuxserver/deluge`), with its web UI.

Variables (from `defaults/main.yml`):

| Variable | Default | Purpose |
|---|---|---|
| `deluge_enabled` | `false` | Deploy the container |
| `deluge_available_externally` | `false` | Expose through Traefik (`traefik.enable` label) |
| `deluge_config_directory` | `{{ docker_home }}/deluge/config` | Config directory |
| `deluge_download_directory` | `{{ downloads_root }}` | Downloads |
| `deluge_watch_directory` | `{{ torrents_root }}` | Watch directory for torrent files |
| `deluge_user_id` | `"0"` | PUID |
| `deluge_group_id` | `"0"` | PGID |
| `deluge_log_level` | `"error"` | Log level |
| `deluge_port` | `"8112"` | Host port published for the web UI |
| `deluge_hostname` | `"deluge"` | Hostname for the Traefik route |
| `deluge_timezone` | `{{ ansible_nas_timezone }}` | Container timezone (`TZ`) |
| `deluge_memory` | `1g` | Container memory limit |
| `deluge_container_name` | `deluge` | Container name |

Port: the web UI listens on 8112 inside the container; it is published on `deluge_port` (default 8112) unless the VPN download stack is enabled (`vpn_download_stack_enabled`), in which case the container runs in the gluetun network and no port is published here.
