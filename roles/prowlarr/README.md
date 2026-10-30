# Prowlarr

Prowlarr is an indexer manager and API proxy for download clients (Sonarr, Radarr, etc.). It centralises indexer configuration and provides a single API endpoint for search and download.

## Variables

| Variable | Default |
|----------|---------|
| `prowlarr_enabled` | `false` |
| `prowlarr_available_externally` | `false` |
| `prowlarr_data_directory` | `"{{ docker_home }}/prowlarr/config"` |
| `prowlarr_user_id` | `"0"` |
| `prowlarr_group_id` | `"0"` |
| `prowlarr_port` | `"9696"` |
| `prowlarr_hostname` | `"prowlarr"` |
| `prowlarr_container_name` | `"prowlarr"` |
| `prowlarr_image_name` | `"ghcr.io/linuxserver/prowlarr"` |
| `prowlarr_image_version` | `"develop"` |
| `prowlarr_memory` | `1g` |

## Port

- **9696** — Web UI
