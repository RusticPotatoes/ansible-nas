# Samba Shares

Ansible-NAS uses the awesome [vladgh.samba](https://github.com/vladgh/ansible-collection-vladgh-samba) Ansible role to configure Samba - check out [the Ansible Galaxy page](https://galaxy.ansible.com/vladgh/samba) for the many different options you can use to configure a share.

## Share Examples

Ansible-NAS shares are defined in the `samba_shares` section within `group_vars/all.yml`. The examples provided are "public" shares that anyone on your LAN can read and write to.

## File Permissions

Ansible-NAS creates an `ansible-nas` user and group on your server, which Samba will use to access the data in your shares. New data created will be permissioned correctly.

However, if you have existing data this will need to be repermissioned so that Samba can read and serve it. An playbook is provided to do this for you - `permission_data.yml`. It is separated from the main Ansible-NAS playbook due to the time it can take to run with large amounts of data - you should only need to run this once.

## Time Machine Share

A Mac backup target is the `timemachine` entry of `samba_extra_shares`, with a dedicated `timemachine` Samba user in `samba_users` (its password is the vault variable `vault_timemachine_password`). The share is not open to guests, and its folder is owned by that user with mode `0700`. Keep it out of any backup plan: Time Machine keeps its own history.

Connect from the Mac with `smb://timemachine@<NAS address>/timemachine`. Avahi is not set up here, so the share does not appear in Finder by itself.
