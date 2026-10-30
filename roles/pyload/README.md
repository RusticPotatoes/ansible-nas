# pyload

Runs pyLoad, a lightweight download manager written in Python and managed from the web, in a container.

Web interface: port `8000` (`pyload_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `pyload_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `pyload_available_externally` | `false` | Lets Traefik route `pyload_hostname`.`ansible_nas_domain` to it. |
| `pyload_config_directory` | `"{{ docker_home }}/pyload"` | pyLoad's configuration, mounted at `/opt/pyload/pyload-config`. |
| `pyload_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/opt/pyload/Downloads`. |
| `pyload_user_id` | `"0"` | User ID the container runs as (`UID`). |
| `pyload_group_id` | `"0"` | Group ID the container runs as (`GID`). |
| `pyload_hostname` | `"pyload"` | Subdomain Traefik uses when it is available externally. |
| `pyload_port` | `"8000"` | Host port published to the container's port 8000. |
| `pyload_container_name` | `"pyload"` | Name of the Docker container. |
| `pyload_image_name` | `"writl/pyload"` | Docker image. |
| `pyload_image_version` | `"latest"` | Image tag. |
| `pyload_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/download-tools/pyload.md`.

Tests: a molecule scenario in `molecule/`.
