# deluge

Runs Deluge, the BitTorrent client, in a container.

- Enable: `deluge_enabled` (default `false`); `deluge_available_externally` controls outside access.
- Port: `deluge_port` (default `8112`); hostname `deluge_hostname` (default `deluge`).
- Log level: `deluge_log_level` (default `error`).
- Timezone: `deluge_timezone` (default `{{ ansible_nas_timezone }}`).
- Memory limit: `deluge_memory` (default `1g`).
- Media: `deluge_download_directory` and `deluge_watch_directory`; config under `deluge_config_directory`.
- Runs as `deluge_user_id` / `deluge_group_id` (default `0`).
- Container name: `deluge_container_name` (default `deluge`).
