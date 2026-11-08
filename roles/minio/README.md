# minio

Runs an S3-compatible object store in a container: Silo (`pgsty/silo`), a maintained fork of MinIO with the same S3 API, environment variables and on-disk format, since MinIO no longer publishes images. Loki stores its logs here.

Ports: S3 API `9001` (`minio_api_port`, container port 9000) and web console `9009` (`minio_console_port`, the same port in the container).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `minio_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `minio_available_externally` | `false` | Lets Traefik route `minio_hostname`.`ansible_nas_domain` to it. |
| `minio_data_directory` | `"{{ docker_home }}/minio"` | Holds `data/`, mounted at `/data`. |
| `minio_admin_username` | `admin` | Root user (`MINIO_ROOT_USER`). |
| `minio_admin_password` | `supersecure` | Root password (`MINIO_ROOT_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `minio_hostname` | `"minio"` | Subdomain Traefik uses when it is available externally. |
| `minio_network_name` | `"minio"` | Name kept for a MinIO network; the tasks do not use it. |
| `minio_api_port` | `"9001"` | Host port published to the container's port 9000. |
| `minio_console_port` | `"9009"` | Port of the web console, published to the same port in the container. |
| `minio_container_name` | `"minio"` | Name of the Docker container. |
| `minio_image_name` | `"pgsty/silo"` | Docker image. |
| `minio_image_version` | `"RELEASE.2026-09-16T00-00-00Z"` | Image tag. |
| `minio_memory` | `"1g"` | Container memory limit. |

Prometheus metrics are public (`MINIO_PROMETHEUS_AUTH_TYPE`).

Application page: `website/docs/applications/system-tools/minio.md`.

Tests: a molecule scenario in `molecule/`.
