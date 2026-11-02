---
title: "Homepage"
---

Homepage: [https://gethomepage.dev](https://gethomepage.dev)

A modern, fully static, fast, secure fully proxied, highly customizable application dashboard
with integrations for over 100 services and translations into multiple languages.
Easily configured via YAML files or through docker label discovery.

## Usage

Set `homepage_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Homepage web interface can be found at [http://ansible_nas_host_or_ip:11111](http://ansible_nas_host_or_ip:11111).

## Specific Configuration

Homepage defaults to port 11111. Override `homepage_port` to move it somewhere else.
