#!/usr/bin/env python3
"""A read-only copy of a mailbox, as a Maildir, for a local assistant to read.

Gmail is read through the Gmail API with a `gmail.readonly` token, so Google itself refuses
anything but reading. iCloud has no such API and is read over IMAP, but only ever with
EXAMINE (a read-only select) and BODY.PEEK (which does not mark anything as read); no
command that changes a mailbox is in this file.

The window of mail it copies widens one step a day, from a week to a year, so the first runs
are small and the history arrives gradually. Nothing it logs names a sender or a subject:
container logs are collected elsewhere, and a count is all they need.

Standard library only, so the image needs nothing installed.
"""
import base64
import imaplib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

# Fixed, never from configuration: an account can name its credentials, not where they go.
GMAIL_TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"
ICLOUD_HOST = "imap.mail.me.com"
ICLOUD_PORT = 993

# Days of mail to copy: a week first, then wider, one step a day.
WINDOWS = [7, 14, 28, 56, 112, 224, 365]
WIDEN_AFTER_SECONDS = 20 * 60 * 60
# Most messages copied per account per run, so a widening window is caught up gently.
MAX_PER_RUN = 500
NAME = re.compile(r"^[a-z0-9_-]{1,32}$")
SAFE_ID = re.compile(r"[^A-Za-z0-9._-]")


class ConfigError(Exception):
    pass


def load_accounts(path):
    with open(path, encoding="utf-8") as handle:
        accounts = json.load(handle)
    if not isinstance(accounts, list):
        raise ConfigError("accounts must be a list")
    names = set()
    for account in accounts:
        name = account.get("name", "")
        if not NAME.match(name):
            raise ConfigError("an account name must be 1-32 of a-z, 0-9, _ and -")
        if name in names:
            raise ConfigError("account names must be unique")
        names.add(name)
        kind = account.get("kind")
        needs = {
            "gmail": ("client_id", "client_secret", "refresh_token"),
            "icloud": ("user", "app_password"),
        }.get(kind)
        if needs is None:
            raise ConfigError("an account kind is gmail or icloud")
        for key in needs:
            if not str(account.get(key, "")).strip():
                raise ConfigError("account %s is missing %s" % (name, key))
    return accounts


# ---- the window -----------------------------------------------------------------------


def window_days(state, now):
    """The days of mail to copy now, widening one step once a step has been in place long
    enough. Returns (days, new_state)."""
    index = min(int(state.get("window_index", 0)), len(WINDOWS) - 1)
    widened_at = float(state.get("widened_at", now))
    if index < len(WINDOWS) - 1 and now - widened_at >= WIDEN_AFTER_SECONDS:
        index += 1
        widened_at = now
    return WINDOWS[index], {"window_index": index, "widened_at": widened_at}


