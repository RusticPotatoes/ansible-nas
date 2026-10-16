---
title: "Mail Mirror"
---

This role now ships with Endora, as part of its `endora.homelab` Ansible collection, and is
documented there: [roles/mail_mirror](https://github.com/RusticPotatos/Endora/tree/develop/deploy/ansible/collection/roles/mail_mirror).

This repository pins the collection in `requirements.yml` and lists the role in `nas.yml` as
`endora.homelab.mail_mirror`. Install it with:

```bash
ansible-galaxy collection install -r requirements.yml
```

Its settings and your vault values are unchanged.
