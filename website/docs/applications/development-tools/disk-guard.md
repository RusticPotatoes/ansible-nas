# Disk guard

Keeps each T3 Code remote's disks from filling, so it runs indefinitely without anyone cleaning
up after the agents. `t3.yml` installs it on every machine in the `t3` group: a script and an
hourly systemd user timer that

- **caps build output**: cargo `target` folders (only those holding cargo's `CACHEDIR.TAG`)
  under `disk_guard_roots` are deleted once unused for `disk_guard_target_max_age_days`, then the
  least recently used go until their total is under `disk_guard_target_cap_mb`. A folder
  written to in the last `disk_guard_active_minutes` is never touched. Machines in the
  `builders` group keep up to 60 GB for 3 days; any other machine is not for building, so 2 GB
  for a day;
- **prunes old logs**: files older than `disk_guard_log_max_age_days` under `disk_guard_log_dirs`
  (T3's provider logs by default);
- **alerts early**: when a disk in `disk_guard_mounts` reaches `disk_guard_alert_percent` (80%),
  it says so in the journal and, if a topic is set, on [ntfy](https://ntfy.sh), at most once
  every `disk_guard_alert_every_hours`.

Docker's own build cache is capped separately, on build machines, by `build_host_build_cache_keep`.

## Usage

From the laptop, with the ntfy topic in the environment (it is never written to a tracked file):

```sh
export DISK_GUARD_NTFY_TOPIC=<your-topic>
make t3 EXTRA="-K --tags disk_guard"
```

See what it did: `journalctl --user -u disk-guard` on the machine.

## Specific Configuration

`disk_guard_root_lv_size` (e.g. `200g`) grows the root logical volume to that size when set,
for an install whose volume group has unallocated space (Ubuntu's installer often leaves much
of the disk free); it needs sudo and never shrinks the volume. Check first with `sudo vgs`:

```sh
make t3 EXTRA="-K --tags disk_guard -e disk_guard_root_lv_size=200g --limit <host>"
```
