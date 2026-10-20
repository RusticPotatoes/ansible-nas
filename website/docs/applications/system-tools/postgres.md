---
title: "PostgreSQL"
---

Homepage: [https://www.postgresql.org/](https://www.postgresql.org/)

PostgreSQL is an open source relational database.

## Usage

Set `postgres_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

* Port: `5432` (`postgres_port`), hostname `postgres_hostname` (default `postgres`)
* Data directory: `postgres_data_directory` (default `<docker_home>/postgres`)
* Image: `postgres`, version `postgres_image_version` (default `16-alpine`)
* Allowed client addresses: `postgres_ip_allowlist` (default `0.0.0.0/0`, narrow it)
* Memory limit: `postgres_memory` (default `1g`)
* Container name: `postgres_container_name` (default `postgres`)

Available externally only if `postgres_available_externally: true`.

Pin the image version: on-disk data cannot jump major versions.

**For more info visit: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)**
