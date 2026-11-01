# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070), the admin username is `admin` and its password is set by `vault_miniflux_admin_password` in your vault (see below).

## Specific Configuration

An admin user will be created with the username and password of `miniflux_admin_username` and `miniflux_admin_password` respectively. Set `vault_miniflux_admin_password` and `vault_miniflux_db_password` in your vault; the role refuses to run while either is empty. A database keeps its first password (see the PostgreSQL note in AGENTS.md): on an existing Miniflux database, `vault_miniflux_db_password` must match the password already set inside it.
