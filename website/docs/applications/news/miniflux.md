# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070), the username is `admin` and the password is the one set in `vault_miniflux_admin_password`.

## Specific Configuration

An admin user will be created with the username of `miniflux_admin_username` and the password of `miniflux_admin_password`, which reads `vault_miniflux_admin_password` from the vault. The database password (`miniflux_db_password`) reads `vault_miniflux_db_password`. Both must be set in the vault before enabling Miniflux; the role stops with a message if either is empty.

PostgreSQL takes its password only when its data folder is first created. On an existing install, change the password inside the database (`ALTER USER miniflux PASSWORD '...';`) to match `vault_miniflux_db_password` before running the playbook.
