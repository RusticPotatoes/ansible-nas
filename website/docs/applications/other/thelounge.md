---
title: "The Lounge"
---

Homepage: [https://thelounge.chat/](https://thelounge.chat/)

The Lounge is a self-hosted web IRC client.

## Usage

Set `thelounge_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

The Lounge web interface can be found at [http://ansible_nas_host_or_ip:9000](http://ansible_nas_host_or_ip:9000).

## Specific Configuration

The first time the role runs, it creates the `admin` account with the default password `admin` in `users/admin.json` under the data directory. Log in with that account and change the password straight away.

Later playbook runs leave `users/admin.json` alone: the password you set, your networks and sessions are kept. The role only writes the file when it is missing. To reset the account to the default, stop The Lounge, delete `users/admin.json` and run the playbook again.
