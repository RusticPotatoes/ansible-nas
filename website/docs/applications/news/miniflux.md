# Miniflux

Homepage: [https://miniflux.app/](https://miniflux.app/)

Miniflux is a minimalist and opinionated feed reader.

## Usage

Set `miniflux_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Miniflux web interface can be found at [http://ansible_nas_host_or_ip:8070](http://ansible_nas_host_or_ip:8070), the username is `admin` and the password is the value of `vault_miniflux_admin_password`.

## Specific Configuration

An admin user will be created with the username `miniflux_admin_username` and the password `miniflux_admin_password`. Set `vault_miniflux_admin_password` and `vault_miniflux_db_password` in your vault (never in a tracked file: this repository may be public). The role stops if either is empty.

The database password `miniflux_db_password` is applied only when the Postgres data folder is first created. On an existing install, change the password inside the database first (`ALTER USER miniflux PASSWORD '...';`), then set the vault value to match. Use letters and digits only in `vault_miniflux_db_password`: it is put into the database URL, and a `/` in it is not encoded.
