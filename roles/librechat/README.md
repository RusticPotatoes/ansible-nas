# librechat

Runs LibreChat, a multi-model chat web app, in a container, with its MCP server data directory.

- Enable: `librechat_enabled` (default `false`); `librechat_available_externally` controls outside access.
- Port: `librechat_port` (default `3080`) is the host port only; LibreChat always listens on 3080 inside the container (`PORT`), and the mapping is `librechat_port:3080`. Hostname `librechat_hostname`; image `librechat_image_name` / `librechat_image_version` (default `latest`).
- Memory limit: `librechat_memory` (default `4g`).
- Models: `librechat_ollama_base_url` points at the `ollama` server (port 11434 by default).
- Media mounts: books, audiobooks and downloads directories, from `books_root`, `audiobooks_root` and `downloads_root`.
- Secrets: each reads its own `vault_*` variable, empty by default. The role refuses to start (with `librechat_enabled` true) if any is empty, if the encryption key is not 64 hex characters, or if the IV is not 32 hex characters. Set them in the vault; never in git.
  - `librechat_encryption_key` (`vault_librechat_encryption_key`): `CREDS_KEY`, 64 hex characters.
  - `librechat_creds_iv` (`vault_librechat_creds_iv`): `CREDS_IV`, 32 hex characters.
  - `librechat_jwt_secret` (`vault_librechat_jwt_secret`): `JWT_SECRET`.
  - `librechat_jwt_refresh_secret` (`vault_librechat_jwt_refresh_secret`): `JWT_REFRESH_SECRET` and `REFRESH_TOKEN_SECRET`.
  - `librechat_admin_email` (`vault_librechat_admin_email`; its default is set in `defaults/main.yml`) and `librechat_admin_password` (`vault_librechat_admin_password`, default empty).
- Access: `librechat_allow_registration` (default `false`) sets `ALLOW_REGISTRATION`; `librechat_allow_social_login` (default `false`) sets `ALLOW_SOCIAL_LOGIN`. Both are off unless set to true.

Application page: none yet under `website/docs/applications/`.
