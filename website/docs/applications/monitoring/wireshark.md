---
title: "Wireshark"
---

Homepage: [https://www.wireshark.org/](https://www.wireshark.org/)

Wireshark is the world’s foremost and widely-used network protocol analyzer. It lets you see what’s happening on your network at a microscopic level and is the de facto (and often de jure) standard across many commercial and non-profit enterprises, government agencies, and educational institutions. Wireshark development thrives thanks to the volunteer contributions of networking experts around the globe and is the continuation of a project started by Gerald Combs in 1998.

## Usage

Set `wireshark_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Wireshark web interface is on port 3000 of the NAS. The role runs with host networking and sets no port default, so the port is not a link here.
