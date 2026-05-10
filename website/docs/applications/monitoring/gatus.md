---
title: "Gatus"
---

Homepage: [https://gatus.io](https://gatus.io)

Gatus is an open source synthetic monitoring tool that performs health checks on your services, exposes a status dashboard, and can send alerts when checks fail.

## Usage

Set `gatus_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Gatus web interface can be found at `http://ansible_nas_host_or_ip:8080`.

The default config is stored at `{{ docker_home }}/gatus/config.yml`; edit it to add your own checks and notifications.
