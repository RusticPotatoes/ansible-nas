---
title: "Loki"
---

Homepage: [https://grafana.com/oss/loki/](https://grafana.com/oss/loki/)

Docker Container: [Loki](https://hub.docker.com/r/grafana/loki)

Loki is a log aggregation system designed to store and query logs from all your applications and infrastructure.

## Log retention

`loki_log_retention` sets how long logs are kept. The default is `672h` (28 days). The compactor deletes logs, chunks and index entries older than this from the MinIO bucket, so storage does not grow without limit. Set a different period in your `inventories/<your_inventory>/group_vars/nas.yml` file, using Loki duration units such as `168h` (7 days).

## Usage

Set `loki_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

Loki doesn't have a web interface. To see what it's doing look at the container logs from your Ansible-NAS shell:

```bash
docker logs loki -f
```
