# mumble

Runs a Mumble server, a free, open source, low-latency voice chat application, in a container.

Port: `64738`, TCP (`mumble_tcp_port`) and UDP (`mumble_udp_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `mumble_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `mumble_available_externally` | `false` | Lets Traefik route `mumble_hostname`.`ansible_nas_domain` to it. |
| `mumble_data_directory` | `"{{ docker_home }}/mumble"` | Server data, mounted at `/data`. Created owned by 1000:1000, the image's user. |
| `mumble_tcp_port` | `"64738"` | Host TCP port published to the container's port 64738. |
| `mumble_udp_port` | `"64738"` | Host UDP port published to the container's port 64738. |
| `mumble_hostname` | `mumble` | Subdomain Traefik uses when it is available externally. |
| `mumble_server_password` | `"abcpassword123"` | Server password clients must give (`MUMBLE_CONFIG_SERVER_PASSWORD`). The default is a placeholder: set your own in your own vars, never in git. |
| `mumble_container_name` | `mumble-server` | Name of the Docker container. |

The image is `mumblevoip/mumble-server:latest`, set in the tasks rather than in defaults.

Application page: `website/docs/applications/other/mumble.md`.
