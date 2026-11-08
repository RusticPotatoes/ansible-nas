# Build machines

Homepage: <https://docs.docker.com/engine/>

Moves heavy builds off the laptop onto another Linux machine. `builders.yml` installs, on each
machine in the `builders` group:

- **Docker** with the Compose plugin (the pinned `geerlingguy.docker` role), the machine's user
  in the `docker` group, and the build cache pruned past `build_host_build_cache_keep`;
- **Rust** for that user (rustup, no root) with clippy and rustfmt, and the native build tools
  (`build-essential`, `pkg-config`, `libssl-dev`, `cmake`, `clang`), so agents T3 Code runs
  there can use `cargo`.

## Usage

Add the machine to a `[builders]` group in `inventories/t3.ini` (see the T3 Code remotes page
for the file), then from the laptop: `make builders` (asks sudo's password).

## Specific Configuration

Point the laptop's Docker at it once:

```sh
docker context create builder --docker host=ssh://me@192.0.2.10
docker --context builder info
```

A project that builds through a Docker context then builds there. Endora, for one: set
`ENDORA_BUILD_CONTEXT = builder` in its `local.mk`, and `make deploy` builds the images on the
builder for the target's CPU and copies them to the target. An x86-64 builder builds x86-64
targets natively; keep arm64 builds (a Raspberry Pi) on an arm64 machine, e.g.
`ENDORA_PI_BUILD_CONTEXT = desktop-linux` on an Apple-silicon laptop.
