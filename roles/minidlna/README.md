# minidlna

Runs MiniDLNA, a DLNA/UPnP media server that serves music, pictures and video to clients on the local network, in a container.

Port `8201` (`minidlna_port`), with a very basic web page. The container uses the host's network, so DLNA discovery works.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `minidlna_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `minidlna_available_externally` | `false` | Kept for outside access; the tasks set no Traefik labels, so it has no effect. |
| `minidlna_media_directory1` | `"{{ movies_root }}"` | First media folder, mounted at `/media1`. |
| `minidlna_media_directory2` | `"{{ tv_root }}"` | Second media folder, mounted at `/media2`. |
| `minidlna_friendly_name` | `"{{ ansible_nas_hostname }}"` | Name clients see (`MINIDLNA_FRIENDLY_NAME`). |
| `minidlna_port` | `"8201"` | Port MiniDLNA listens on (`MINIDLNA_PORT`), on the host's network. |
| `minidlna_container_name` | `"minidnla"` | Name of the Docker container. |
| `minidlna_image_name` | `"vladgh/minidlna"` | Docker image. |
| `minidlna_image_version` | `"latest"` | Image tag. |
| `minidlna_memory` | `"1g"` | Container memory limit. |

Application page: `website/docs/applications/media-serving/minidlna.md`.

Tests: a molecule scenario in `molecule/`.
