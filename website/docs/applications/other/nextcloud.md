---
title: "Nextcloud"
---

Homepage: [https://nextcloud.com](https://nextcloud.com)

## Usage

Set `nextcloud_enabled: true` in your `inventories/<your_inventory>/group_vars/nas.yml` file.

Tread carefully.

### Secrets

The database passwords have no default. Set them in your vault (`vault.yml`, encrypted with `ansible-vault`), and the role reads them from these variables:

```yaml
vault_nextcloud_sql_password: "<database user password>"
vault_nextcloud_sql_root_password: "<database root password>"
```

If either is unset or empty, the play stops before any container is started, with a message naming the variable to set.

External access may require that you manually configure your Fully Qualified Domain Name (FQDN) as a trusted domain within the application.  There is an environment variable set up for this in the "nextcloud task" which will most likely make manual configuration unnecessary.  If you get the following [screenshot](https://docs.nextcloud.com/server/14/admin_manual/installation/installation_wizard.html#trusted-domains) warning when trying to access nextcloud externally you'll need to manually set it up.

This can be accomplished in two commands.

```bash
# On the server where the docker containers are running
$ docker exec -it --user www-data nextcloud /bin/bash
$ php occ config:system:set trusted_domains INDEX_FOR_NEW_ENTRY_SEE_DOCS_LINK_BELOW --value=YOUR_FQDN_HERE --update-only
```

The above commands are documented in the administration guide for Nextcloud:

* [set array values](https://docs.nextcloud.com/server/14/admin_manual/configuration_server/occ_command.html#setting-an-array-configuration-value)

* [docker container docs, references environment variables](https://github.com/nextcloud/docker)
