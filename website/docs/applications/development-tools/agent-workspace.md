# Agent workspace

Gives each T3 Code remote (see [T3 Code remotes](t3-host.md)) a working agent workspace, made
only by the playbook: no hand edits over SSH and no T3 clone tool. The `agent_workspace` role runs
after `t3_host` and is off unless `agent_workspace_enabled` is true. On each machine it:

- installs **git**, **rsync** and **gh** (from GitHub's own signed apt source) and sets the git
  identity;
- makes one **ed25519 deploy key per repository** on the machine and registers it from the
  machine that runs the play, with that machine's `gh` (logged in with admin on each repository),
  titled `t3-<machine>`; a key already registered under that title is left alone;
- writes `~/.ssh/config` aliases (`github-<name>`) and GitHub's pinned host keys;
- clones each repository into `~/repos/<name>`, only ever fast-forwarding, and sets a read-only
  repository's push URL to `disabled://reader`;
- runs agent-config's installer and check, and reports its `config-version`;
- starts an **hourly systemd user timer** running agent-config's `scripts/update.sh`;
- on one machine, **once**, copies the steward's private state (see below).

## Usage

In the git-ignored `inventories/t3.ini` (fictional values):

```ini
[t3:vars]
agent_workspace_enabled=true
agent_workspace_git_name=Example
agent_workspace_git_email=12345+example@users.noreply.github.com
agent_workspace_repos=[{"name": "notes", "repo": "example-owner/notes", "read_only": true}]

[t3]
box1 ansible_host=192.0.2.10 agent_workspace_seed_local_state=true
box2 ansible_host=192.0.2.11 agent_workspace_repos=[{"name": "notes", "repo": "example-owner/notes", "read_only": true}]
```

Then `make t3` from the laptop. It needs `gh auth status` to be logged in there with the
`admin:public_key` scope and admin on each repository.

## Specific Configuration

`agent_workspace_seed_local_state` copies `agent_workspace_seed_source` (a folder on the laptop)
to the machine with rsync, leaving out `agent_workspace_seed_exclude` (provider sign-ins, T3
state, memory, the rebuild archive). It runs only if the marker file is absent and writes it
after: from then on the machine's copy is authoritative and the play never overwrites it. Delete
the marker to seed again.

If a machine is rebuilt, delete its `t3-<machine>` deploy keys on GitHub first; the play stops
with a message when a key under that title does not match the machine's current one.
