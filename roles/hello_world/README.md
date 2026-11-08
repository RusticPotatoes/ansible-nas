# hello_world

Runs a minimal "hello world" web page in a container. It is the template role a new application starts from.

Web interface: port `9999` (`hello_world_port`), published to the container's port 8000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `hello_world_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `hello_world_available_externally` | `false` | Lets Traefik route `hello_world_hostname`.`ansible_nas_domain` to it. |
| `hello_world_data_directory` | `"{{ docker_home }}/hello_world"` | Data folder, mounted at `/hello_world`. |
| `hello_world_port` | `"9999"` | Host port published to the container's port 8000. |
| `hello_world_hostname` | `"hello_world"` | Subdomain Traefik uses when it is available externally. |
| `hello_world_memory` | `1g` | Container memory limit. |
| `hello_world_container_name` | `hello_world` | Name of the Docker container. |

The image is `crccheck/hello-world`, set in the tasks rather than in defaults. `docs/hello_world.md` is the template for a new application's documentation page.

Application page: `website/docs/applications/other/hello_world.md`.

Tests: a molecule scenario in `molecule/`.
