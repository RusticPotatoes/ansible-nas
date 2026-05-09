---
title: "VPN Downloads"
---

The VPN download stack runs selected download tools through a shared Gluetun VPN
container. Gluetun owns the published ports, while the download containers share
Gluetun's network namespace.

To enable it, add the following to your `inventories/<your_inventory>/group_vars/nas.yml`:

```yaml
vpn_download_stack_enabled: true
```

By default this enables:

```yaml
gluetun_enabled: true
prowlarr_enabled: true
deluge_enabled: true
radarr_enabled: true
sonarr_enabled: true
nzbget_enabled: true
```

Optional download tools can be included with:

```yaml
vpn_download_stack_readarr_enabled: true
vpn_download_stack_jackett_enabled: true
vpn_download_stack_sabnzbd_enabled: true
```

When the stack is enabled, these application containers do not publish their own
ports. Their web UIs are exposed through Gluetun's port bindings so outbound
download traffic uses the VPN path.
