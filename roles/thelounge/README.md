# thelounge

Runs The Lounge, a self-hosted web IRC client, in a container.

Web interface: port `9002` (`thelounge_port_two`), published to the container's port 9000. `thelounge_port_one` (`113`) is published to the container's port 9001.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `thelounge_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `thelounge_available_externally` | `false` | Lets Traefik route `thelounge_hostname`.`ansible_nas_domain` to it. |
| `thelounge_data_directory` | `"{{ docker_home }}/thelounge"` | The Lounge's data, mounted at `/var/opt/thelounge`. |
| `thelounge_port_one` | `"113"` | Host port published to the container's port 9001. |
| `thelounge_port_two` | `"9002"` | Host port published to the container's port 9000, the web interface. |
| `thelounge_hostname` | `thelounge` | Subdomain Traefik uses when it is available externally. |
| `thelounge_memory` | `1g` | Container memory limit. |
| `thelounge_container_name` | `"thelounge"` | Name of the Docker container. |
| `thelounge_image_name` | `"thelounge/thelounge"` | Docker image. |
| `thelounge_image_version` | `"latest"` | Image tag. |

The role copies an `admin` user into `users/admin.json` of the data folder. Its password is `admin`, as the docs page says: change it once you have logged in. The host's `/var/run/dbus` is mounted into the container.

Application page: `website/docs/applications/other/thelounge.md`.

Tests: a molecule scenario in `molecule/`.
