# nomad

Installs HashiCorp Nomad, a scheduler and orchestrator for containers and other applications, from HashiCorp's apt repository and runs it as a systemd service on the host, as both server and client. It does not run in a container.

Ports: web interface and API on `4646` (`nomad_port_http`), RPC on `4647` (`nomad_port_rpc`) and Serf on `4648` (`nomad_port_serf`), bound on all addresses.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `nomad_enabled` | `false` | Installs, configures and starts Nomad when `true`; stops and uninstalls it when `false`. |
| `nomad_data_home` | `"{{ docker_home }}/nomad"` | Nomad's `data_dir` is its `data/` subfolder. |
| `nomad_service_name` | `nomad` | Name of the systemd service started, restarted and stopped. |
| `nomad_port_http` | `4646` | HTTP port in `/etc/nomad.d/nomad.hcl`. |
| `nomad_port_rpc` | `4647` | RPC port in `/etc/nomad.d/nomad.hcl`. |
| `nomad_port_serf` | `4648` | Serf port in `/etc/nomad.d/nomad.hcl`. |

The config template (`templates/nomad.hcl`) gives the client a host volume `docker_data` at `docker_home`. The uninstall step checks `nomad_install`, which the preceding `stat` task does not register.

Application page: `website/docs/applications/development-tools/nomad.md`.

Tests: a molecule scenario in `molecule/`.
