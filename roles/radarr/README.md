# radarr

Runs Radarr, the movie collection manager, in a container.

- Enable: `radarr_enabled` (default `false`); `radarr_available_externally` controls outside access.
- Port: `radarr_port` (default `7878`); hostname `radarr_hostname` (default `radarr`).
- Image: `radarr_image_name` (default `linuxserver/radarr`) / `radarr_image_version` (default `latest`).
- Memory limit: `radarr_memory` (default `1g`).
- Media: `radarr_movies_directory` and `radarr_download_directory`; config under `radarr_data_directory`.
- Runs as `radarr_user_id` / `radarr_group_id` (default `0`).
- Container name: `radarr_container_name` (default `radarr`).
