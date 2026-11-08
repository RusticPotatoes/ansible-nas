# ebook2audiobook

Runs ebook2audiobook, which converts e-books into audiobooks with text-to-speech, in a container with its web interface, using the NVIDIA GPU by default.

Web interface: port `7860` (`ebook2audiobook_port`).

## Variables

Every variable in `defaults/main.yml`, with its default:

| Variable | Default | What it sets |
| --- | --- | --- |
| `ebook2audiobook_enabled` | `false` | Starts the container when `true`; removes it when `false`. |
| `ebook2audiobook_available_externally` | `false` | Lets Traefik route `ebook2audiobook_hostname`.`ansible_nas_domain` to it. |
| `ebook2audiobook_books_directory` | `"{{ books_root }}"` | E-books, mounted at `/app/ebooks`; also what the auto-conversion job scans. |
| `ebook2audiobook_audiobooks_directory` | `"{{ audiobooks_root }}"` | Audiobooks, mounted at `/app/audiobooks`. |
| `ebook2audiobook_download_directory` | `"{{ downloads_root }}"` | Downloads folder. Not used by the tasks yet. |
| `ebook2audiobook_data_directory` | `"{{ docker_home }}/ebook2audiobook"` | The app's own folder, parent of the folders below. |
| `ebook2audiobook_models_directory` | `"{{ ebook2audiobook_data_directory }}/models"` | Models, mounted at `/app/models`. |
| `ebook2audiobook_voices_directory` | `"{{ ebook2audiobook_data_directory }}/voices"` | Voices, mounted at `/app/voices`. |
| `ebook2audiobook_tmp_directory` | `"{{ ebook2audiobook_data_directory }}/tmp"` | Scratch space, mounted at `/app/tmp`. |
| `ebook2audiobook_processed_directory` | `"{{ ebook2audiobook_data_directory }}/processed"` | Success markers and the lock file of the auto-conversion job. |
| `ebook2audiobook_auto_convert_enabled` | `false` | Auto-conversion job (run by the `nas_maintenance` role): convert new e-books on a timer. |
| `ebook2audiobook_auto_convert_interval` | `"30m"` | Auto-conversion job (run by the `nas_maintenance` role): how often it runs. |
| `ebook2audiobook_auto_convert_script_path` | `"/usr/local/sbin/ebook2audiobook-auto-convert"` | Auto-conversion job (run by the `nas_maintenance` role): where its script is installed. |
| `ebook2audiobook_auto_convert_language` | `"eng"` | Auto-conversion job (run by the `nas_maintenance` role): `--language`. |
| `ebook2audiobook_auto_convert_device` | `"{{ 'gpu' if (ebook2audiobook_gpu_enabled \| bool) else 'cpu' }}"` | Auto-conversion job (run by the `nas_maintenance` role): `--device`, `gpu` or `cpu`. |
| `ebook2audiobook_auto_convert_output_format` | `"m4b"` | Auto-conversion job (run by the `nas_maintenance` role): `--output_format`. |
| `ebook2audiobook_auto_convert_output_directory` | `"/app/audiobooks/auto"` | Auto-conversion job (run by the `nas_maintenance` role): `--output_dir`, a path inside the container. |
| `ebook2audiobook_auto_convert_host_output_directory` | `"{{ ebook2audiobook_audiobooks_directory }}/auto"` | The same output folder on the host; the role creates it. |
| `ebook2audiobook_auto_convert_timeout` | `"0"` | Auto-conversion job (run by the `nas_maintenance` role): time limit of a run; `0` means none. |
| `ebook2audiobook_auto_convert_max_jobs` | `0` | Auto-conversion job (run by the `nas_maintenance` role): most conversions per run; `0` means no limit. |
| `ebook2audiobook_auto_convert_gpu_guard_enabled` | `"{{ ebook2audiobook_gpu_enabled }}"` | Auto-conversion job (run by the `nas_maintenance` role): skip new conversions while the GPU is busy. |
| `ebook2audiobook_auto_convert_gpu_max_utilization` | `90` | GPU guard: average utilisation (percent) at or above which it skips. |
| `ebook2audiobook_auto_convert_gpu_average_samples` | `3` | GPU guard: how many `nvidia-smi` samples to average. |
| `ebook2audiobook_auto_convert_gpu_average_sample_interval` | `5` | GPU guard: seconds between samples. |
| `ebook2audiobook_auto_convert_extensions` | see below | Auto-conversion job (run by the `nas_maintenance` role): file extensions it converts. |
| `ebook2audiobook_seed_builtin_voices` | `true` | Copy the image's built-in voices into the voices folder when it holds none (the bind mount hides them otherwise). |
| `ebook2audiobook_seed_voice_source` | `""` | Optional local audio file to turn into a custom voice (24 kHz mono wav); empty means none. |
| `ebook2audiobook_seed_voice_name` | `"Narrator"` | Name of that voice. |
| `ebook2audiobook_seed_voice_language` | `"eng"` | Language folder of that voice. |
| `ebook2audiobook_seed_voice_age` | `"adult"` | Age folder of that voice. |
| `ebook2audiobook_seed_voice_gender` | `"male"` | Gender folder of that voice. |
| `ebook2audiobook_seed_voice_safe_name` | `"{{ ebook2audiobook_seed_voice_name \| regex_replace('[^A-Za-z0-9_-]', '') }}"` | Voice name with unsafe characters removed, used in the file name. |
| `ebook2audiobook_seed_voice_directory` | `"{{ ebook2audiobook_voices_directory }}/{{ ebook2audiobook_seed_voice_language }}/{{ ebook2audiobook_seed_voice_age }}/{{ ebook2audiobook_seed_voice_gender }}"` | Folder the custom voice is written to. |
| `ebook2audiobook_seed_voice_path` | `"{{ ebook2audiobook_seed_voice_directory }}/{{ ebook2audiobook_seed_voice_safe_name }}_24000.wav"` | Path of the custom voice file. |
| `ebook2audiobook_user_id` | `"0"` | User the container runs as (`PUID`). |
| `ebook2audiobook_group_id` | `"0"` | Group the container runs as (`PGID`). |
| `ebook2audiobook_port` | `"7860"` | Host port published to the container's port 7860. |
| `ebook2audiobook_hostname` | `"ebook2audiobook"` | Subdomain Traefik uses when it is available externally. |
| `ebook2audiobook_container_name` | `"ebook2audiobook"` | Name of the Docker container. |
| `ebook2audiobook_image_name` | `"athomasson2/ebook2audiobook"` | Docker image. |
| `ebook2audiobook_image_version` | `"cuda12-v25.5.29"` | Image tag. |
| `ebook2audiobook_gpu_enabled` | `true` | Give the container the GPU (`ebook2audiobook_device_requests`). |
| `ebook2audiobook_nvidia_visible_devices` | `"all"` | `NVIDIA_VISIBLE_DEVICES`. |
| `ebook2audiobook_nvidia_driver_capabilities` | `"compute,utility"` | `NVIDIA_DRIVER_CAPABILITIES`. |
| `ebook2audiobook_device_requests` | see below | Docker device requests used when `ebook2audiobook_gpu_enabled` is on. |
| `ebook2audiobook_memory` | `8g` | Container memory limit. |

Default of `ebook2audiobook_auto_convert_extensions`:

```yaml
ebook2audiobook_auto_convert_extensions:
  - epub
  - mobi
  - azw3
  - pdf
  - txt
```

Default of `ebook2audiobook_device_requests`:

```yaml
ebook2audiobook_device_requests:
  - driver: nvidia
    count: -1
    capabilities:
      - ["gpu"]
```

The `ebook2audiobook_auto_convert_*` variables are read by the `nas_maintenance` role's `ebook2audiobook-auto-convert` job, which runs only when both `ebook2audiobook_enabled` and `ebook2audiobook_auto_convert_enabled` are on. The role's `files/Dockerfile` is not used by its tasks.

Application page: none yet under `website/docs/applications/`.

Tests: a molecule scenario in `molecule/`.
