# odysseus

Runs Odysseus, a self-hosted AI workspace (chat, agents, memory, documents), with the ChromaDB
it keeps its vector memory in and a SearXNG for web search. Models come from the Ollama server in `ollama`.

- Enable: `odysseus_enabled` (default `false`). Needs `vault_odysseus_admin_password` in vault.yml.
- Port: `odysseus_port` (default `7011`); image `odysseus_image_name` / `odysseus_image_version` (a pinned main build).
- Memory limits: `odysseus_memory` (`4g`), `odysseus_chromadb_memory` (`1g`), `odysseus_searxng_memory` (`512m`).
- Ollama endpoint: `odysseus_ollama_base_url`, built from the host address and port 11434 by default.
- Data: `odysseus_data_directory` under `docker_home`.

Application page: `website/docs/applications/other/odysseus.md`.
