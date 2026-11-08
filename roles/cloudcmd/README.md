# cloudcmd

Runs Cloud Commander, a web file manager with a command-line console and a text editor, in a container.

Web interface: port `7373` (`cloudcmd_port`), published to the container's port 8000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `cloudcmd_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `cloudcmd_available_externally` | `false` | Lets Traefik route `cloudcmd_hostname`.`ansible_nas_domain` to it. |
| `cloudcmd_data_directory` | `"{{ docker_home }}/cloudcmd/config"` | Cloud Commander's configuration, mounted at `/config`. |
| `cloudcmd_browse_directory` | `"/"` | Folder on the host you can browse, mounted at `/mnt/fs`. By default the whole filesystem. |
| `cloudcmd_user_id` | `"0"` | User the container runs as (`PUID`). |
| `cloudcmd_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `cloudcmd_hostname` | `"cloudcmd"` | Subdomain Traefik uses when it is available externally. |
| `cloudcmd_port` | `"7373"` | Host port published to the container's port 8000. |
| `cloudcmd_memory` | `"1g"` | Container memory limit. |
| `cloudcmd_container_name` | `cloudcmd` | Name of the Docker container. |

The image is `coderaiser/cloudcmd` (tag `latest`), set in the tasks rather than in defaults. If you make it available externally, set up authorisation inside the app first (F10 from the main menu).

Application page: `website/docs/applications/system-tools/cloudcmd.md`.

Tests: a molecule scenario in `molecule/`.
