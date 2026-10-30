# emby

Runs Emby, a media server that clients on computers, phones and smart TVs connect to, in a container.

Ports: HTTP on `8096` (`emby_port_http`) and HTTPS on `8920` (`emby_port_https`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `emby_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `emby_available_externally` | `false` | Lets Traefik route `emby_hostname`.`ansible_nas_domain` to it. |
| `emby_config_directory` | `"{{ docker_home }}/emby/config"` | Emby's configuration, mounted at `/config`. |
| `emby_movies_directory` | `"{{ movies_root }}"` | Movie library, mounted at `/movies`. |
| `emby_tv_directory` | `"{{ tv_root }}"` | TV library, mounted at `/tv`. |
| `emby_movies_permissions` | `"rw"` | Mount mode of the movie library; `ro` stops Emby from ever deleting files. |
| `emby_tv_permissions` | `"rw"` | Mount mode of the TV library; `ro` stops Emby from ever deleting files. |
| `emby_user_id` | `"0"` | User the container runs as (`PUID`). |
| `emby_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `emby_port_http` | `"8096"` | Host port published to the container's port 8096. |
| `emby_port_https` | `"8920"` | Host port published to the container's port 8920. |
| `emby_hostname` | `"emby"` | Subdomain Traefik uses when it is available externally. |
| `emby_memory` | `1g` | Container memory limit. |
| `emby_container_name` | `emby` | Name of the Docker container. |
| `emby_image` | `emby/embyserver` | Docker image. |
| `emby_image_tag` | `beta` | Image tag. |

Optional `emby_devices` (no default here) maps devices into the container, for example `/dev/dri:/dev/dri` for hardware transcoding.

Application page: `website/docs/applications/media-serving/emby.md`.

Tests: a molecule scenario in `molecule/`.
