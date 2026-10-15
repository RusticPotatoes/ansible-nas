---
title: "OwnTone (Spotify to HomePods)"
---

Homepage: [https://owntone.github.io/owntone-server/](https://owntone.github.io/owntone-server/)

OwnTone is a media server that can stream to AirPlay 2 speakers such as HomePods. This role pairs it with [librespot](https://github.com/librespot-org/librespot), an open source Spotify Connect receiver, so a Spotify Connect device (called `HomePods` by default) appears in the Spotify app. Anything you play on it is written to a named pipe that OwnTone reads and sends to the HomePods you choose.

Enabling the role runs two containers, both with host networking because AirPlay and Spotify Connect rely on mDNS:

* `owntone` from [`owntone/owntone`](https://github.com/owntone/owntone-container), the official OwnTone image. Its web interface is on port 3689.
* `owntone-spotify` from [`giof71/librespot`](https://github.com/GioF71/librespot-docker), which runs librespot with its pipe output.

Everything is stored under `{{ docker_home }}/owntone`:

* `config/owntone.conf` is created by OwnTone on first start.
* `cache/` holds the OwnTone database.
* `pipes/spotify` is the FIFO librespot writes to. OwnTone uses this directory as its library.
* `librespot/credentials.json` is the saved Spotify login.

A Spotify Premium account is required.

## Usage

Set `owntone_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file and run the playbook.

### One-time Spotify login

By default the receiver is not advertised on your network (`owntone_spotify_discovery: false`). Spotify only lists it on devices signed in to the account that logged it in, so guests on your Wi-Fi can't play to it. With discovery turned off, librespot needs a saved login, so the playbook doesn't start `owntone-spotify` until one exists.

To save the login, run this on the NAS, replacing `/path/to/docker_home` with your `docker_home`:

```bash
docker run --rm -it --network host \
  -v /path/to/docker_home/owntone/librespot:/data/system-cache \
  -e ENABLE_SYSTEM_CACHE=Y -e ENABLE_OAUTH=headless -e DISABLE_DISCOVERY=Y \
  -e BACKEND=pipe -e DEVICE=/dev/null \
  giof71/librespot:latest
```

1. Open the link it prints and sign in to Spotify with your own account.
2. Spotify then redirects to a `127.0.0.1` address that won't load. Copy the whole URL from the address bar and paste it into the terminal.
3. Once the log shows that it has authenticated, press Ctrl+C. The login is now saved in `librespot/credentials.json`.
4. Re-run the playbook. It will now start `owntone-spotify`.

If Spotify later revokes the login (for example after a password change), the receiver will stop working. Repeat these steps to fix it.

If you would rather let anyone on your network use the receiver and skip the login step, set `owntone_spotify_discovery: true`. Every Spotify Premium user on your network will then see it.

### Choosing which HomePods play

Open the OwnTone web interface at [http://ansible_nas_host_or_ip:3689](http://ansible_nas_host_or_ip:3689). Then open the speaker menu (the speaker icon at the bottom) and switch on the HomePods that should play, for example `Office` or `Living Room`. You can switch on several at once, and each has its own volume. OwnTone remembers your selection.

An Apple TV needs pairing once. When you switch it on in the speaker menu, the TV shows a 4-digit code and the switch fails with `400 Bad Request`, because the speaker menu doesn't ask for the code. Open **Settings → Remotes & Outputs**, type the code under the Apple TV and press **Verify**. OwnTone saves the pairing in its cache directory, so you only do this once. After that, the Apple TV switches on like any other speaker.

If a HomePod is listed but won't play, open the Home app and go to Home Settings → Speakers & TV. Set *Allow Speaker & TV Access* to *Anyone on the Same Network* or *Everyone*, or enter the PIN that OwnTone asks for.

### Playing Spotify

In any Spotify app on the same account, open the device picker and choose `HomePods`. When audio arrives on the pipe, OwnTone starts the `spotify` pipe automatically on the selected HomePods.

Both apps have a volume control. Use OwnTone or the HomePods for the room volume. The Spotify slider starts at 100% (`owntone_spotify_initial_volume`) and scales the signal before it reaches OwnTone.

### Delay

AirPlay 2 buffers audio. Expect about 2-3 seconds between pressing play, pause or skip in Spotify and hearing the change on the HomePods. This is normal and can't be tuned away.

### Troubleshooting

* HomePods don't show up in OwnTone. OwnTone runs its own Avahi daemon in the container. If the NAS also runs `avahi-daemon`, both share mDNS on port 5353 and discovery can be unreliable. Check the container logs with `docker logs owntone`.
* A HomePod is listed but switching it on fails with `400 Bad Request`, and `docker logs owntone` shows `Response to GET /info (probe) ... (403 Forbidden)`. HomePod OS 27 rejects AirPlay clients whose User-Agent doesn't start with `AirPlay/`. The role sets `user_agent` in the `general` section of `owntone.conf` to `owntone_airplay_user_agent` to fix this. If you edited that line by hand, re-run the playbook.
* Nothing plays. Check `docker logs owntone-spotify` and confirm that `pipes/spotify` is a FIFO (`ls -l` shows a leading `p`).

## Configuration

* `owntone_spotify_device_name`: the name shown in Spotify. The default is `HomePods`.
* `owntone_spotify_bitrate`: `96`, `160` or `320` (the default).
* `owntone_airplay_user_agent`: the User-Agent OwnTone sends to AirPlay speakers. The default is `AirPlay/999.0.0`, which HomePod OS 27 accepts.
* `owntone_spotify_discovery`: whether to advertise the receiver to everyone on the LAN. The default is `false`.
* `owntone_available_externally`: whether to expose the OwnTone web interface through Traefik at `owntone.<your domain>`. The default is `false`. The interface has no password, so leave this off unless you add one in `owntone.conf`.
