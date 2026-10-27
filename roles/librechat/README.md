# librechat

Runs LibreChat, a multi-model chat web app, in a container, with its MCP server data directory.

- Enable: `librechat_enabled` (default `false`); `librechat_available_externally` controls outside access.
- Port: `librechat_port` (default `3080`); hostname `librechat_hostname`; image `librechat_image_name` / `librechat_image_version` (default `latest`).
- Memory limit: `librechat_memory` (default `4g`).
- Models: `librechat_ollama_base_url` points at the `ollama` server (port 11434 by default).
- Media mounts: books, audiobooks and downloads directories, from `books_root`, `audiobooks_root` and `downloads_root`.
- Secrets: `librechat_encryption_key`, `librechat_jwt_secret`, `librechat_admin_email` and `librechat_admin_password` read `vault_*` variables. Set them in the vault before enabling; never in git.

Application page: none yet under `website/docs/applications/`.
