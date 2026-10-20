---
title: "MongoDB"
---

Homepage: [https://www.mongodb.com/](https://www.mongodb.com/)

MongoDB is a document-oriented NoSQL database.

## Usage

Set `mongodb_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

* Port: `27017` (`mongodb_port`), hostname `mongodb_hostname` (default `mongodb`)
* Data directory: `mongodb_directory` (default `<docker_home>/mongodb`)
* Credentials: `mongodb_user` and `mongodb_password`. The role ships a placeholder password: set your own in your inventory.
* Image: `mongodb/mongodb-community-server`, version `mongodb_image_version` (default `8.2-ubuntu2204`)
* Log level: `mongodb_log_level` (default `error`)
* Memory limit: `mongodb_memory` (default `1g`)
* Container name: `mongodb_container_name` (default `mongodb`)

Available externally through Traefik only if `mongodb_available_externally: true`.

Keep the image version pinned: on-disk data (featureCompatibilityVersion) cannot jump major versions, so an unpinned `latest` can break startup.

**For more info visit: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)**
