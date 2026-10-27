# ollama

Runs the Ollama model server in a container, for the lab's local AI assistant (Endora's chat).

- Enable: `ollama_enabled` (default `false`).
- Port: `ollama_port` (default `11434`); image `ollama_image_name` / `ollama_image_version`.
- Memory limit: `ollama_memory` (default `12g`).
- Tuning: `ollama_context_length` (per-request window), `ollama_num_parallel` (requests served at once), `ollama_keep_alive` (how long a model stays loaded). The defaults and the reasons for them are commented in `defaults/main.yml`.
- Data: `ollama_data_directory` under `docker_home`.

Application page: none yet under `website/docs/applications/`. Other roles use this server: `open-webui` and `librechat` point their `*_ollama_url` at it.
