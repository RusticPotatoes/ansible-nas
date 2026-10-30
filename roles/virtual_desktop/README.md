# virtual_desktop

Runs a cut-down Ubuntu MATE desktop in a container, reached over RDP, from RattyDAVE's `docker-ubuntu-xrdp-mate-custom` image.

RDP: port `3389` (`virtual_desktop_rdp_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `virtual_desktop_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `virtual_desktop_users` | see below | Desktop users, each with `username`, `password` and `sudo`, written to `users.txt` and mounted at `/root/createusers.txt`. The default password is a placeholder: set your own users in your vars, never in git. |
| `virtual_desktop_user_id` | `"0"` | User ID. Not used by the tasks yet. |
| `virtual_desktop_group_id` | `"0"` | Group ID. Not used by the tasks yet. |
| `virtual_desktop_data_directory` | `"{{ docker_home }}/virtual_desktop"` | Holds `users.txt` and the users' `home` folder, mounted at `/home`. |
| `virtual_desktop_rdp_port` | `3389` | Host port published to the container's RDP port 3389. |
| `virtual_desktop_memory` | `2g` | Container memory limit. |
| `virtual_desktop_container_name` | `"virtual_desktop"` | Name of the Docker container. |
| `virtual_desktop_image_name` | `"rattydave/docker-ubuntu-xrdp-mate-custom"` | Docker image. |
| `virtual_desktop_image_version` | `"20.04-tools"` | Image tag. |

Default of `virtual_desktop_users`:

```yaml
virtual_desktop_users:
  - username: "{{ ansible_nas_user }}"
    password: "topsecret"
    sudo: "Y"
```

The container runs privileged, and mounts `samba_shares_root` at `/samba`, `docker_home` at `/docker` and the host's `/etc/timezone`. It has no Traefik labels. The docs page names the users variable `vd_users`; the role reads `virtual_desktop_users`.

Application page: `website/docs/applications/other/virtual_desktop.md`.

Tests: a molecule scenario in `molecule/`.
