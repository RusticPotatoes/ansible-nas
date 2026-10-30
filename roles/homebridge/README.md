# homebridge

Runs Homebridge, a NodeJS server that emulates the iOS HomeKit API and bridges HomeKit to other smart-home devices through plugins, in a container with its config UI.

Web interface: port `8087` (`homebridge_port`). The container uses the host's network; the port is passed as `HOMEBRIDGE_CONFIG_UI_PORT`.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `homebridge_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `homebridge_available_externally` | `false` | Lets Traefik route `homebridge_hostname`.`ansible_nas_domain` to it. |
| `homebridge_config_directory` | `"{{ docker_home }}/homebridge/config"` | Homebridge's configuration, mounted at `/homebridge`. |
| `homebridge_user_id` | `"0"` | User the container runs as (`PUID`). |
| `homebridge_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `homebridge_hostname` | `"homebridge"` | Subdomain Traefik uses when it is available externally. |
| `homebridge_port` | `"8087"` | Port of the config UI (`HOMEBRIDGE_CONFIG_UI_PORT`) on the host's network. |
| `homebridge_container_name` | `"homebridge"` | Name of the Docker container. |
| `homebridge_image_name` | `"oznu/homebridge"` | Docker image. |
| `homebridge_image_version` | `"latest"` | Image tag. |
| `homebridge_memory` | `"1g"` | Container memory limit. |

The config UI's stock login is `admin` / `admin`; change it after the first login.

Application page: `website/docs/applications/home-automation/homebridge.md`.

Tests: a molecule scenario in `molecule/`.
