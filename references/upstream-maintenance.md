# Upstream maintenance workflow

Use this workflow when refreshing or reviewing code from
[Bao-qing/123pan](https://github.com/Bao-qing/123pan). The baseline archive
has unknown original Git revision, so its content hashes in `archive/UPSTREAM.md`
are the primary identity for this particular copy.

## Preserve the comparison baseline

`archive/upstream-123pan/` is evidence, not a development directory. Do not
edit, format, delete, or replace files in it. Do all source retrieval and
experimentation in a separate staging directory. Do not put credentials,
tokens, runtime JSON, downloads, build products, or user data into either the
archive or a new source snapshot.

## Refresh procedure

1. Obtain the desired upstream state from the repository URL and record an
   immutable identifier: preferably the resolved commit SHA, plus tag/release
   when applicable. If no immutable identifier is available, mark the source
   as **待确认** instead of inventing a version.
2. Inspect the upstream license and README before copying code. Preserve the
   license text associated with that revision; do not assume the license remains
   unchanged just because this baseline has one.
3. Diff the staging source against `archive/upstream-123pan/`. Separate
   mechanical changes from behavior changes, and inspect at least login/header
   construction, request URLs, upload multipart workflow, download redirect
   handling, and config persistence.
4. If retaining the retrieved source, copy it unchanged into a new sibling
   directory named `archive/upstream-history/YYYY-MM-DD-<short-commit>/`. Add a
   small manifest there with repository URL, full revision/tag, retrieval date,
   copied-file hashes, and license location.
5. Update the root README only when source provenance, archived capability, or
   security notes materially change. Update `references/client-behavior.md`
   only after code evidence supports the new statement. The original baseline
   manifest must remain intact.
6. Apply any downstream adaptation outside the archive, in a clearly named
   working module or project. Keep its tests and changelog separate from the
   upstream snapshot so a later diff remains meaningful.

## Minimum validation

For an archival-only refresh, recalculate SHA-256 hashes, compare file lists,
validate the skill entrypoint, and compile the archived Python modules. For a
behavioral update, add targeted tests or controlled, user-authorized checks for
the changed behavior. A syntax check does not validate credentials, endpoints,
or transfers.

## Review checklist

- [ ] Upstream URL and exact revision/tag are recorded.
- [ ] Upstream license and attribution accompany the snapshot.
- [ ] No credential JSON, cookie, token, download, or build output was copied.
- [ ] Diff review notes any change to authentication, headers, endpoints,
  redirect/TLS handling, destructive actions, or overwrite defaults.
- [ ] Baseline `archive/upstream-123pan/` still matches its recorded hashes.
- [ ] README source attribution still links to
  `https://github.com/Bao-qing/123pan`.
