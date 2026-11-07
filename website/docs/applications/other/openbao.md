---
title: "OpenBao"
---

Homepage: [https://openbao.org](https://openbao.org)

OpenBao is the open-source fork of HashiCorp Vault (MPL-2.0): the house's vault for machine
secrets. It runs in its own role, on its own network, and is unsealed by you. Endora's node is
one client of it ([Endora ADR 0127](https://github.com/RusticPotatos/Endora/blob/develop/docs/adr/0127-openbao-and-the-passkey-unlock.md),
amended 2026-11-07); until 7 Nov 2026 the role shipped in Endora's `endora.homelab` collection.

No key, share or token is ever set in this repository or your inventory. You type them
yourself, at the vault's own prompt.

## Usage

Set `openbao_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file, then
run the playbook with `-t openbao`.

## What it runs

- The official image, **pinned by digest** (`openbao_image`), never pulled again and never
  auto-updated (a `watchtower.enable=false` label): a new vault image is a decision.
- Its own Docker network, `openbao` (`openbao_network_name`): internal, with no address on the
  host, so the vault reaches no internet, no LAN and not the NAS. A client joins it by name and
  reaches the vault at `http://openbao:8200`.
- Integrated (raft) storage and the audit log in `openbao_data_directory`
  (`{{ docker_home }}/openbao`, the folder Endora's role used; an inventory that still sets
  `openbao_data_dir` is honoured), owned by the image's `openbao` user, mode `0700`. The storage
  is encrypted by the vault's barrier: a copy of it opens nothing without the unseal shares.
- Read-only root filesystem, every capability dropped, `no-new-privileges`, 256 MB.
- **A health check that is healthy only when the vault is unsealed.** Sealed (or not yet
  initialised), `docker ps` shows it `unhealthy`, and the lab's "Docker Container Unhealthy"
  alert fires. Every run of the role ends by saying which: unsealed, sealed, or not initialised.
- No port on the NAS unless `openbao_port` asks for one (e.g. `127.0.0.1:8200`). The commands
  below run inside the container and need none.

The role removes a container named `endora-openbao` (Endora's role's) before it starts its own,
so two servers never open the same folder. It never removes the data folder; switched off, it
removes only its container.

## Clients

**Endora's node**: in Endora's `local.mk` (for `make deploy`), or with the `endora` role,

```text
ENDORA_VAULT_URL = http://openbao:8200          endora_vault_url: http://openbao:8200
ENDORA_VAULT_NETWORK = openbao                  endora_vault_network: openbao
```

The network must exist before the node starts with it: run this role first.

## Unsealing

The vault seals itself on every restart. Unseal it on the NAS with two of your three shares:

```bash
docker exec -it openbao bao operator unseal -address=http://127.0.0.1:8200
```

Run it twice. Each time it asks `Unseal Key (will be hidden):`: paste one share there, never
on the command line (that would put it in your shell's history). Then check:

```bash
docker exec openbao bao status -address=http://127.0.0.1:8200   # Sealed  false
docker inspect -f '{{.State.Health.Status}}' openbao             # healthy (within a minute)
```

## Initialising a fresh vault

Only on an empty data folder (the role's run says `not initialised`). On the NAS, in a terminal
that is not being recorded (no `script`, no tmux logging):

```bash
docker exec -it openbao bao operator init -address=http://127.0.0.1:8200 -key-shares=3 -key-threshold=2
```

**3 shares, any 2 open it**: one lost is survivable, one found opens nothing (Endora ADR 0127
§2). It prints the three shares and an initial root token, once. Save each share as its own
password-manager item, the root token as another, copy the shares into your paper kit, then
clear the terminal (`clear && printf '\033[3J'`, or ⌘K in Terminal) and unseal as above.

The root token can do anything. Endora's own setup revokes its root token as soon as setup is
done; to do the same, once nothing needs it:

```bash
docker exec -it openbao sh -c 'printf "Root token: "; read -rs T; echo; BAO_TOKEN="$T" bao token revoke -self -address=http://127.0.0.1:8200'
```

A new one can be made later from two shares (`bao operator generate-root`).

## Backups

The data folder is in `docker_home`, which the lab's backup reaches. For a consistent copy
while it runs, `bao operator raft snapshot save` (with a token that may) is the tool. Keep the
shares apart from any copy of the folder.

## Moving from Endora's role

A one-time move, done in this order; [Endora's homelab guide](https://github.com/RusticPotatos/Endora/blob/develop/docs/homelab.md#the-vault-adr-0127)
has the full procedure and the rollback.

1. Back up the data folder with the old container stopped, and check the archive holds
   `openbao/vault.db` and `openbao/raft/raft.db`, neither empty.
2. Merge this role, then run the playbook with `-t openbao`: it removes `endora-openbao`, makes
   the `openbao` network and starts `openbao` on the same folder.
3. Deploy Endora with `ENDORA_VAULT_NETWORK = openbao`.
4. Unseal (or initialise fresh, after moving the old folder aside).
5. When the node no longer uses it: `docker network rm endora_vault`.
