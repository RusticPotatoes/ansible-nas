# apcupsd

Runs apcupsd, a daemon that monitors a connected APC UPS and can shut the host down cleanly in a power outage, in a privileged container.

Network information server: port `3551` (`apcupsd_port`), for collecting UPS events and data.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `apcupsd_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `apcupsd_data_directory` | `"{{ docker_home }}/apcupsd"` | Holds `apcupsd.conf`, templated on the first run only and mounted at `/etc/apcupsd/apcupsd.conf`. |
| `apcupsd_port` | `"3551"` | Host port published to the container's port 3551. |
| `apcupsd_memory` | `1g` | Container memory limit. |
| `apcupsd_container_name` | `apcupsd` | Name of the Docker container. |
| `apcupsd_onbatterydelay` | `6` | `ONBATTERYDELAY`: seconds from a detected power failure until the onbattery event. |
| `apcupsd_batterylevel` | `5` | `BATTERYLEVEL`: shut down when the battery percentage falls to this or below. |
| `apcupsd_minutes` | `5` | `MINUTES`: shut down when the remaining runtime in minutes falls to this or below. |
| `apcupsd_timeout` | `0` | `TIMEOUT`: shut down after this many seconds on battery; `0` disables the timer. |
| `apcupsd_annoy` | `300` | `ANNOY`: seconds between warnings to log off before shutdown; `0` disables. |
| `apcupsd_annoydelay` | `60` | `ANNOYDELAY`: delay after a power failure before the first warning. |
| `apcupsd_nologon` | `"disable"` | `NOLOGON`: when logins are refused during a power failure (`disable`, `timeout`, `percent`, `minutes` or `always`). |
| `apcupsd_killdelay` | `0` | `KILLDELAY`: if non-zero, seconds after a shutdown request before apcupsd tries to cut the UPS power. |

Set `apcupsd_device` (no default here) to the UPS device path, for example `/dev/usb/hiddev0`; the tasks pass it into the container. The config file is written only when it does not exist yet, so later changes to these variables need the file removed first. The image is `gregewing/apcupsd` (tag `latest`), set in the tasks rather than in defaults.

Application page: `website/docs/applications/system-tools/apcupsd.md`.

Tests: a molecule scenario in `molecule/`.
