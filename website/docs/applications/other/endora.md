---
title: "Endora"
---

Homepage: [https://github.com/RusticPotatoes/Endora](https://github.com/RusticPotatoes/Endora)

Endora is a self-hosted butler for the house: a chat console that reads your Home Assistant,
your mail copy (see [Mail Mirror](mail_mirror.md)) and your containers, using a model that
runs on your own hardware (see the `ollama` role).

This role checks out a branch or tag of Endora on the NAS, builds the image there and starts
it with Endora's own `docker-compose.yml`. Nothing is pulled from a registry. The Compose
project is named `endora`, the name Endora's `make deploy` uses, so a node deployed either way
is the same node with the same data. Deploying from a laptop with `make deploy` to try a
change, then running this role to go back to a branch, moves no data.

## Settings

```yaml
endora_enabled: true
endora_version: develop          # a branch, tag or commit
endora_own_work: true            # looks into things on its own when you are quiet
endora_utc_offset_minutes: -300  # your distance from UTC, for the patterns it notices
endora_docker_observer: true     # a read-only view of this host's containers
```

- **Mail** is mounted read-only from `mail_mirror_root` when the `mail_mirror` role is
  enabled; set `endora_mail_dir: ""` to keep it from Endora.
- **The model** defaults to the `ollama` role on this host (`endora_model_url`,
  `endora_model`).
- **The certificate.** The node serves HTTPS with a self-signed certificate issued for the
  NAS's own address (`endora_tls_san`, by default the address Ansible sees). Accept the
  browser's warning once.
- **Rebuilding.** The image is built again when the checkout moves. If it was replaced from
  elsewhere (a `make deploy`), set `endora_rebuild: true` for one run to go back to the branch.

## Where its data lives

Everything Endora keeps (every setting, API key and sign-in secret) is one SQLite database. By
default it is in the Docker volume `endora_endora-data`, which is **not** in your backups. To
keep it in a folder that is:

1. Copy the volume there with Endora's `make migrate-data` (it verifies every file and deletes
   nothing).
2. Set `endora_data_dir` to that folder, for example `"{{ docker_home }}/endora/data"`.

The role refuses to start on an empty `endora_data_dir` while the volume still holds a
database: that would be a brand-new node with no settings, which looks like data loss.

## Checking it

```bash
docker logs --tail 20 endora-node
```

The console's header shows the build (the short commit) that is running. Open it at
`https://<your-nas>:8787`.

## Turning it off

Set `endora_enabled: false` and run the role. It stops a node it started (it looks for its
own checkout under `endora_root`); a node started some other way is left alone. The data volume
is never removed.
