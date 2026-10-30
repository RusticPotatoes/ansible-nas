# NZBGet

NZBGet is a binary Usenet downloader. It fetches content from Usenet servers based on NZB files produced by search tools (Prowlarr, Sabnzbd, etc.) and stores them in the designated download directory.

## Variables

| Variable | Default |
|----------|---------|
| `nzbget_enabled` | `false` |
| `nzbget_available_externally` | `false` |
| `nzbget_data_directory` | `"{{ docker_home }}/nzbget"` |
| `nzbget_download_directory` | `"{{ downloads_root }}"` |
| `nzbget_user_id` | `"0"` |
| `nzbget_group_id` | `"0"` |
| `nzbget_port` | `"6789"` |
| `nzbget_hostname` | `"nzbget"` |
| `nzbget_container_name` | `"nzbget"` |
| `nzbget_image_name` | `"linuxserver/nzbget"` |
| `nzbget_image_version` | `"latest"` |
| `nzbget_memory` | `"1g"` |

## Port

- **6789** — Web UI
