# ansible-nas-general

General host setup for the NAS: login banner, apt cache and optional full upgrade, extra packages, optional unattended upgrades, hostname, time zone, optional systemd-resolved DNS settings, and the ownership of the Samba share folders. It runs no container.

No port.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ansible_nas_hostname` | `ansible-nas` | Hostname set on the NAS. |
| `keep_packages_updated` | `false` | Upgrade all apt packages on every run. |
| `ansible_nas_extra_packages` | see below | Extra apt packages to install. |
| `ansible_nas_timezone` | `Etc/UTC` | Time zone of the host; most container roles pass it on as `TZ`. |
| `ansible_nas_configure_systemd_resolved` | `false` | Write a systemd-resolved drop-in so host lookups (including image pulls) do not depend on LAN DNS. |
| `ansible_nas_resolved_dns_servers` | `"{{ default_dns_servers \| default(['1.1.1.1', '9.9.9.9']) }}"` | `DNS=` servers of that drop-in; also used for `/etc/resolv.conf` below. |
| `ansible_nas_resolved_fallback_dns_servers` | `"{{ default_dns_servers \| default(['1.1.1.1', '9.9.9.9']) }}"` | `FallbackDNS=` servers. |
| `ansible_nas_resolved_domains` | see below | `Domains=` of the drop-in. |
| `ansible_nas_resolved_cache_no_negative` | `true` | `Cache=no-negative` when `true`, `Cache=yes` otherwise. |
| `ansible_nas_resolved_use_uplink_resolv_conf` | `false` | Also write a plain `/etc/resolv.conf` listing `ansible_nas_resolved_dns_servers`. |
| `ansible_nas_unattended_upgrades_enabled` | `false` | Install and turn on unattended-upgrades. |
| `ansible_nas_unattended_reboot` | `false` | Let unattended-upgrades reboot when an update requires it. |
| `ansible_nas_unattended_reboot_with_users` | `false` | Reboot even when users are logged in. |
| `ansible_nas_unattended_reboot_time` | `"04:00"` | Time of those automatic reboots. |
| `ansible_nas_unattended_remove_unused_dependencies` | `true` | Let unattended-upgrades remove unused dependencies. |

Default of `ansible_nas_extra_packages`:

```yaml
ansible_nas_extra_packages:
  - smartmontools
  - htop
  - zfsutils-linux
  - bonnie++
  - unzip
  - lm-sensors
```

Default of `ansible_nas_resolved_domains`:

```yaml
ansible_nas_resolved_domains:
  - "~."
```

The last task gives every folder in `samba_shares` (set elsewhere) to the `ansible-nas` user and group, which the `ansible-nas-users` role creates. The login banner is the role's `files/motd.txt`.

Application page: none yet under `website/docs/applications/`.
