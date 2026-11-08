# silverbullet

Runs SilverBullet, a note-taking application whose notes can be queried like a database, in a container.

Web interface: port `3002` (`silverbullet_port`), published to the container's port 3000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `silverbullet_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `silverbullet_available_externally` | `false` | Lets Traefik route `silverbullet_hostname`.`ansible_nas_domain` to it. |
| `silverbullet_data_directory` | `"{{ docker_home }}/silverbullet"` | The notes (the space), mounted at `/space`. |
| `silverbullet_port` | `3002` | Host port published to the container's port 3000. |
| `silverbullet_hostname` | `silverbullet` | Subdomain Traefik uses when it is available externally. |
| `silverbullet_container_name` | `"silverbullet"` | Name of the Docker container. |
| `silverbullet_image_name` | `"zefhemel/silverbullet"` | Docker image. |
| `silverbullet_image_version` | `"latest"` | Image tag. |
| `silverbullet_memory` | `1g` | Container memory limit. |
| `silverbullet_username` | `admin` | Login user name, passed in `SB_USER`. |
| `silverbullet_password` | `topSecret` | Login password, passed in `SB_USER`. The default is a placeholder: set your own in your vars, never in git. |

Application page: `website/docs/applications/other/silverbullet.md`.

Tests: a molecule scenario in `molecule/`.