def read_state(state_dir, name):
    try:
        with open(os.path.join(state_dir, name + ".json"), encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def write_state(state_dir, name, state):
    path = os.path.join(state_dir, name + ".json")
    temporary = path + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(state, handle)
    os.replace(temporary, path)


# ---- the Maildir ----------------------------------------------------------------------


class Maildir:
    """One account's Maildir. A message's file name is derived from its id at the source, so
    copying the same message twice is the same file, not a second one."""

    def __init__(self, root, account):
        self.base = os.path.join(root, account)
        for sub in ("tmp", "new", "cur"):
            os.makedirs(os.path.join(self.base, sub), mode=0o750, exist_ok=True)

    def _name(self, message_id):
        return SAFE_ID.sub("_", message_id)[:200]

    def has(self, message_id):
        name = self._name(message_id)
        return any(
            os.path.exists(os.path.join(self.base, sub, name)) for sub in ("new", "cur")
        )

    def add(self, message_id, raw):
        name = self._name(message_id)
        temporary = os.path.join(self.base, "tmp", name)
        with open(temporary, "wb") as handle:
            handle.write(raw)
        os.replace(temporary, os.path.join(self.base, "new", name))


# ---- Gmail ----------------------------------------------------------------------------


def _json(opener, request):
    with opener(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def gmail_access_token(account, opener):
    body = urllib.parse.urlencode(
        {
            "client_id": account["client_id"],
            "client_secret": account["client_secret"],
            "refresh_token": account["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode("ascii")
    request = urllib.request.Request(GMAIL_TOKEN_URL, data=body, method="POST")
    return _json(opener, request)["access_token"]


def _gmail_get(path, token, opener):
    request = urllib.request.Request(
        GMAIL_API + path, headers={"Authorization": "Bearer " + token}, method="GET"
    )
    return _json(opener, request)


def sync_gmail(account, maildir, since_epoch, opener, limit=MAX_PER_RUN):
    """Copies Gmail messages since a moment. Spam and Trash are left out, which is what the
    API's list does unless asked otherwise. Returns how many were added."""
    token = gmail_access_token(account, opener)
    query = urllib.parse.quote("after:%d" % int(since_epoch))
    added = 0
    page = ""
    while added < limit:
        path = "/messages?maxResults=500&q=" + query
        if page:
            path += "&pageToken=" + urllib.parse.quote(page)
        listing = _gmail_get(path, token, opener)
        for item in listing.get("messages", []):
            if added >= limit:
                break
            message_id = "gmail-" + item["id"]
            if maildir.has(message_id):
                continue
            raw = _gmail_get(
                "/messages/%s?format=raw" % urllib.parse.quote(item["id"]), token, opener
            )["raw"]
            maildir.add(message_id, base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
            added += 1
        page = listing.get("nextPageToken", "")
        if not page:
            break
    return added


# ---- iCloud ---------------------------------------------------------------------------


def _imap_date(since_epoch):
    return time.strftime("%d-%b-%Y", time.gmtime(since_epoch))


def sync_imap(account, maildir, since_epoch, connect, limit=MAX_PER_RUN):
    """Copies messages since a day over IMAP, read-only: every folder is opened with
    EXAMINE and every message fetched with BODY.PEEK. Returns how many were added."""
    folders = account.get("folders") or ["INBOX", "Sent Messages"]
    imap = connect()
    added = 0
    try:
        imap.login(account["user"], account["app_password"])
        for folder in folders:
            if added >= limit:
                break
            status, _ = imap.select('"%s"' % folder.replace('"', ""), readonly=True)
            if status != "OK":
                continue
            _, validity = imap.response("UIDVALIDITY")
            uid_validity = (validity[0] or b"0").decode("ascii", "replace")
            status, found = imap.uid("SEARCH", None, "SINCE", _imap_date(since_epoch))
            if status != "OK" or not found or not found[0]:
                continue
            slug = re.sub(r"[^a-z0-9]+", "-", folder.lower()).strip("-") or "folder"
            for uid in found[0].split():
                if added >= limit:
                    break
                uid = uid.decode("ascii")
                message_id = "%s.%s.%s" % (slug, uid_validity, uid)
                if maildir.has(message_id):
                    continue
                status, parts = imap.uid("FETCH", uid, "(BODY.PEEK[])")
                if status != "OK":
                    continue
                raw = next(
                    (p[1] for p in parts if isinstance(p, tuple) and len(p) == 2), None
                )
                if raw is None:
                    continue
                maildir.add(message_id, raw)
                added += 1
    finally:
        try:
            imap.logout()
        except Exception:  # noqa: BLE001 - leaving is best effort
            pass
    return added


# ---- one pass -------------------------------------------------------------------------


def run_once(config_path, maildir_root, state_dir, now=None, opener=None, connect=None):
    """One pass over every account. One account failing never stops the others, and what is
    reported is a kind of failure, never a message's content."""
    now = time.time() if now is None else now
    opener = opener or urllib.request.urlopen
    connect = connect or (lambda: imaplib.IMAP4_SSL(ICLOUD_HOST, ICLOUD_PORT))
    report = {}
    for account in load_accounts(config_path):
        name = account["name"]
        days, state = window_days(read_state(state_dir, name), now)
        since = now - days * 24 * 60 * 60
        maildir = Maildir(maildir_root, name)
        try:
            if account["kind"] == "gmail":
                added = sync_gmail(account, maildir, since, opener)
            else:
                added = sync_imap(account, maildir, since, connect)
            write_state(state_dir, name, state)
            report[name] = "%d new, window %d days" % (added, days)
        except Exception as error:  # noqa: BLE001 - one account must not stop the rest
            report[name] = "failed (%s)" % type(error).__name__
    return report


def main(argv):
    config = os.environ.get("MAIL_MIRROR_CONFIG", "/config/accounts.json")
    maildir = os.environ.get("MAIL_MIRROR_MAILDIR", "/maildir")
    state = os.environ.get("MAIL_MIRROR_STATE", "/state")
    every = int(os.environ.get("MAIL_MIRROR_EVERY_SECONDS", "300"))
    os.umask(0o027)
    while True:
        try:
            report = run_once(config, maildir, state)
            print("mail mirror: " + "; ".join("%s: %s" % kv for kv in sorted(report.items())))
        except ConfigError as error:
            print("mail mirror: configuration problem: %s" % error)
        sys.stdout.flush()
        if "--once" in argv:
            return 0
        time.sleep(every)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
