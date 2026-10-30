# krusader

Runs Krusader, a twin-panel file manager, in a privileged container, reachable from a browser (noVNC) and by VNC.

Ports: web interface `6080` (`krusader_port_http`) and VNC `5900` (`krusader_port_vnc`), each published to the same container port.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `krusader_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `krusader_available_externally` | `"false"` | Lets Traefik route `krusader_hostname`.`ansible_nas_domain` to it (passed as a string). |
| `krusader_user_id` | `"0"` | User the container runs as (`PUID`). |
| `krusader_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `krusader_config_directory` | `"{{ docker_home }}/krusader/config"` | Krusader's configuration, mounted at `/config`. |
| `krusader_browse_directory` | `"/"` | Host folder Krusader can browse, mounted at `/mnt/fs`. The default is the whole file system. |
| `krusader_port_http` | `"6080"` | Host port published to the container's port 6080 (web interface). |
| `krusader_port_vnc` | `"5900"` | Host port published to the container's port 5900 (VNC). |
| `krusader_hostname` | `"krusader"` | Subdomain Traefik uses when it is available externally. |
| `krusader_container_name` | `"krusader"` | Name of the Docker container. |
| `krusader_image_name` | `"binhex/arch-krusader"` | Docker image. |
| `krusader_image_version` | `"latest"` | Image tag. |
| `krusader_memory` | `1g` | Container memory limit. |
| `krusader_umask` | `"000"` | File creation mask (`UMASK`). |
| `krusader_webpage_title` | `"Tower"` | Title of the web page (`WEBPAGE_TITLE`). |
| `krusader_temp_folder` | `"/config/krusader/tmp"` | Temporary folder inside the container (`TEMP_FOLDER`). |
| `krusader_vnc_password` | `"topsecret"` | VNC password (`VNC_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |

Application page: `website/docs/applications/system-tools/krusader.md`.

Tests: a molecule scenario in `molecule/`.
