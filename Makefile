INVENTORY ?= inventories/inventory.ini
PLAYBOOK ?= nas.yml
VAULT_FILE ?= vault.yml
VAULT_PASSWORD_FILE ?= vault_password.txt

.PHONY: deploy syntax tags run

PLAY = ansible-playbook -i $(INVENTORY) $(PLAYBOOK) -e @$(VAULT_FILE) --vault-password-file $(VAULT_PASSWORD_FILE)

# One step for a change: pull, install the pinned roles and collections, a dry run of TAGS
# showing what would change, then apply only on a yes. EXTRA passes more flags; by default -K,
# so sudo's password is asked for (once for the dry run, once for the real one).
#   make run TAGS=openbao,pihole
EXTRA ?= -K
run:
	@test -n "$(TAGS)" || { echo "usage: make run TAGS=openbao,pihole"; exit 1; }
	git pull --ff-only
	ansible-galaxy collection install -r requirements.yml --force
	ansible-galaxy role install -r requirements.yml
	$(PLAY) --tags "$(TAGS)" --check --diff $(EXTRA)
	@printf 'Apply these changes? [y/N] '; read answer; \
		[ "$$answer" = y ] || [ "$$answer" = Y ] || { echo "Nothing applied."; exit 1; }
	$(PLAY) --tags "$(TAGS)" $(EXTRA)

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
