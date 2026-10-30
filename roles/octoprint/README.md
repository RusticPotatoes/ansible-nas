# octoprint

Runs OctoPrint, a web interface to control and monitor a 3D printer connected to the NAS by USB, in a container.

Web interface: port `8095` (`octoprint_port`), published to the container's port 80.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `octoprint_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `octoprint_available_externally` | `false` | Lets Traefik route `octoprint_hostname`.`ansible_nas_domain` to it. |
| `octoprint_data_directory` | `"{{ docker_home }}/octoprint"` | OctoPrint's data, mounted at `/octoprint`. |
| `octoprint_port` | `"8095"` | Host port published to the container's port 80. |
| `octoprint_hostname` | `"octoprint"` | Subdomain Traefik uses when it is available externally. |
| `octoprint_container_name` | `"octoprint"` | Name of the Docker container. |
| `octoprint_image_name` | `"octoprint/octoprint"` | Docker image. |
| `octoprint_image_version` | `"latest"` | Image tag. |
| `octoprint_printer_mountpoint` | `"/dev/ttyUSB0"` | Printer's serial device, passed to the container. |
| `octoprint_enable_webcam` | `false` | Passes the webcam device and turns on the MJPG streamer (`ENABLE_MJPG_STREAMER`). |
| `octoprint_webcam_mountpoint` | `"/dev/video0"` | Webcam device, passed when `octoprint_enable_webcam` is on (otherwise `/dev/null`). |
| `octoprint_memory` | `1g` | Container memory limit. |

Application page: `website/docs/applications/other/octoprint.md`.

Tests: a molecule scenario in `molecule/`.
