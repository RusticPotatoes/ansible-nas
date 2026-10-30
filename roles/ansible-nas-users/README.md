# ansible-nas-users

Creates the accounts the NAS needs: the `ansible-nas` system user and group (no home, no login shell), and, when `ansible_nas_user` is set, that account with a home, bash and membership of the `docker` group. When `ansible_become_password` is also set, it adds that user to Samba with the same password.

The role has no `defaults/main.yml`. It reads `ansible_nas_user` (default in the `ansible-nas-docker` role) and `ansible_become_password`, both optional; keep the password in your vault, never in git. It runs no container and opens no port.

Application page: none yet under `website/docs/applications/`.
