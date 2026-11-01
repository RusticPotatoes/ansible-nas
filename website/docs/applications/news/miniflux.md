# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070), the username is `miniflux_admin_username` (default `admin`) and the password is `vault_miniflux_admin_password` from your vault.yml.

## Specific Configuration

An admin user will be created with the username `miniflux_admin_username` and the password `miniflux_admin_password`, which is set from `vault_miniflux_admin_password` in vault.yml. The database password comes from `vault_miniflux_db_password` in vault.yml. Neither has a default: set both before deploying.
