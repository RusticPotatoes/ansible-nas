# timemachine

Runs a Samba share for Time Machine, the backup application of the Mac, in a container. It also installs Avahi on the NAS itself, with a service file that lets Macs on the local network discover the share.

SMB: port `10445` (`timemachine_port`), published to the container's port 445 and announced by Avahi.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `timemachine_enabled` | `false` | Starts the container and sets up Avahi when `true`; removes the container when `false`. |
| `timemachine_volume_size_limit` | `"0"` | Most space Time Machine may use, in MiB (`TMSIZE`); `0` for no limit. |
| `timemachine_password` | `timemachine` | Password of the share (`PASS`). The default is a placeholder: set your own in your vars, never in git. |
| `timemachine_share_name` | `Data` | Name of the share as Time Machine shows it (`SHARENAME`), also announced by Avahi. |
| `timemachine_log_level` | `error` | Log level. Not used by the tasks yet. |
| `timemachine_data_directory` | `"{{ docker_home }}/timemachine"` | Base folder; its `data` subfolder holds the backups, mounted at `/backups`. |
| `timemachine_port` | `"10445"` | Host port published to the container's port 445. |
| `timemachine_memory` | `1g` | Container memory limit. |
| `timemachine_container_name` | `"timemachine"` | Name of the Docker container. |
| `timemachine_image_name` | `"awlnx/samba-timemachine"` | Docker image. |
| `timemachine_image_version` | `"latest"` | Image tag. |

The role writes `/etc/avahi/services/timemachine.service` on the NAS and reloads Avahi when it changes; turning the role off removes only the container.

Application page: `website/docs/applications/system-tools/timemachine.md`.

Tests: a molecule scenario in `molecule/`.
