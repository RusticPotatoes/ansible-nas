# T3 Code remotes

Homepage: <https://github.com/pingdotgg/t3code>

Makes any Linux machine a T3 Code remote that runs coding agents for the desktop app, so the work
runs there instead of on the laptop. Not a container: the `t3_host` role installs, for the
machine's own user and without root:

- **Node.js LTS** from nodejs.org, checked against its published checksum;
- the agents' CLIs from their makers' installers: **Claude Code** (`claude`), **Codex**
  (`codex`) and **Antigravity** (`agy`), plus Antigravity's ACP runtime that T3 Code needs;
- `~/.local/bin` on `PATH` for every shell, SSH commands included;
- T3 Code's **always-on service** (`t3 service install`, a systemd user unit) with that `PATH`,
  started at boot by linger (the one step that needs sudo).

It turns the three providers on in T3 Code's settings and keeps every other setting.

## Usage

List the machines in `inventories/t3.ini` (git-ignored):

```ini
[t3]
box1 ansible_host=192.0.2.10
box2 ansible_host=192.0.2.11

[t3:vars]
ansible_user=me
```

Then, from the laptop: `make t3` (applies straight away, `DRY=1` for a dry run and a yes first; asks sudo's password for
linger). Without sudo: `make t3 EXTRA="--skip-tags t3_host_sudo"`.

Drop an entry from `t3_clis` to leave an agent off; set `t3_service_enabled: false` to keep
T3 Code started only by the desktop app over SSH. Set `t3_lan: true` (for example under
`[t3:vars]`) to let other devices on the network reach the service at
`http://<machine>:3773`, so another T3 Code can link the machine and run threads there; a device
still needs a pairing token.

## Specific Configuration

Once per machine, sign each agent in (the role cannot, it needs your browser):

- `claude auth login`: open the link, paste the code back;
- `codex login --device-auth`: enter the code at the link (one machine at a time);
- Antigravity: in T3 Code, that machine's provider settings, sign in with Google.

Only one T3 Code server may own `~/.t3`: the role stops a server the desktop app started over
SSH so the service can take over. Optional, by hand: `t3 service protect` (asks for sudo)
shields the server from agents that exhaust memory. Prefer `t3_lan` to `t3 up --lan`, so the
playbook keeps the setting; avoid `t3 up --yes`, which turns T3 Connect on.

## Local models through OpenCode

`t3_opencode_enabled` (on by default) installs OpenCode at the pinned `t3_opencode_version`, links it
into the binaries folder and turns T3 Code's OpenCode provider on. `t3_opencode_ollama` lists the
Ollama servers it offers (OpenAI-compatible `/v1` addresses); the first model of the first server is
the default. The default points at `nas.home.arpa`. To add a laptop's Ollama as an extra choice,
append it to the list in your inventory: it is only there while the laptop is awake. OpenCode's
installer can lag behind the latest release, so the version is pinned here rather than "latest".
