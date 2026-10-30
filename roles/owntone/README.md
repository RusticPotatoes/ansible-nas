# owntone

Runs OwnTone, a media server that streams to AirPlay 2 speakers such as HomePods, in a container, paired with a librespot Spotify Connect receiver in a second container. What you play on that receiver goes through a named pipe to OwnTone, which sends it to the speakers you choose. Both containers use the host's network.

Web interface: port `3689` (`owntone_port`), OwnTone's own port on the host network.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `owntone_enabled` | `false` | Starts both containers when `true`; removes both when `false`. |
| `owntone_available_externally` | `false` | Lets Traefik route `owntone_hostname`.`ansible_nas_domain` to it. |
| `owntone_data_directory` | `"{{ docker_home }}/owntone"` | Parent of the folders below. |
| `owntone_config_directory` | `"{{ owntone_data_directory }}/config"` | OwnTone's configuration, mounted at `/etc/owntone`; OwnTone writes `owntone.conf` on first start. |
| `owntone_cache_directory` | `"{{ owntone_data_directory }}/cache"` | OwnTone's database, mounted at `/var/cache/owntone`. |
| `owntone_pipe_directory` | `"{{ owntone_data_directory }}/pipes"` | Holds the FIFO librespot writes to; mounted at `/srv/media` (OwnTone's library) and at `/pipes` in the receiver. |
| `owntone_pipe_name` | `"spotify"` | Name of the audio pipe; a `.metadata` pipe of the same name carries track details. |
| `owntone_spotify_credentials_directory` | `"{{ owntone_data_directory }}/librespot"` | The saved Spotify login (`credentials.json`), mounted at `/data/system-cache` in the receiver. |
| `owntone_spotify_scripts_directory` | `"{{ owntone_data_directory }}/scripts"` | Holds `owntone-metadata.py`, librespot's event hook that passes track details to OwnTone; mounted at `/userscripts`. |
| `owntone_user_id` | `"1000"` | User OwnTone runs as (`UID`) and owner of its folders and pipes. |
| `owntone_group_id` | `"1000"` | Group OwnTone runs as (`GID`) and group of its folders and pipes. |
| `owntone_hostname` | `"owntone"` | Subdomain Traefik uses when it is available externally. |
| `owntone_port` | `"3689"` | OwnTone's web port; Traefik routes to it. |
| `owntone_container_name` | `"owntone"` | Name of the Docker container. |
| `owntone_image_name` | `"owntone/owntone"` | Docker image. |
| `owntone_image_version` | `"latest"` | Image tag. |
| `owntone_memory` | `"512m"` | Memory limit of the OwnTone container. |
| `owntone_airplay_user_agent` | `"AirPlay/999.0.0"` | AirPlay `user_agent` written into `owntone.conf`: HomePods answer 403 unless it starts with `AirPlay/`. |
| `owntone_spotify_container_name` | `"owntone-spotify"` | Name of the Spotify Connect receiver container. |
| `owntone_spotify_image_name` | `"giof71/librespot"` | Receiver image. |
| `owntone_spotify_image_version` | `"latest"` | Receiver image tag. |
| `owntone_spotify_device_name` | `"HomePods"` | Name the receiver shows in the Spotify app (`DEVICE_NAME`). |
| `owntone_spotify_bitrate` | `"320"` | Spotify bitrate (`BITRATE`). |
| `owntone_spotify_initial_volume` | `"100"` | Receiver's starting volume (`INITIAL_VOLUME`). |
| `owntone_spotify_memory` | `"256m"` | Memory limit of the receiver container. |
| `owntone_spotify_discovery` | `false` | `false` hides the receiver from the LAN, so only the account that did the one-time login can use it; `true` lets any Spotify Premium user on the network find it. |

Without discovery, the receiver starts only once a Spotify login is saved in `owntone_spotify_credentials_directory`; until then the role removes it and prints how to log in (see the docs page). A Spotify Premium account is required.

Application page: `website/docs/applications/media-serving/owntone.md`.

Tests: a molecule scenario in `molecule/`.
