# tiddlywiki

Runs TiddlyWiki, a non-linear notebook for capturing, organizing and sharing information, as a server in a container.

Web interface: port `8092` (`tiddlywiki_port`), published to the container's port 8080.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `tiddlywiki_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `tiddlywiki_available_externally` | `false` | Lets Traefik route `tiddlywiki_hostname`.`ansible_nas_domain` to it. |
| `tiddlywiki_data_directory` | `"{{ docker_home }}/tiddlywiki"` | The wiki's data, mounted at `/var/lib/tiddlywiki`. |
| `tiddlywiki_port` | `8092` | Host port published to the container's port 8080. |
| `tiddlywiki_hostname` | `tiddlywiki` | Subdomain Traefik uses when it is available externally. |
| `tiddlywiki_memory` | `512MB` | Container memory limit. |
| `tiddlywiki_container_name` | `"tiddlywiki"` | Name of the Docker container. |
| `tiddlywiki_image_name` | `"wmudge/tiddlywiki"` | Docker image. |
| `tiddlywiki_image_version` | `"latest"` | Image tag. |

The tasks also read four optional variables that have no default here (they are commented out in `defaults/main.yml`) and are left out when unset: `tiddlywiki_username` and `tiddlywiki_password` (basic auth; set them in your own vars, never in git), `tiddlywiki_node_memory` (`NODE_MEM`) and `tiddlywiki_debug_level` (`DEBUG`).

Application page: `website/docs/applications/content-management/tiddlywiki.md`.

Tests: a molecule scenario in `molecule/`.
