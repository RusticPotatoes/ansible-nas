# nzbget

Runs NZBGet, a Usenet downloader, in a container.

Port: the web UI on `6789` (`nzbget_port`). When `vpn_download_stack_enabled` is true, NZBGet
runs in gluetun's network and the port is published by the `gluetun` role instead.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it does |
| --- | --- | --- |
| `nzbget_enabled` | `false` | Start NZBGet; `false` removes the container. |
| `nzbget_available_externally` | `false` | Route `nzbget_hostname` through Traefik. |
| `nzbget_data_directory` | `"{{ docker_home }}/nzbget"` | Config, mounted at `/config`. |
| `nzbget_download_directory` | `"{{ downloads_root }}"` | Downloads, mounted at `/downloads`. |
| `nzbget_user_id` | `"0"` | UID the app runs as (`PUID`). |
| `nzbget_group_id` | `"0"` | GID the app runs as (`PGID`). |
| `nzbget_port` | `"6789"` | Host port of the web UI. |
| `nzbget_hostname` | `"nzbget"` | Traefik hostname, under `ansible_nas_domain`. |
| `nzbget_container_name` | `"nzbget"` | Container name. |
| `nzbget_image_name` | `"linuxserver/nzbget"` | Image. |
| `nzbget_image_version` | `"latest"` | Image tag. |
| `nzbget_memory` | `"1g"` | Memory limit. |

The Homepage widget reads `nzbget_user` and `nzbget_pass` (default empty). Set them in your own
vars, never in git, and change NZBGet's own login after the first start.

Application page: `website/docs/applications/download-tools/nzbget.md`.

Tests: a molecule scenario in `molecule/`.
