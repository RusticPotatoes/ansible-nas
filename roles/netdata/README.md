# netdata

Runs Netdata, a real-time system monitoring dashboard, in a container.

- Enable: `netdata_enabled` (default `false`); `netdata_available_externally` controls outside access.
- Port: `netdata_port` (default `19999`); hostname `netdata_hostname`.
- Image: `netdata_image_name` (`netdata/netdata`) / `netdata_image_version` (default `latest`).
- Memory limit: `netdata_memory` (default `1g`).

Application page: none yet under `website/docs/applications/` (the monitoring category holds other tools).

Tests: a molecule scenario in `molecule/`.
