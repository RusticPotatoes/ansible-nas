# mongodb

Runs MongoDB Community Server, a document-oriented NoSQL database, in a container. Other roles (UniFi, LibreChat) use it.

Port `27017` (`mongodb_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mongodb_enabled` | `false` | Starts the container when `true`. The role has no stop task: `false` leaves a running container as it is. |
| `mongodb_available_externally` | `false` | Kept for outside access; the tasks set no Traefik labels, so it has no effect. |
| `mongodb_directory` | `"{{ docker_home }}/mongodb"` | Database files, mounted at `/data/db`. |
| `mongodb_user_id` | `"0"` | User the container runs as (`user:`). |
| `mongodb_group_id` | `"0"` | Group the container runs as (`user:`). |
| `mongodb_log_level` | `"error"` | Log level. Not used by the tasks. |
| `mongodb_user` | `"admin"` | Root user created on first start (`MONGODB_INITDB_ROOT_USERNAME`). |
| `mongodb_password` | `"strongpassword123"` | Root password (`MONGODB_INITDB_ROOT_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `mongodb_port` | `"27017"` | Host port published to the container's port 27017. |
| `mongodb_hostname` | `"mongodb"` | Hostname kept for a Traefik route; not used by the tasks. |
| `mongodb_timezone` | `"{{ ansible_nas_timezone }}"` | Container time zone (`TZ`). |
| `mongodb_memory` | `1g` | Memory limit. Not used by the tasks: the container has no limit. |
| `mongodb_container_name` | `mongodb` | Container name. Not used by the tasks, which name the container `mongodb` directly. |
| `mongodb_image_name` | `"mongodb/mongodb-community-server"` | Docker image. |
| `mongodb_image_version` | `"8.2-ubuntu2204"` | Image tag. Pinned to a major and minor version: the on-disk data cannot jump major versions, so an unpinned `latest` can break startup. |

MongoDB takes `mongodb_user` and `mongodb_password` only when its data folder is empty; changing them later does not change the database, and roles that read them stop being able to log in (see `AGENTS.md`).

Application page: `website/docs/applications/system-tools/mongodb.md`.

Tests: a molecule scenario in `molecule/`.
