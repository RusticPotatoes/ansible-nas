---
title: "Odysseus"
---

Homepage: [https://github.com/odysseus-dev/odysseus](https://github.com/odysseus-dev/odysseus)

A self-hosted AI workspace: chat, agents with tools, long-term memory and documents, served by
the models you already run. This role runs it with its ChromaDB (vector memory) and SearXNG (web search),
on a private network of their own, and points it at
the Ollama role for models, so it needs no GPU of its own.

## Usage

1. Put `vault_odysseus_admin_password` (12 characters or more) in your vault. It seeds the
   `admin` account on the first boot only; change it later in the app's Settings.
2. Set `odysseus_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The web interface can be found at [http://ansible_nas_host_or_ip:7011](http://ansible_nas_host_or_ip:7011).
Log in as `admin`, then add Ollama under Settings if its models are not listed.

## Specific configuration

- Memory limits: `odysseus_memory` (`4g`), `odysseus_chromadb_memory` (`1g`) and
  `odysseus_searxng_memory` (`512m`): 5.5 GB at most in all.
- Upstream's compose also runs ntfy for push reminders. This role leaves it out: point Settings
  at any ntfy server you already use, such as ntfy.sh.
- Embeddings run inside the app (fastembed, about 50 MB) unless `EMBEDDING_URL` points elsewhere.
- Odysseus agents can run shell and file tools behind approval gates. The role mounts no Docker
  socket and no host folders beyond its own data. Keep it on the LAN:
  `odysseus_available_externally` stays `false` unless you put it behind Traefik with HTTPS.
