# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070). The admin user's username is `miniflux_admin_username` (default `admin`).

## Specific Configuration

An admin user will be created with the username `miniflux_admin_username` and the password `miniflux_admin_password`. Both secrets are taken from your **vault** (never in a tracked file: this repository may be public):

```yaml
vault_miniflux_admin_password: "<the admin password>"
vault_miniflux_db_password: "<the Postgres password for the miniflux database>"
```

With either one empty the play stops before Miniflux starts, and says which to set.
