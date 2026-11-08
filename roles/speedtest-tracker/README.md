# speedtest-tracker

Runs Speedtest-Tracker, which continuously tracks your internet speed, in a container.

Web interface: port `8765` (`speedtest_tracker_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `speedtest_tracker_enabled` | `false` | Meant to switch the role on, but the tasks test `speedtest_enabled` instead (see below). |
| `speedtest_tracker_available_externally` | `false` | Lets Traefik route `speedtest_tracker_hostname`.`ansible_nas_domain` to it. |
| `speedtest_data_directory` | `"{{ docker_home }}/speedtest_tracker"` | Base folder; its `config` subfolder is mounted at `/config`. |
| `speedtest_tracker_user_id` | `"0"` | User ID. Not used by the tasks yet. |
| `speedtest_tracker_group_id` | `"0"` | Group ID. Not used by the tasks yet. |
| `speedtest_tracker_port` | `"8765"` | Host port published to the container's port 80. |
| `speedtest_tracker_hostname` | `"speedtest-tracker"` | Subdomain Traefik uses when it is available externally. |
| `speedtest_container_name` | `"speedtest-tracker"` | Name of the Docker container. |
| `speedtest_image_name` | `"henrywhitaker3/speedtest-tracker"` | Docker image. |
| `speedtest_image_version` | `"latest"` | Image tag. |
| `speedtest_tracker_memory` | `1g` | Memory limit. Not used by the tasks: they set `1g` directly. |

The tasks start or stop the container on `speedtest_enabled`, which has no default here; the docs page names `speedtest_tracker_enabled`. Set `speedtest_enabled` to use the role. The container is removed and recreated on every run, and accepts the Ookla EULA (`OOKLA_EULA_GDPR`).

Application page: `website/docs/applications/monitoring/speedtest.md`.

Tests: a molecule scenario in `molecule/`.
