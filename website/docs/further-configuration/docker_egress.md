---
title: "Locked-down Docker networks (docker_egress)"
---

This role now ships with Endora, as part of its `endora.homelab` Ansible collection, and is
documented there: [roles/docker_egress](https://github.com/RusticPotatos/Endora/tree/develop/deploy/ansible/collection/roles/docker_egress).

This repository pins the collection in `requirements.yml` and lists the role in `nas.yml` as
`endora.homelab.docker_egress`. Install it with:

```bash
ansible-galaxy collection install -r requirements.yml
```

Its settings and your vault values are unchanged.
