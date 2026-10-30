# Gluetun

Gluetun is a VPN client that runs in Docker and provides a WireGuard/OpenVPN tunnel for the home lab. It creates a dedicated Docker network that other containers (deluge, nzbget, prowlarr) can route through for privacy.

## Variables

| Variable | Default |
|----------|---------|
| `gluetun_enabled` | `false` |
| `gluetun_available_externally` | `false` |
| `gluetun_network_name` | `"gluetun"` |
| `gluetun_name` | `"container:{{ gluetun_container_name }}"` |
| `gluetun_routed_containers` | `[]` |
| `gluetun_container_name` | `"gluetun"` |
| `gluetun_image_name` | `"qmcgaw/gluetun"` |
| `gluetun_image_version` | `"latest"` |
| `gluetun_memory` | `"512m"` |
| `gluetun_periodic_restart_enabled` | `false` |
| `gluetun_periodic_restart_interval` | `"2h"` |
| `gluetun_periodic_restart_script_path` | `"/usr/local/sbin/gluetun-stack-restart"` |
| `gluetun_recover_with_ansible_enabled` | `true` |
| `gluetun_ansible_repo_path` | `"{{ playbook_dir }}"` |
| `gluetun_ansible_playbook` | `"{{ playbook_dir }}/nas.yml"` |
| `gluetun_ansible_inventory` | `"{{ inventory_file \| default(playbook_dir + '/inventories/inventory.ini') }}"` |
| `gluetun_ansible_vault_file` | `"{{ playbook_dir }}/vault.yml"` |
| `gluetun_ansible_vault_password_file` | `"{{ playbook_dir }}/vault_password.txt"` |
| `gluetun_config_directory` | `"/{{ docker_home }}/gluetun"` |
| `gluetun_http_port` | `"8000:8000"` |
| `gluetun_dns_port` | `53` |
| `gluetun_hostname` | `"vpn"` |
| `ansible_nas_domain` | `"example.com"` |

## Port

- **8000** — Web UI (optional, for debugging)
- **53** — Internal DNS
