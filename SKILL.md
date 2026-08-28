---
name: 123pan
description: "Use and maintain the archived Bao-qing/123pan Python client for 123 网盘 file operations or upstream-source updates. Apply when a task needs this specific third-party client, not for generic cloud-storage work."
---

<!--
@file SKILL.md
@project 123panSkill
@module 123pan Codex skill entrypoint
@description Provides safe, source-grounded guidance for using and maintaining the archived Bao-qing/123pan client.
@logic Classifies requested 123 网盘 work, routes to the relevant local reference, preserves the immutable upstream baseline, and requires explicit authorization before account-changing operations.
@dependencies Archived upstream Python snapshot; requests~=2.31.0 for executing the archived client.
@index_tags 123pan, cloud-storage, upstream-archive, python-client
@author holic512
-->

# 123pan client

Use this skill for tasks that specifically need the archived Python client from
[Bao-qing/123pan](https://github.com/Bao-qing/123pan), such as inspecting its
behaviour, running a user-authorized 123 网盘 operation, or bringing in a newer
upstream snapshot. It is a third-party implementation of network calls, not an
official 123 网盘 SDK and not evidence that an endpoint remains supported.

The preserved baseline is under `archive/upstream-123pan/`. Treat that folder
as immutable source evidence. Do not edit files in it to implement a task;
make a working copy or create a separately dated upstream snapshot when an
update is required.

## Route the request

- Before using the account-facing client or changing its code, read
  [references/client-behavior.md](references/client-behavior.md). It identifies
  verified operations, index conventions, credential handling, and known
  security/compatibility constraints from this exact snapshot.
- Before refreshing or comparing upstream code, read
  [references/upstream-maintenance.md](references/upstream-maintenance.md) and
  `archive/UPSTREAM.md`. Preserve the baseline and license, record an
  identifiable upstream revision for every new snapshot, and compare changes
  before adopting them.

## Operating boundaries

1. Do not ask for, print, commit, or place usernames, passwords, Bearer tokens,
   share links, or private file metadata in this skill repository. The archived
   client can persist username, password, and authorization in cleartext JSON;
   use an ignored, user-controlled path outside the source snapshot when
   persistence is necessary.
2. Confirm the requested scope before account-changing operations. Uploading,
   creating directories or shares, deleting/trashing/restoring content, and
   overwriting local or remote files all change state. A request to inspect,
   list, or explain the client does not authorize those actions.
3. Use the archived `requirements.txt` only in an isolated execution environment
   or working copy. Its declared runtime dependency is `requests~=2.31.0`.
4. Keep archive maintenance separate from feature changes. A newer upstream
   release belongs in a new dated snapshot first; only then decide which
   behavior changes should be exposed through this skill or another project.
5. Report unverified network behavior as unverified. No live account, endpoint,
   or transfer test is implied by the archived source code alone.

## Expected result shape

When proposing or performing work with this client, state: the source snapshot
used, whether the operation is read-only or mutating, how secrets are kept out
of the workspace, the exact local changes made, and the validation actually
run. Preserve the upstream attribution and its archived license in every
redistribution or derivative that includes upstream code.
