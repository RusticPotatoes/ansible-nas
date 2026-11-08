# Tailscale

Homepage: <https://tailscale.com/>

Puts the T3 Code remotes on your tailnet, so another T3 Code can link them over HTTPS. T3 Code
refuses to link a plain `http://` address, and `t3_tailscale_serve` has each remote publish
itself with Tailscale's HTTPS instead. Run by `t3.yml` on the `t3` group.

## Usage

Set in `inventories/t3.ini` (git-ignored), under `[t3:vars]`:

```ini
tailscale_enabled=true
t3_tailscale_serve=true
t3_linked_environments=true
```

Then `make t3` (asks sudo's password). The role installs Tailscale from its own signed apt
source, keeps `tailscaled` running, and makes the machine's user Tailscale's operator, so T3
Code's service can run `tailscale serve` without root.

## Specific Configuration

Once, in the tailnet's admin console: turn on MagicDNS and HTTPS certificates (DNS page).

Join each machine once: `sudo tailscale up` and open the link it prints. Or put a reusable auth
key in `vault.yml` as `tailscale_auth_key` and the role joins for you.

Link the machine from another T3 Code at `https://<machine>.<tailnet>.ts.net`; the playbook's
report shows the name.
