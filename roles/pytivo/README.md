# pytivo

Runs pyTivo, an HMO and GoBack server that streams many video formats to a TiVo, in a container. The media folders are mounted read-only.

Ports: `9032` (web) and `2190`/udp, written in the tasks; there is no port variable.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `pytivo_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `pytivo_available_externally` | `false` | Lets Traefik route `pytivo_hostname`.`ansible_nas_domain` to it. |
| `pytivo_config_directory` | `"{{ docker_home }}/pytivo/config"` | pyTivo's configuration, mounted at `/config`. |
| `pytivo_movies_directory` | `"{{ movies_root }}"` | Movies, mounted read-only at `/movies`. |
| `pytivo_tv_directory` | `"{{ tv_root }}"` | TV, mounted read-only at `/tv`. |
| `pytivo_photos_directory` | `"{{ photos_root }}"` | Photos, mounted read-only at `/photos`. |
| `pytivo_music_directory` | `"{{ music_root }}"` | Music, mounted read-only at `/music`. |
| `pytivo_podcasts_directory` | `"{{ podcasts_root }}"` | Podcasts, mounted read-only at `/podcasts`. |
| `pytivo_user_id` | `"0"` | User the container runs as (`PUID`). |
| `pytivo_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `pytivo_hostname` | `"pytivo"` | Subdomain Traefik uses when it is available externally. |
| `pytivo_container_name` | `"pytivo"` | Name of the Docker container. |
| `pytivo_image_name` | `"pinion/docker-pytivo"` | Docker image. |
| `pytivo_image_version` | `"latest"` | Image tag. |

The container's memory limit is `1g`, set in the tasks.

Application page: `website/docs/applications/media-serving/pytivo.md`.

Tests: a molecule scenario in `molecule/`.
