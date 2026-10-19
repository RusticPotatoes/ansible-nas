#!/bin/sh
# The vault password from the macOS login Keychain, for --vault-password-file: no file on disk.
# Add it once (it prompts, so it is never on the command line or in shell history):
#   security add-generic-password -a "$USER" -s "ansible-nas vault" -w
exec security find-generic-password -a "$USER" -s "ansible-nas vault" -w
