#!/usr/bin/env python3
"""librespot --onevent hook: pass the playing track's details to OwnTone.

OwnTone reads shairport-sync style metadata from a FIFO named after the audio
pipe with a ".metadata" suffix. librespot runs this script on every player
event with the details in environment variables.
"""
import base64
import errno
import os
import struct
import sys
import time
import urllib.request

PIPE = os.environ.get("OWNTONE_METADATA_PIPE", "/pipes/spotify.metadata")
# OwnTone only opens the metadata pipe while the audio pipe is playing, which
# can start shortly after librespot reports the new track.
WAIT_SECONDS = 10


def item(kind, code, data=b""):
    out = "<item><type>%s</type><code>%s</code><length>%d</length>\n" % (
        kind.encode().hex(),
        code.encode().hex(),
        len(data),
    )
    if data:
        out += '<data encoding="base64">\n%s</data>' % base64.b64encode(data).decode()
    return out + "</item>\n"


def cover(urls):
    for url in urls.splitlines():
        try:
            with urllib.request.urlopen(url.strip(), timeout=5) as reply:
                return reply.read()
        except Exception:
            continue
    return b""


def track_items(env):
    items = [item("ssnc", "mdst")]
    items.append(item("core", "minm", env.get("NAME", "").encode()))
    artists = ", ".join(a for a in env.get("ARTISTS", env.get("SHOW_NAME", "")).splitlines() if a)
    items.append(item("core", "asar", artists.encode()))
    items.append(item("core", "asal", env.get("ALBUM", "").encode()))
    duration = env.get("DURATION_MS", "")
    if duration.isdigit():
        items.append(item("core", "astm", struct.pack(">I", int(duration))))
    items.append(item("ssnc", "mden"))
    picture = cover(env.get("COVERS", ""))
    if picture:
        items.append(item("ssnc", "pcst"))
        items.append(item("ssnc", "PICT", picture))
        items.append(item("ssnc", "pcen"))
    return "".join(items).encode()


def open_pipe(path, wait):
    deadline = time.monotonic() + wait
    while True:
        try:
            # Non-blocking so a missing reader never hangs librespot.
            return os.open(path, os.O_WRONLY | os.O_NONBLOCK)
        except OSError as err:
            if err.errno not in (errno.ENXIO, errno.ENOENT) or time.monotonic() >= deadline:
                return None
            time.sleep(0.5)


def send(payload, path=PIPE, wait=WAIT_SECONDS):
    fd = open_pipe(path, wait)
    if fd is None:
        return False
    try:
        os.set_blocking(fd, True)
        os.write(fd, payload)
        return True
    finally:
        os.close(fd)


def main(env):
    if env.get("PLAYER_EVENT") != "track_changed":
        return 0
    # Write before exiting: a forked writer is killed once this process exits.
    # librespot runs event hooks off the audio path, so the short wait for
    # OwnTone's reader doesn't delay playback.
    send(track_items(env))
    return 0


if __name__ == "__main__":
    sys.exit(main(os.environ))
