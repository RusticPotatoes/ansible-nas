# syncthing

Runs Syncthing, a continuous file synchronization program that keeps files in step between two or more computers, in a container.

Web interface: port `8384` (`syncthing_port`). The tasks also publish Syncthing's fixed sync and discovery ports: `22000` (TCP and UDP) and `21027` (UDP).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `syncthing_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `syncthing_available_externally` | `false` | Lets Traefik route `syncthing_hostname`.`ansible_nas_domain` to it. |
| `syncthing_data_directory` | `"{{ samba_shares_root }}/syncthing"` | Syncthing's folder, created by the role and mounted by the default `syncthing_volumes`. |
| `syncthing_volumes` | see below | The mounts of the container, as `host:container` strings. Add the NAS folders you want to sync here, under `/var/syncthing/`. |
| `syncthing_user_id` | `"0"` | User the container runs as (`PUID`). |
| `syncthing_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `syncthing_port` | `8384` | Host port published to the container's port 8384. |
| `syncthing_hostname` | `syncthing` | Subdomain Traefik uses when it is available externally. |
| `syncthing_container_name` | `"syncthing"` | Name of the Docker container. |
| `syncthing_image_name` | `"syncthing/syncthing"` | Docker image. |
| `syncthing_image_version` | `"latest"` | Image tag. |
| `syncthing_memory` | `1g` | Container memory limit. |

Default of `syncthing_volumes`:

```yaml
syncthing_volumes:
  - "{{ syncthing_data_directory }}:/var/syncthing/"
```

Application page: `website/docs/applications/system-tools/syncthing.md`.

Tests: a molecule scenario in `molecule/`.
