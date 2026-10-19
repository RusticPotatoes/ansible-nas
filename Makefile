INVENTORY ?= inventories/inventory.ini
PLAYBOOK ?= nas.yml
VAULT_FILE ?= vault.yml
VAULT_PASSWORD_FILE ?= vault_password.txt

.PHONY: deploy syntax tags run run-remote venv

# Where the ansible commands come from: the system's (empty, on the NAS) or the venv's.
BIN ?=
PLAY = $(BIN)ansible-playbook -i $(INVENTORY) $(PLAYBOOK) -e @$(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)

# One step for a change: pull, install the pinned roles and collections, a dry run of TAGS
# showing what would change, then apply only on a yes. EXTRA passes more flags; by default -K,
# so sudo's password is asked for (once for the dry run, once for the real one).
#   make run TAGS=openbao,pihole
EXTRA ?= -K
run:
	@test -n "$(TAGS)" || { echo "usage: make run TAGS=openbao,pihole"; exit 1; }
	git pull --ff-only
	$(BIN)ansible-galaxy collection install -r requirements.yml --force
	$(BIN)ansible-galaxy role install -r requirements.yml
	$(PLAY) --tags "$(TAGS)" --check --diff $(EXTRA)
	@printf 'Apply these changes? [y/N] '; read answer; \
		[ "$$answer" = y ] || [ "$$answer" = Y ] || { echo "Nothing applied."; exit 1; }
	$(PLAY) --tags "$(TAGS)" $(EXTRA)

# The same from another machine (a laptop) over SSH: the NAS's ansible version from a venv here,
# the encrypted vault.yml copied here (git-ignored), its password from the macOS Keychain.
#   make run-remote TAGS=openbao,pihole
run-remote: venv
	@test -f $(VAULT_FILE) || { echo "copy the encrypted vault.yml here first: scp nas.home.arpa:ansible-nas/vault.yml ."; exit 1; }
	$(MAKE) run INVENTORY=inventories/remote.ini VAULT_PASSWORD_FILE=misc/vault-pass-keychain.sh BIN=.venv/bin/

# ansible-core as the NAS runs it (requirements-ansible.txt), in .venv, made once, on the NAS's
# Python (3.12: ansible-core 2.16 does not run on newer ones).
PYTHON ?= python3.12
venv: .venv/bin/ansible-playbook
.venv/bin/ansible-playbook: requirements-ansible.txt
	$(PYTHON) -m venv .venv
	.venv/bin/pip install --quiet -r requirements-ansible.txt
	@touch $@

deploy:
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK) -e @$(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)

syntax:
	ansible-playbook -i $(INVENTORY) --syntax-check $(PLAYBOOK) -e @$(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)

tags:
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK) -e @$(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE) --tags "$(TAGS)"
decrypt:
	ansible-vault decrypt $(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)

encrypt:
	ansible-vault encrypt $(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)
