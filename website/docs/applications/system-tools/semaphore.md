---
title: "Semaphore"
---

Homepage: [https://semaphoreui.com/](https://semaphoreui.com/)

Docker image: [https://hub.docker.com/r/semaphoreui/semaphore](https://hub.docker.com/r/semaphoreui/semaphore)

Semaphore UI is a web interface for running Ansible playbooks, Terraform/OpenTofu and shell scripts against your inventories.

## Usage

Set `semaphore_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file. Semaphore stores its data in the shared PostgreSQL container, so `postgres_enabled: true` is required too. Semaphore creates its `semaphore` database on first start.

Set the admin password with `semaphore_admin_password` (ideally from a vault). The admin account is only created on first start.

Semaphore's web interface can be found at [http://ansible_nas_host_or_ip:3333](http://ansible_nas_host_or_ip:3333)

## Specific Configuration

The container runs as uid `1001`, gid `0` (`semaphore_user_id` / `semaphore_group_id`); the role creates the host directories with that owner.

Two host directories are mounted and must be kept (and backed up) together with the PostgreSQL data:

- `semaphore_config_directory` (default `{{ docker_home }}/semaphore/config`) at `/etc/semaphore`. It holds `config.json`, including the `access_key_encryption` secret that encrypts the SSH keys and passwords stored in the database. If this file is lost, a recreated container generates new secrets and the stored keys can no longer be decrypted.
- `semaphore_data_directory` (default `{{ docker_home }}/semaphore/data`) at `/var/lib/semaphore`.

Current Semaphore releases no longer run on BoltDB. To bring data over from an old `database.boltdb`, see the `SEMAPHORE_MIGRATE_FROM_BOLTDB` option in the Semaphore documentation (it only migrates into SQLite).

The image is pinned with `semaphore_image_version`; bump it deliberately rather than tracking `latest`.
