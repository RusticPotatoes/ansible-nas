# sickchill

Runs SickChill, a TV show manager, in a container.

- Enable: `sickchill_enabled` (default `false`); `sickchill_available_externally` controls outside access.
- Port: `sickchill_port` (default `8081`); hostname `sickchill_hostname`.
- Image: `sickchill_image_name` (`linuxserver/sickchill`) / `sickchill_image_version` (default `latest`).
- Memory limit: `sickchill_memory` (default `1g`).
- Media: `sickchill_tv_directory` for shows, `sickchill_downloads_directory` (completed downloads); config under `sickchill_config_directory`.
- Runs as `sickchill_user_id` / `sickchill_group_id` (default `0`).

Application page: none yet under `website/docs/applications/` (the nearest is `sonarr`, a TV manager).

Tests: a molecule scenario in `molecule/`.
