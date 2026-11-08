# gitlab

Runs GitLab Community Edition, a Git repository service with code review and analytics, in a container. It needs much more memory than Gitea.

Ports: web interface `4080` (`gitlab_port_http`, container port 80), HTTPS `4443` (`gitlab_port_https`, container port 443) and Git over SSH `422` (`gitlab_port_ssh`, container port 22).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `gitlab_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `gitlab_available_externally` | `false` | Lets Traefik route `gitlab_hostname`.`ansible_nas_domain` to it. |
| `gitlab_data_directory` | `"{{ docker_home }}/gitlab"` | Holds `config/` (`/etc/gitlab`), `log/` (`/var/log/gitlab`) and `data/` (`/var/opt/gitlab`). |
| `gitlab_hostname` | `"gitlab"` | Subdomain Traefik uses when it is available externally; also the container's hostname under `ansible_nas_domain`. |
| `gitlab_port_http` | `"4080"` | Host port published to the container's port 80. |
| `gitlab_port_https` | `"4443"` | Host port published to the container's port 443. |
| `gitlab_port_ssh` | `"422"` | Host port published to the container's port 22. |
| `gitlab_container_name` | `"gitlab"` | Name of the Docker container. |
| `gitlab_image_name` | `"gitlab/gitlab-ce"` | Docker image. |
| `gitlab_image_version` | `"latest"` | Image tag. |
| `gitlab_user_id` | `"1000"` | User the container runs as (`PUID`). |
| `gitlab_group_id` | `"1000"` | Group the container runs as (`PGID`). |
| `gitlab_memory` | `"4g"` | Container memory limit. |

The tasks create a `gitlab` user and group (uid and gid 998, matching `git:git` in the image) that own the data folders. On first start GitLab asks for the password of its `root` administrator account.

Application page: `website/docs/applications/development-tools/gitlab.md`.

Tests: a molecule scenario in `molecule/`.
