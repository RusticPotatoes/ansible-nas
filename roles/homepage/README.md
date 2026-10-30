# homepage

Runs Homepage, a static, customizable application dashboard configured by YAML files and Docker labels, in a container. Other roles add themselves to it through `homepage.*` container labels.

Web interface: port `11111` (`homepage_port`), published to the container's port 3000.

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `homepage_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `homepage_available_externally` | `false` | Lets Traefik route `homepage_hostname`.`ansible_nas_domain` to it. |
| `homepage_data_directory` | `"{{ docker_home }}/homepage"` | Holds the templated config files, mounted at `/app/config`. |
| `homepage_hostname` | `"homepage"` | Subdomain Traefik uses when it is available externally. |
| `homepage_port` | `"11111"` | Host port published to the container's port 3000. |
| `homepage_container_name` | `"homepage"` | Name of the Docker container. |
| `homepage_image_name` | `"ghcr.io/gethomepage/homepage"` | Docker image. |
| `homepage_image_tag` | `"latest"` | Image tag. |
| `homepage_extra_volumes` | `[]` | Extra volumes, for example read-only mounts so the resources widget can show disk usage. |
| `homepage_memory` | `"1g"` | Container memory limit. |
| `homepage_title` | `Ansible-NAS Homepage` | Dashboard title, used in `homepage_settings_yaml`. |
| `homepage_locale` | `en-US` | Dashboard language, used in `homepage_settings_yaml`. |
| `homepage_settings_yaml` | see below | Written to `settings.yaml`. |
| `homepage_services_yaml` | see below | Written to `services.yaml`. |
| `homepage_widgets_yaml` | see below | Written to `widgets.yaml`. |
| `homepage_bookmarks_yaml` | see below | Written to `bookmarks.yaml`. |
| `homepage_allowed_hosts` | `"*"` | Passed as `HOMEPAGE_ALLOWED_HOSTS`. |

Default of `homepage_settings_yaml`:

```yaml
homepage_settings_yaml:
  title: "{{ homepage_title }}"
  language: "{{ homepage_locale }}"
  showStats: true
```

Default of `homepage_services_yaml`:

```yaml
homepage_services_yaml:
  - Networking:
      - Router:
          icon: asus-router
          href: "http://{{ ansible_nas_gateway }}/"
          description: Asus Router
```

Default of `homepage_widgets_yaml`:

```yaml
homepage_widgets_yaml:
  - search:
      provider: google # google, duckduckgo, bing, baidu, brave or custom
      focus: true # Optional, will set focus to the search bar on page load
      target: _blank # One of _self, _blank, _parent or _top
  - greeting:
      text_size: xl
      text: Ansible-NAS
  - resources:
      cpu: true
      memory: true
      cputemp: true
      uptime: true
      units: metric # only used by cpu temp
      refresh: 60000 # optional, in ms
```

Default of `homepage_bookmarks_yaml`:

```yaml
homepage_bookmarks_yaml:
  - Developer:
      - "Ansible-NAS":
          - abbr: AN
            href: https://ansible-nas.io/
      - Github:
          - abbr: GH
            href: https://github.com/
            icon: github
      - "Hacker News":
          - abbr: HN
            href: https://news.ycombinator.com/
  - Social:
      - Reddit:
          - abbr: RE
            href: https://reddit.com/
            icon: reddit
  - Entertainment:
      - YouTube:
          - abbr: YT
            href: https://youtube.com/
            icon: youtube
```

The tasks also write `docker.yaml` (the Docker socket, named after `ansible_nas_hostname`), mount the Docker socket, and restart the container when a config file changes. The container runs with an init process to reap the processes its health check leaves behind. The default services entry reads `ansible_nas_gateway`.

Application page: `website/docs/applications/dashboards/homepage.md`.
