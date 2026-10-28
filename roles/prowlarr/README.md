# prowlarr

Runs Prowlarr, an indexer and downloader manager for *arr applications, in a container.

- Enable: `prowlarr_enabled` (default `false`); `prowlarr_available_externally` controls outside access.
- Port: `prowlarr_port` (default `9696`); hostname `prowlarr_hostname` (default `prowlarr`).
- Container: `prowlarr_container_name` (default `prowlarr`).
- Image: `prowlarr_image_name` (`ghcr.io/linuxserver/prowlarr`) / `prowlarr_image_version` (default `develop`).
- Memory limit: `prowlarr_memory` (default `1g`).
- Config: `prowlarr_data_directory` (default `{{ docker_home }}/prowlarr/config`).
- Runs as `prowlarr_user_id` / `prowlarr_group_id` (default `0`).
