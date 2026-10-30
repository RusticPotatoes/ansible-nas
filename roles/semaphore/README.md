# semaphore

Runs Semaphore UI, a web interface for running Ansible playbooks, Terraform/OpenTofu and shell scripts against your inventories, in a container. It keeps its data in the shared PostgreSQL container.

Web interface: port `3333` (`semaphore_port`), published to the container's port 3000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `semaphore_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `semaphore_available_externally` | `false` | Lets Traefik route `semaphore_hostname`.`ansible_nas_domain` to it. |
| `semaphore_config_directory` | `"{{ docker_home }}/semaphore/config"` | Holds `config.json`, including the secret that encrypts stored keys; mounted at `/etc/semaphore`. Keep and back it up with the PostgreSQL data. |
| `semaphore_data_directory` | `"{{ docker_home }}/semaphore/data"` | Local data, mounted at `/var/lib/semaphore`. |
| `semaphore_user_id` | `"1001"` | User the container runs as, and owner of its folders. |
| `semaphore_group_id` | `"0"` | Group the container runs as, and group of its folders. |
| `semaphore_port` | `"3333"` | Host port published to the container's port 3000. |
| `semaphore_hostname` | `"semaphore"` | Subdomain Traefik uses when it is available externally. |
| `semaphore_container_name` | `"semaphore"` | Name of the Docker container. |
| `semaphore_image_name` | `"semaphoreui/semaphore"` | Docker image. |
| `semaphore_image_version` | `"v2.19.16"` | Image tag. |
| `semaphore_memory` | `1g` | Container memory limit. |
| `semaphore_admin_user` | `"{{ vault_semaphore_admin_user \| default('admin') }}"` | Admin account name (`SEMAPHORE_ADMIN`), created on first start only. |
| `semaphore_admin_password` | `"{{ vault_semaphore_admin_password \| default('') }}"` | Admin password (`SEMAPHORE_ADMIN_PASSWORD`). Set `vault_semaphore_admin_password` in your vault, never in git. |
| `semaphore_admin_email` | `"{{ vault_semaphore_admin_email \| default('admin@localhost') }}"` | Admin email (`SEMAPHORE_ADMIN_EMAIL`). |

Semaphore needs the `postgres` role (`postgres_enabled: true`): it joins the `postgres_net` network, logs in with `postgres_user` / `postgres_password`, and creates its `semaphore` database on first start. The image is pinned with `semaphore_image_version`; bump it deliberately.

Application page: `website/docs/applications/system-tools/semaphore.md`.

Tests: a molecule scenario in `molecule/`.
