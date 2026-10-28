# gluetun

Runs Gluetun, a VPN client, in a container. Other containers can share its network, so all of
their traffic leaves through the VPN tunnel (WireGuard, custom provider).

Port: the control server and web UI on `8000` (`gluetun_http_port`, published as `8000:8000`).
The ports of each container in `gluetun_routed_containers` are published on gluetun too, since
those containers have no network of their own.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it does |
| --- | --- | --- |
| `gluetun_enabled` | `false` | Start gluetun; `false` removes the container. |
| `gluetun_available_externally` | `false` | Route `gluetun_hostname` through Traefik. |
| `gluetun_network_name` | `"gluetun"` | Name kept for a gluetun network; the tasks do not use it. |
| `gluetun_name` | `"container:{{ gluetun_container_name }}"` | The `network_mode` other roles use to route through gluetun. |
| `gluetun_routed_containers` | `[]` | Containers routed through gluetun: each has a `name` and its `ports`. They are stopped before gluetun is recreated. |
| `gluetun_container_name` | `"gluetun"` | Container name. |
| `gluetun_image_name` | `"qmcgaw/gluetun"` | Image. |
| `gluetun_image_version` | `"latest"` | Image tag. |
| `gluetun_memory` | `"512m"` | Memory limit. |
| `gluetun_periodic_restart_enabled` | `false` | Restart the VPN stack on a timer (a job of the `nas_maintenance` role). |
| `gluetun_periodic_restart_interval` | `"2h"` | How often that restart runs. |
| `gluetun_periodic_restart_script_path` | `"/usr/local/sbin/gluetun-stack-restart"` | Where the restart script is installed. |
| `gluetun_recover_with_ansible_enabled` | `true` | Let the restart script run the playbook to repair the stack. |
| `gluetun_ansible_repo_path` | `"{{ playbook_dir }}"` | Checkout the repair runs from. |
| `gluetun_ansible_playbook` | `"{{ playbook_dir }}/nas.yml"` | Playbook the repair runs. |
| `gluetun_ansible_inventory` | `"{{ inventory_file \| default(playbook_dir + '/inventories/inventory.ini') }}"` | Inventory the repair uses. |
| `gluetun_ansible_vault_file` | `"{{ playbook_dir }}/vault.yml"` | Encrypted vars file the repair loads. |
| `gluetun_ansible_vault_password_file` | `"{{ playbook_dir }}/vault_password.txt"` | Password file for it. |
| `gluetun_config_directory` | `"/{{ docker_home }}/gluetun"` | Holds `wireguard/` (the tunnel's config) and `auth/`. |
| `gluetun_http_port` | `"8000:8000"` | Host:container port of the control server. |
| `gluetun_dns_port` | `53` | Gluetun's internal DNS port; not published by the tasks. |
| `gluetun_hostname` | `"vpn"` | Traefik hostname, under `ansible_nas_domain`. |
| `ansible_nas_domain` | `"example.com"` | Domain for the Traefik route; normally set for the whole NAS. |

The `gluetun_ansible_*` paths default to the paths of the machine that runs the playbook, which
is often not the NAS (see `AGENTS.md`, "How a change reaches the NAS"). Before turning the
repair on, point them at the NAS's own checkout.

The tasks also read `gluetun_firewall_outbound_subnets` (default empty), the local subnets the
routed containers may still reach outside the tunnel. Other roles route through gluetun when
`vpn_download_stack_enabled` is true.

Application page: `website/docs/applications/download-tools/gluetun.md`.

Tests: a molecule scenario in `molecule/`.
