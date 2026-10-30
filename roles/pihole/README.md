# pihole

Runs Pi-hole, a network-wide DNS ad blocker, in a container on its own macvlan network (`pihole_macvlan`), so it has its own address on the LAN.

Ports: DNS on `53` (TCP and UDP), DHCP on `67`/udp and the web interface on `80`, all written in the tasks. `pihole_port` is not used by the tasks.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `pihole_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `pihole_available_externally` | `false` | Meant to route Pi-hole through Traefik. Not used by the tasks yet. |
| `pihole_config_directory` | `"{{ docker_home }}/pihole/config"` | Pi-hole's configuration, mounted at `/etc/pihole`. |
| `pihole_dnsmasq_directory` | `"{{ docker_home }}/pihole/dnsmasq"` | dnsmasq configuration, mounted at `/etc/dnsmasq.d`. |
| `pihole_user_id` | `"1000"` | User ID. Not used by the tasks yet. |
| `pihole_group_id` | `"1000"` | Group ID. Not used by the tasks yet. |
| `pihole_log_level` | `"error"` | Log level. Not used by the tasks yet. |
| `pihole_port` | `"8443"` | Web interface port. Not used by the tasks yet. |
| `pihole_hostname` | `"pihole"` | Traefik hostname. Not used by the tasks yet. |
| `pihole_timezone` | `"{{ ansible_nas_timezone }}"` | Container time zone (`TZ`). |
| `pihole_web_password` | `"{{ vault_pihole_web_password \| default('') }}"` | Web interface and API password (`WEBPASSWORD` and `FTLCONF_webserver_api_password`), also the Homepage widget's key. Read from `vault_pihole_web_password`: set that in your vault, never in git. |
| `pihole_dns_hosts` | `[]` | Local DNS records, each `"<address> <name>"` (e.g. `"192.168.1.10 nas.example.com"`). Empty keeps what the web UI holds; set, it replaces that list (`FTLCONF_dns_hosts`). |
| `pihole_rev_servers` | `[]` | Names Pi-hole asks the router for, each `"true,<LAN CIDR>,<router>,<router's domain>"` (`FTLCONF_dns_revServers`). Empty: none. |
| `pihole_memory` | `1g` | Container memory limit. |
| `pihole_container_name` | `pihole` | Name used to remove the container when disabled. The start task names it `pihole` directly. |

The image is `pihole/pihole:latest` and the container's LAN address is fixed, both set in the tasks. The macvlan network uses `primary_eth`, `ansible_nas_subnet` and `ansible_nas_gateway`. The container gets the `NET_ADMIN` capability.

Application page: `website/docs/applications/system-tools/pihole.md`.

Tests: a molecule scenario in `molecule/`.
