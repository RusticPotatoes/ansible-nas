# route53_ddns

Runs ddns-route53 in a container, which keeps an AWS Route53 `A` record pointed at your dynamic IP address, so the NAS can be reached under its domain from outside.

No port: the container only calls the AWS API on a schedule.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `route53_ddns_enabled` | `false` | Meant to turn the updater on; the tasks check `route53_enabled` instead (see below). |
| `route53_data_directory` | `"{{ docker_home }}/route53_ddns"` | Holds the generated `ddns-route53.yml`, mounted at `/etc/ddns-route53/ddns-route53.yml`. |
| `route53_key_id` | `"{{ mandatory }}"` | AWS access key ID. Required: set it in your own vars, never in git. |
| `route53_secret_key` | `"{{ mandatory }}"` | AWS secret key. Required: set it in your own vars, never in git. |
| `route53_hosted_zone_id` | `"{{ mandatory }}"` | ID of the Route53 hosted zone to update. Required. |
| `route53_host` | `"*.{{ ansible_nas_domain }}"` | Record name to update. |
| `route53_ttl` | `600` | TTL of the record, in seconds. |
| `route53_schedule` | `"*/30 * * * *"` | Cron schedule for checking and updating (`SCHEDULE`). |
| `route53_memory` | `512MB` | Container memory limit. |
| `route53_container_name` | `"route53-ddns"` | Name of the Docker container. |
| `route53_image_name` | `"crazymax/ddns-route53"` | Docker image. |
| `route53_image_version` | `"latest"` | Image tag. |

The tasks start and stop the container on `route53_enabled`, which has no default here, not on `route53_ddns_enabled`. Set `route53_enabled` too, or the role fails on the undefined variable. The container is recreated when the config file changes.

Application page: `website/docs/applications/system-tools/route53_ddns.md`.

Tests: a molecule scenario in `molecule/`.
