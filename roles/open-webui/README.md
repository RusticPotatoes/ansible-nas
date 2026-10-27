# open-webui

Runs Open WebUI, a browser chat front end, in a container. It talks to the Ollama server in `ollama`.

- Enable: `open_webui_enabled` (default `false`).
- Port: `open_webui_port` (default `8090`); image `open_webui_image_name` / `open_webui_image_version` (default `main`).
- Memory limit: `open_webui_memory` (default `2g`).
- Ollama endpoint: `open_webui_ollama_url`, built from the host address and port 11434 by default.
- Data: `open_webui_data_directory` under `docker_home`.

Application page: none yet under `website/docs/applications/`.
