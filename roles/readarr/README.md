# readarr

Runs Readarr, the book collection manager, in a container.

- Enable: `readarr_enabled` (default `false`); `readarr_available_externally` controls outside access.
- Port: `readarr_port` (default `8787`); hostname `readarr_hostname`.
- Image: `readarr_image_name` (`ghcr.io/linuxserver/readarr`) / `readarr_image_version` (default `develop`).
- Memory limit: `readarr_memory` (default `1g`).
- Media: `readarr_books_directory` and `readarr_download_directory`; config under `readarr_data_directory`.
- Runs as `readarr_user_id` / `readarr_group_id` (default `0`).

Application page: none yet under `website/docs/applications/` (the nearest is `lidarr`, a music manager).

Tests: a molecule scenario in `molecule/`.
