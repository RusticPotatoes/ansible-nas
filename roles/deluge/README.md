# deluge

Runs Deluge, the BitTorrent client, in a container. Port: **8112** (web UI).

## Variables (defaults/main.yml)

| Variable | Default | Purpose |
|---|---|---|
| `deluge_enabled` | `false` | Turn the role on |
| `deluge_available_externally` | `false` | Allow access from outside the network |
| `deluge_config_directory` | `{{ docker_home }}/deluge/config` | Config directory on the host |
| `deluge_download_directory` | `{{ downloads_root }}` | Download directory |
| `deluge_watch_directory` | `{{ torrents_root }}` | Watch directory for .torrent files |
| `deluge_user_id` | `"0"` | UID the container runs as |
| `deluge_group_id` | `"0"` | GID the container runs as |
| `deluge_log_level` | `"error"` | Log level |
| `deluge_port` | `"8112"` | Web UI port |
| `deluge_hostname` | `"deluge"` | Container hostname |
| `deluge_timezone` | `{{ ansible_nas_timezone }}` | Timezone for the container |
| `deluge_memory` | `1g` | Memory limit |
| `deluge_container_name` | `deluge` | Container name |
