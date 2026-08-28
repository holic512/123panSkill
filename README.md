# 123pan Codex Skill

This repository packages a Codex skill around an archived Python client for
123 网盘. It separates the **skill instructions** from the **unmodified upstream
source snapshot**, so later upstream changes can be reviewed and adopted without
losing the original baseline.

## Source and attribution

Original upstream project: [Bao-qing/123pan](https://github.com/Bao-qing/123pan)

The original files are preserved in
[`archive/upstream-123pan`](archive/upstream-123pan), including the upstream
README, build script, dependency file, icon, `.gitignore`, and license. The
archived license is titled **“MIT License with No Commercial Use”**; its exact
terms are retained in
[`archive/upstream-123pan/LICENSE`](archive/upstream-123pan/LICENSE). This
skill repository is not affiliated with, endorsed by, or an official SDK of
123 网盘 or the upstream author.

The incoming snapshot did not contain Git metadata, so its original commit,
tag, and release version are **待确认**. File hashes and the archival policy are
recorded in [`archive/UPSTREAM.md`](archive/UPSTREAM.md).

## Layout

```text
.
├── SKILL.md                         # Codex skill entrypoint
├── README.md                        # This package guide and attribution
├── references/
│   ├── client-behavior.md           # Code-verified operation and risk notes
│   └── upstream-maintenance.md      # Safe upstream refresh workflow
└── archive/
    ├── UPSTREAM.md                  # Snapshot manifest and integrity record
    └── upstream-123pan/             # Byte-preserved source baseline
        ├── pan123_core.py           # API client and transfer logic
        ├── pan123_cli.py            # Interactive CLI
        ├── sign_py.py               # Request-signing helper
        ├── requirements.txt         # requests~=2.31.0
        └── ...                      # Upstream README, license, build assets
```

To make the package discoverable by Codex, place or symlink this whole directory
under your local Codex skills directory using the folder name `123pan`. Do not
copy only `SKILL.md`: the skill relies on its adjacent archive and references.

## What the archived client implements

The source implements an interactive CLI and a Python API layer for:

| Area | Code-verified capability |
| --- | --- |
| Authentication | Load credentials/token, sign in, validate session, sign out |
| Browsing | List directories, paginate, enter/leave folders, retrieve user information |
| Transfer | Obtain download URLs, download files/folders, upload files/folders with multipart upload |
| File actions | Create folders, create shares, trash, restore, and inspect recycle-bin contents |
| Configuration | Persist username, password, authorization, device fields, and protocol in JSON |

The implementation talks to service endpoints directly and emulates web or
Android request headers. It should therefore be considered compatibility-sensitive
third-party code, rather than a stable API contract. See
[`references/client-behavior.md`](references/client-behavior.md) before running
it or adapting its behavior.

## Using the skill

Invoke `$123pan` when the work explicitly concerns this archived client. The
skill will first distinguish read-only inspection from account-changing actions,
keep credentials outside this repository, and point to the relevant source
evidence. Typical requests include:

- “Use `$123pan` to explain how the archived client performs multipart upload.”
- “Use `$123pan` to compare a newer upstream revision against the archived
  baseline.”
- “Use `$123pan` to prepare a locally isolated, user-authorized download
  workflow without storing credentials in the repository.”

Listing or explaining code does not authorize uploads, deletions, shares,
restores, overwrites, or credential persistence. Those operations need an
explicitly scoped request.

## Updating from upstream

The baseline at `archive/upstream-123pan/` is deliberately immutable. Do not
overwrite it when checking [Bao-qing/123pan](https://github.com/Bao-qing/123pan)
for updates. Fetch a new source tree into a staging location, identify its
commit/tag, compare it with this baseline, then archive it under a new dated
directory before deciding whether to incorporate its behavior. The full,
repeatable process and required evidence are in
[`references/upstream-maintenance.md`](references/upstream-maintenance.md).

## Security and compatibility notes

- The archived configuration writer stores the username, password, and Bearer
  authorization in plain JSON. Keep any runtime configuration outside the
  repository and out of logs.
- The download-URL resolver disables TLS certificate verification for one
  redirect request in this snapshot. Treat that behavior as a security concern
  to assess during any implementation or upstream update; it has not been
  executed or accepted by this refactoring.
- No live network operation has been run while creating this skill. Endpoint
  availability, login behavior, and transfer compatibility remain unverified.

## Validation performed for this refactoring

The final validation records the archived Python syntax check, skill frontmatter
validation, and SHA-256 comparison against the snapshot manifest. Results are
reported with the refactoring handoff rather than assumed from these documents.
