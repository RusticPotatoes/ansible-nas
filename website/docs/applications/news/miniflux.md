# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070), the admin username is `admin` (`miniflux_admin_username`); the password is the one set as `vault_miniflux_admin_password` in `vault.yml`.

## Specific Configuration

An admin user will be created with the username and password of `miniflux_admin_username` and `miniflux_admin_password` respectively. The password comes from `vault_miniflux_admin_password`, and the PostgreSQL password from `vault_miniflux_db_password` (`miniflux_db_password`). Set both in `vault.yml` before enabling Miniflux; neither has a default. PostgreSQL applies its password only when its data folder is first created: on an existing install, `vault_miniflux_db_password` must match the password already in the database.
