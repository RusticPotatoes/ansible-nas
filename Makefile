INVENTORY ?= inventories/inventory.ini
PLAYBOOK ?= nas.yml
VAULT_FILE ?= vault.yml
VAULT_PASSWORD_FILE ?= vault_password.txt

.PHONY: deploy syntax tags

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
