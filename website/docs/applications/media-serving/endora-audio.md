---
title: "Endora Audio"
---

Homepage: [https://github.com/RusticPotatos/endora-audio](https://github.com/RusticPotatos/endora-audio)

Endora Audio is a sound hub. Radio stations, Spotify and anything cast in over AirPlay are
sources. AirPlay speakers (HomePods, for one) and phones or browsers listening to a stream are
speakers. Each source-to-speaker wire has its own level, so a speaker plays a mix, and speakers
with the same wires play in sync. Named setups keep a set of wires. It has its own web page and
needs no account or cloud service, apart from the stations you add and Spotify.

Enabling the role runs up to four containers that share a pipes volume:

* `endora-audio`, the hub, with its page on port 8791. Its state is one JSON file in the
  `endora-audio-data` volume.
* `endora-audio-spotify`, a Spotify Connect receiver (stock
  [librespot](https://github.com/GioF71/librespot-docker)) on the host's network, which plays
  into the hub.
* `endora-audio-senders`, four stock [OwnTone](https://owntone.github.io/owntone-server/)
  instances that send the hub's groups to AirPlay 2 speakers, on the host's network. With the
  door off, they also run the classic AirPlay door, "Endora Mixer", on the NAS's address.
* `endora-audio-airplay` (optional), the AirPlay 2 door, "Endora Mixer", on a LAN address of its
  own. An Apple TV casting into it keeps lip-sync.

The senders cannot run beside the `owntone` role: both take the AirPlay clock's ports and the
speakers. The role refuses to start with both on.

## Usage

Set `endora_audio_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file
and run the playbook. Then read the hub's token:

```sh
docker exec endora-audio cat /token/token
```

Open `http://<your NAS>:8791` and paste the token. The page keeps it in that browser.

### Live mode and HTTPS

A phone can listen in two ways. *Listening* plays an MP3 stream and keeps going with the screen
locked. *Live* is a fraction of a second behind, and browsers allow it only on a secure page.
Over plain HTTP on the LAN the page offers Listening only. Everything else works.

For Live, give the page TLS **on the LAN only**: a reverse proxy on the LAN serving the hub under
a local name (a `home.arpa` record in Pi-hole, say) with a certificate your devices trust, such
as one from your own private CA. This role does not set that up yet.

Do **not** use `endora_audio_available_externally` for this. It publishes the page through
Traefik on your internet domain, so control of your speakers would be reachable from the
internet, guarded only by the token. It is off by default. Turning it on is a separate decision
about that risk.

### The AirPlay 2 door

The door needs a free LAN address, outside your router's DHCP pool and reserved there, and a fixed
MAC so the router keeps the reservation. It joins an existing macvlan network (the `pihole`
role's `pihole_macvlan` by default). The role checks that the network exists and never creates
one, because Docker allows only one macvlan network per subnet.

```yaml
endora_audio_airplay_enabled: true
endora_audio_airplay_ip: 192.168.1.10          # your free, reserved address
endora_audio_airplay_mac: "02:00:00:00:a2:01"  # any fixed, locally administered MAC
endora_audio_airplay_latency: 0.5              # seconds the door hands sound over early
```

The NAS itself cannot reach a macvlan address, so `ping` from the NAS fails. That is by design.
Other devices on the LAN reach it.

### Spotify

Pick "Endora" (`endora_audio_spotify_name`) in the Spotify app's devices once. It keeps its own
login after that, in the `endora-audio-spotify-login` volume. A Spotify Premium account is
required.

## Moving over from Endora's own sound containers

Endora ran the same hub as `endora-sound`, `endora-senders`, `endora-airplay2` and
`endora-spotify`, from its compose project. To keep every speaker, wire, setup and Spotify login,
point the role at Endora's volumes:

```yaml
endora_audio_data_volume: endora_endora-sound-data
endora_audio_token_volume: endora_endora-sound-token
endora_audio_pipes_volume: endora_endora-sound-pipes
endora_audio_secret_volume: endora_endora-sound-secret
endora_audio_senders_data_volume: endora_endora-senders-data
endora_audio_spotify_login_volume: endora_endora-spotify-login
```

Keep the door's address and MAC as they were, so your router and the Apple TV see the same
device. Back up the data volume first and stop the four old containers before running the role,
since the two sets cannot run together. Keep the old images until the new ones are proven. Then
turn off Endora's `sound` profile, and set its node's sound URL to the new hub if Endora is still
the remote: the token in the token volume is the same.

After moving over, each phone or browser opens the hub's page at a new address, so it no longer
knows which speaker it was. The page offers "This is me: …" with the stream speakers already
there: pick yours, and it keeps its wires and its live delay. The live delay applies in Live mode
only; music in Listening mode is not delayed.

## Specific configuration

* `endora_audio_port` (default `8791`): the hub's page and API.
* `endora_audio_version` (default `1.0.1`): the release of all three images (see the
  repository's releases for each one's digests).
* `endora_audio_senders_enabled`, `endora_audio_spotify_enabled` (default `true`): each part on
  or off.
* `endora_audio_*_volume`: the volumes, kept when the role is turned off.
* `endora_audio_*_memory`: each container's memory cap.
