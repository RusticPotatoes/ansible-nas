---
title: "Minio"
---

Homepage: [https://min.io/](https://min.io/)

Docker Container: [Minio](https://hub.docker.com/r/minio/minio)

MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service. Use MinIO to build high performance infrastructure for machine learning, analytics and application data workloads.

## Usage

Set `minio_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Minio web interface can be found at [http://ansible_nas_host_or_ip:9009](http://ansible_nas_host_or_ip:9009).

## Root credentials

The root password has no default, so the role stops with a clear message if it is not set.
Keep it in your Ansible vault rather than in plain group vars:

1. Open your vault: `ansible-vault edit <your vault file>`.
2. Add the password (at least 8 characters), for example:

   ```yaml
   vault_minio_admin_password: "<a long random password>"
   ```

3. Run the playbook as usual (`--tags minio` to apply just this role).

The role reads `minio_admin_password` from `vault_minio_admin_password`. The root user is
`minio_admin_username` (default `admin`), which can be overridden the same way with
`vault_minio_admin_username`.

MinIO reads its root credentials from the environment at every start. If you already run MinIO,
put the password it uses today in the vault to keep everything as it is; changing it later
changes the root login, and any client using the root credentials must be updated too.
