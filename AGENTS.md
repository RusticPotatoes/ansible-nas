# Working agreements

This is the owner's fork of ansible-nas, which builds the home lab. It builds on the owner's
global standards, kept in Endora:
<https://github.com/RusticPotatos/Endora/blob/develop/docs/standards.md> (test first,
behaviour in the owner's words, abstract only when needed, evidence over claims, nothing
personal in tracked files, and the rest). What follows is this repository's own. `CLAUDE.md`
is a link to this file.

## The repository

- **Base branch: `develop`.** Branch from it and propose back to it. `main` mirrors upstream
  and is never a base.
- **Keep upstream's conventions**, so changes stay easy to compare with upstream:
  - a new application starts from the `hello_world` template role, with everything it has
    (defaults, tasks, docs, molecule);
  - every variable of a role is named `<app>_*` (`<app>_enabled`, `<app>_data_directory`,
    `<app>_port`, ...);
  - one documentation page per application under `website/docs/applications/`;
  - a molecule scenario per role, whose `verify` shows the application starts and stops.
- **Lint is pinned** as the fork's CI pins it: ansible-lint 6.14.6 and yamllint 1.30.0.
  ansible-lint also runs this fork's own rules (`tests/lint_rules/`, loaded by `.ansible-lint`).
  Before submitting, the branch passes:
  - `ansible-playbook --syntax-check nas.yml -i tests/inventories/integration_testing`
  - `ansible-lint nas.yml`
  - `yamllint .`
  - `python3 -m unittest discover -s tests -p 'test_*.py'`

## How a change reaches the NAS

Read this before writing anything that runs on the NAS by itself (a timer, a script, a
service), or that changes a credential. A branch can look right, pass every lint and still fail
on the NAS, because these facts are not in any role. The first two are checked by this fork's
lint rules; the rest are for the branch's description.

1. **The playbook usually runs from another machine.** The owner applies a change from a laptop
   with `make run-remote`, over SSH (`inventories/remote.ini`); `make run` on the NAS is the
   other way. So `playbook_dir`, `inventory_file` and `inventory_dir` are the paths of whichever
   machine runs the playbook, often the laptop. Never bake them into a file, unit or script that
   stays on the NAS: give the role a variable for the NAS's own checkout instead. Rule
   `nas-controller-path`.
2. **Ansible's collections and roles are installed for the playbook's user**, not for the
   system: `ansible-galaxy` puts them in that user's `~/.ansible`, and `ansible.cfg` sets no
   `collections_path`. Anything on the NAS that runs `ansible-playbook` runs as that user: its
   systemd unit sets `User={{ ansible_nas_user }}`. As root it cannot load `community.docker`
   and the rest. Rule `nas-playbook-user`.
3. **The vault's password is not always on the NAS.** From a laptop it comes from the owner's
   keychain (`misc/vault-pass-keychain.sh`); `vault_password.txt` exists only in the NAS's own
   checkout. A job on the NAS that needs the vault reads it there, and the branch says so.
4. **A database takes its first credentials once.** MongoDB (`MONGODB_INITDB_*`), PostgreSQL
   (`POSTGRES_PASSWORD`) and MariaDB or MySQL root passwords are applied only when the data
   folder is empty. Changing such a variable later does not change the database, and every role
   that reads the same variable stops being able to log in (UniFi and LibreChat read
   `mongodb_password`). A branch that changes one says how to change it inside the database
   first. No test catches this: it depends on the data already there.
5. **A variable a role newly requires must already be set.** An `assert` that a value is
   present stops the whole play where it is missing, and the owner's values live where a branch
   never reads (below). A branch that makes a variable required names it, for the owner to set
   before merging.
6. **What is switched off here is no precedent.** Some upstream features are off on this NAS,
   and a role may still carry them. Don't copy a pattern from a role without asking whether it
   is on and works here.
7. **A dry run may not be quiet here.** Many roles pull their images (`pull: true`) and track
   `latest`, so `--check` can report changes when nothing drifted. Anything built on counting
   its changes needs a baseline from a real run first.

## The owner's values

**Never edit, cite or copy from `group_vars/`, `host_vars/` or any inventory, or anything
named for a vault.** They hold the owner's own settings. A branch that touches them is refused
whole. Use a role's `defaults/main.yml` and fictional examples instead; what a branch needs the
owner to set, it names in its description.

## What may change without asking

- **May change without asking:** a role's settings and defaults, documentation, the clean-up
  of a retired application, and lint fixes.
- **Needs a proposal first:** the network, the firewall, backups, credentials, storage, anything
  that deletes data, and anything that runs on the NAS by itself. Propose it to the wing's lead
  with the evidence (what you read, by receipt), and the owner gets a desk item; no branch is cut
  until the owner has said yes.

## Branches and commits

- **One branch per task**, named `hq/task-<N>-<slug>`, cut from `develop`, kept under about
  **200 changed lines**. A larger change is split into tasks.
- **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`),
  authored `Endora HQ`, each carrying the member trailer
  (`Made-by: Endora HQ (<members>) for task #N`).
- HQ never pushes on its own, never opens a pull request and never merges: the owner pushes an
  accepted branch and merges it on GitHub.

## A branch's description

Every branch's description says, in this order:

1. **What changed:** the files and roles, in a line or two each.
2. **Why:** the task, and what was found that called for it.
3. **What was run, with receipts:** each check and its result (syntax, ansible-lint, yamllint,
   this fork's tests, molecule where it ran), cited by receipt.
4. **How it reaches the NAS:** the tags to run; any variable or credential the owner must set
   first, by name; anything that will run on the NAS by itself, and as whom.
5. **How to roll back:** what to revert, and anything to redo on the lab after reverting.
