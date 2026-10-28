# gluetun

Runs gluetun, a VPN client that routes traffic through a WireGuard or OpenVPN tunnel, in a container.

- Enable: `gluetun_enabled` (default `false`); `gluetun_available_externally` controls outside access.
- Container: `gluetun_container_name` (default `gluetun`); displayed as `gluetun_name` (default `container:{{ gluetun_container_name }}`).
- Network: `gluetun_network_name` (default `gluetun`); `gluetun_routed_containers` (default `[]`) lists containers whose traffic is routed through the VPN.
- Image: `gluetun_image_name` (`qmcgaw/gluetun`) / `gluetun_image_version` (default `latest`).
- Memory limit: `gluetun_memory` (default `512m`).
- Config: `gluetun_config_directory` (default `/{{ docker_home }}/gluetun`).
- Ports: `gluetun_http_port` (default `8000:8000`, optional Web UI); `gluetun_dns_port` (default `53`, internal DNS).
- Traefik: `gluetun_hostname` (default `vpn`); `ansible_nas_domain` (default `example.com`).
- Periodic restart: `gluetun_periodic_restart_enabled` (default `false`); `gluetun_periodic_restart_interval` (default `2h`); `gluetun_periodic_restart_script_path` (default `/usr/local/sbin/gluetun-stack-restart`).
- Ansible recovery: `gluetun_recover_with_ansible_enabled` (default `true`); `gluetun_ansible_repo_path` (default `{{ playbook_dir }}`); `gluetun_ansible_playbook` (default `{{ playbook_dir }}/nas.yml`); `gluetun_ansible_inventory` (default `{{ inventory_file | default(playbook_dir + '/inventories/inventory.ini') }}`); `gluetun_ansible_vault_file` (default `{{ playbook_dir }}/vault.yml`); `gluetun_ansible_vault_password_file` (default `{{ playbook_dir }}/vault_password.txt`).
