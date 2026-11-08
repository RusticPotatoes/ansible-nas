# valheim

Runs a Valheim dedicated game server in a container, with the `mbround18/valheim` image (Odin), which adds automatic updates and world backups.

Game ports: `2456`, `2457` and `2458` (UDP; `valheim_port_a`, `valheim_port_b`, `valheim_port_c`). Players connect to `2456`.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `valheim_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `valheim_available_externally` | `false` | Lets Traefik route `valheim_hostname`.`ansible_nas_domain` to it. |
| `valheim_data_directory` | `"{{ docker_home }}/valheim"` | Base folder; its `saves`, `server` and `backups` subfolders hold the worlds, the server files and the backups. |
| `valheim_port_a` | `"2456"` | Host port published to the container's UDP port 2456; also the server's `PORT`. |
| `valheim_port_b` | `"2457"` | Host port published to the container's UDP port 2457. |
| `valheim_port_c` | `"2458"` | Host port published to the container's UDP port 2458. |
| `valheim_hostname` | `"valheim"` | Subdomain Traefik uses when it is available externally. |
| `valheim_container_name` | `"valheim"` | Name of the Docker container. |
| `valheim_image_name` | `"mbround18/valheim"` | Docker image. |
| `valheim_image_version` | `"latest"` | Image tag. |
| `valheim_user_id` | `"1000"` | User the server runs as (`PUID`) and owner of its folders. |
| `valheim_group_id` | `"1000"` | Group the server runs as (`PGID`) and group of its folders. |
| `valheim_memory` | `1g` | Container memory limit. |
| `valheim_name` | `"Created With Valheim Docker"` | Server name (`NAME`). |
| `valheim_world` | `"Dedicated"` | World name (`WORLD`). |
| `valheim_password` | `"Strong! Password @ Here"` | Server password (`PASSWORD`). The default is a placeholder: set your own in your vars, never in git. |
| `valheim_public` | `"1"` | List the server publicly (`PUBLIC`). |
| `valheim_auto_update` | `"1"` | Update the server automatically (`AUTO_UPDATE`). |
| `valheim_auto_update_pause_with_players` | `"0"` | Hold updates while players are online (`AUTO_UPDATE_PAUSE_WITH_PLAYERS`). |
| `valheim_auto_update_schedule` | `"0 1 * * *"` | Cron schedule of the update check (`AUTO_UPDATE_SCHEDULE`). |
| `valheim_auto_backup` | `"1"` | Back up the world automatically (`AUTO_BACKUP`). |
| `valheim_auto_backup_nice_level` | `"19"` | Nice level of the backup job (`AUTO_BACKUP_NICE_LEVEL`). |
| `valheim_auto_backup_schedule` | `"*/15 * * * *"` | Cron schedule of the backups (`AUTO_BACKUP_SCHEDULE`). |
| `valheim_auto_backup_remove_old` | `"1"` | Remove old backups (`AUTO_BACKUP_REMOVE_OLD`). |
| `valheim_auto_backup_days_to_live` | `"3"` | Days a backup is kept (`AUTO_BACKUP_DAYS_TO_LIVE`). |
| `valheim_auto_backup_on_update` | `"1"` | Back up before an update (`AUTO_BACKUP_ON_UPDATE`). |
| `valheim_auto_backup_on_shutdown` | `"1"` | Back up on shutdown (`AUTO_BACKUP_ON_SHUTDOWN`). |
| `valheim_auto_backup_pause_with_no_players` | `"0"` | Skip backups while nobody plays (`AUTO_BACKUP_PAUSE_WITH_NO_PLAYERS`). |
| `valheim_webhook_url` | `"https://discord.com/api/webhooks/IM_A_SNOWFLAKE/AND_I_AM_A_SECRET"` | Webhook for server notices. Not passed by default: its line in `valheim_env` is commented out. The default is a placeholder. |
| `valheim_webhook_include_public_ip` | `"1"` | Include the public IP in webhook notices. Not passed by default (commented out in `valheim_env`). |
| `valheim_update_on_startup` | `"0"` | Update when the server starts (`UPDATE_ON_STARTUP`). |
| `valheim_enable_crossplay` | `"0"` | Allow crossplay (`ENABLE_CROSSPLAY`). |
| `valheim_type` | `"Vanilla"` | Server type, such as `Vanilla` (`TYPE`). |
| `valheim_preset` | `""` | World preset. Not passed by default (commented out in `valheim_env`). |
| `valheim_modifiers` | `""` | World modifiers. Not passed by default (commented out in `valheim_env`). |
| `valheim_set_key` | `""` | World key. Not passed by default (commented out in `valheim_env`). |
| `valheim_mods` | `""` | Mods to install. Not passed by default (commented out in `valheim_env`). |
| `valheim_additional_steamcmd_args` | `""` | Extra SteamCMD arguments. Not passed by default (commented out in `valheim_env`). |
| `valheim_scheduled_restart` | `"0"` | Restart the server on a schedule (`SCHEDULED_RESTART`). |
| `valheim_scheduled_restart_schedule` | `"0 2 * * *"` | Cron schedule of that restart (`SCHEDULED_RESTART_SCHEDULE`). |
| `valheim_env` | see below | The container's whole environment, built from the variables above. Override it to pass other settings of the image. |

Default of `valheim_env`:

```yaml
valheim_env:
  PUID: "{{ valheim_user_id }}"
  PGID: "{{ valheim_group_id }}"
  PORT: "{{ valheim_port_a }}"
  NAME: "{{ valheim_name }}"
  WORLD: "{{ valheim_world }}"
  PASSWORD: "{{ valheim_password }}"
  TZ: "{{ ansible_nas_timezone }}"
  PUBLIC: "{{ valheim_public }}"
  AUTO_UPDATE: "{{ valheim_auto_update }}"
  AUTO_UPDATE_PAUSE_WITH_PLAYERS: "{{ valheim_auto_update_pause_with_players }}"
  AUTO_UPDATE_SCHEDULE: "{{ valheim_auto_update_schedule }}"
  AUTO_BACKUP: "{{ valheim_auto_backup }}"
  AUTO_BACKUP_SCHEDULE: "{{ valheim_auto_backup_schedule }}"
  AUTO_BACKUP_NICE_LEVEL: "{{ valheim_auto_backup_nice_level }}"
  AUTO_BACKUP_REMOVE_OLD: "{{ valheim_auto_backup_remove_old }}"
  AUTO_BACKUP_DAYS_TO_LIVE: "{{ valheim_auto_backup_days_to_live }}"
  AUTO_BACKUP_ON_UPDATE: "{{ valheim_auto_backup_on_update }}"
  AUTO_BACKUP_ON_SHUTDOWN: "{{ valheim_auto_backup_on_shutdown }}"
  AUTO_BACKUP_PAUSE_WITH_NO_PLAYERS: "{{ valheim_auto_backup_pause_with_no_players }}"
  UPDATE_ON_STARTUP: "{{ valheim_update_on_startup }}"
  ENABLE_CROSSPLAY: "{{ valheim_enable_crossplay }}"
  TYPE: "{{ valheim_type }}"
  SCHEDULED_RESTART: "{{ valheim_scheduled_restart }}"
  SCHEDULED_RESTART_SCHEDULE: "{{ valheim_scheduled_restart_schedule }}"
```

The container gets the `SYS_NICE` capability. In `defaults/main.yml`, `valheim_env` also holds commented-out lines for the webhook, preset, modifiers, key, mods and SteamCMD settings; uncomment them in your own copy of `valheim_env` to pass them. The docs page mentions `valheim_optional_env`, which the role does not read.

Application page: `website/docs/applications/gaming/valheim.md`.

Tests: a molecule scenario in `molecule/`.
