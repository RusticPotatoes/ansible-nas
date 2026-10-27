# znc

Runs ZNC, an IRC bouncer, in a container, so an IRC connection stays up between clients.

- Enable: `znc_enabled` (default `false`); `znc_available_externally` controls outside access.
- Port: `znc_port` (default `6677`); hostname `znc_hostname`.
- Image: `znc_image_name` / `znc_image_version` (default `latest`).
- Memory limit: `znc_memory` (default `1g`).
- Data: `znc_data_directory` under `docker_home`.
- User: `znc_user_nick`, `znc_user_altnick`, `znc_user_ident`, `znc_user_real_name`. Set `znc_user_password` in your own vars, never in git; the default in `defaults/main.yml` is a placeholder.

Application page: none yet under `website/docs/applications/`.

Tests: a molecule scenario in `molecule/`.
