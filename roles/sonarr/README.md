# sonarr

Runs Sonarr, the TV series automation tool, in a container.

- Enable: `sonarr_enabled` (default `false`); `sonarr_available_externally` controls outside access.
- Port: `sonarr_port` (default `8989`); hostname `sonarr_hostname` (default `sonarr`).
- Image: `sonarr_image_name` (default `linuxserver/sonarr`) / `sonarr_image_version` (default `latest`).
- Memory limit: `sonarr_memory` (default `1g`).
- Media: `sonarr_tv_directory` and `sonarr_download_directory`; config under `sonarr_data_directory`.
- Runs as `sonarr_user_id` / `sonarr_group_id` (default `0`).
- Container name: `sonarr_container_name` (default `sonarr`).
