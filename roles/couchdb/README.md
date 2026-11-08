# couchdb

Runs Apache CouchDB, a document-oriented NoSQL database with an HTTP API and the Fauxton web interface, in a container.

API and web interface: port `5984` (`couchdb_port`); Fauxton is at `/_utils`.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `couchdb_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `couchdb_available_externally` | `false` | Lets Traefik route `couchdb_hostname`.`ansible_nas_domain` to it. |
| `couchdb_data_directory` | `"{{ docker_home }}/couchdb"` | CouchDB's folder: `config` is mounted at `/opt/couchdb/etc/local.d` and `data` at `/opt/couchdb/data`. |
| `couchdb_admin_user` | `"admin"` | `COUCHDB_USER`, the admin account. |
| `couchdb_admin_password` | `"changeme"` | `COUCHDB_PASSWORD`. The default is a placeholder: set it in your own vars, never in git. |
| `couchdb_hostname` | `"couchdb"` | Subdomain Traefik uses when it is available externally. |
| `couchdb_port` | `"5984"` | Host port published to the container's port 5984. |
| `couchdb_memory` | `1024MB` | Container memory limit. |
| `couchdb_container_name` | `"couchdb"` | Name of the Docker container. |
| `couchdb_image_name` | `"couchdb"` | Docker image. |
| `couchdb_image_version` | `"latest"` | Image tag. |

Application page: `website/docs/applications/other/couchdb.md`.

Tests: a molecule scenario in `molecule/`.
