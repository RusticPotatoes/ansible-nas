# nzbget

Runs NZBGet, an Usenet downloader, in a container.

- Enable: `nzbget_enabled` (default `false`); `nzbget_available_externally` controls outside access.
- Port: `nzbget_port` (default `6789`); hostname `nzbget_hostname` (default `nzbget`).
- Container: `nzbget_container_name` (default `nzbget`).
- Image: `nzbget_image_name` (`linuxserver/nzbget`) / `nzbget_image_version` (default `latest`).
- Memory limit: `nzbget_memory` (default `1g`).
- Directories: `nzbget_data_directory` (default `{{ docker_home }}/nzbget`); `nzbget_download_directory` (default `{{ downloads_root }}`).
- Runs as `nzbget_user_id` / `nzbget_group_id` (default `0`).
