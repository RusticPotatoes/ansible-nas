# ombi

Runs Ombi, a web app that lets your shared Plex or Emby users request content themselves, in a container.

Web interface: port `3579` (`ombi_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ombi_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `ombi_available_externally` | `false` | Lets Traefik route `ombi_hostname`.`ansible_nas_domain` to it. |
| `ombi_config_directory` | `"{{ docker_home }}/ombi/config"` | Ombi's configuration, mounted at `/config`. |
| `ombi_port` | `"3579"` | Host port published to the container's port 3579. |
| `ombi_hostname` | `"ombi"` | Subdomain Traefik uses when it is available externally. |
| `ombi_container_name` | `"ombi"` | Name of the Docker container. |
| `ombi_image_name` | `"linuxserver/ombi"` | Docker image. |
| `ombi_image_version` | `"latest"` | Image tag. |
| `ombi_user_id` | `"0"` | User the container runs as (`PUID`). |
| `ombi_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `ombi_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/download-tools/ombi.md`.

Tests: a molecule scenario in `molecule/`.
