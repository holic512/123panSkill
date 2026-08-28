# Upstream snapshot record

## Provenance

- **Upstream repository:** [Bao-qing/123pan](https://github.com/Bao-qing/123pan)
- **Archived source directory:** `archive/upstream-123pan/`
- **Original revision/tag/release:** 待确认 — the incoming source directory had
  no `.git` metadata and no revision value in its files.
- **Archive purpose:** retain the original source as a fixed comparison baseline
  while the repository root is used as a Codex skill package.

The files inside `upstream-123pan/` were moved without content edits during this
refactoring. Do not modify them in place. Keep upstream-derived code and its
license together when creating a newer archival snapshot or redistribution.

## Baseline manifest

SHA-256 values were calculated immediately before the files were moved into the
archive. Recalculate and compare them before an update if baseline integrity is
important.

| Path | SHA-256 |
| --- | --- |
| `.gitignore` | `42ccda6cbfabece4682b2f3529396830f8b696ec86355f575de826ad03739c7c` |
| `LICENSE` | `76c681a85bfb6257bce15ff8e08b8fede310c981776b2fa721547e85f8bbe9f6` |
| `README.md` | `758df673511ed0ee95bc4b79e11d11ab44608648e86f485b065f786dd309f52c` |
| `favicon.ico` | `f3b969604a9733985da732b5a6d09b8720c8093a74135a0c77c2eac6f7dd27fb` |
| `pack.sh` | `e7244b19ef022653388c92bd620b7e129a4571a016b2b6424c08b28f42890aa8` |
| `pan123_cli.py` | `52d347fa969182f8cdbce9fc9a042ecb6c200299890e1748cbc3611750a12ca4` |
| `pan123_core.py` | `22617e1534e398d9ee7fa6a75e25fd7e85ef7bc5534142e768da7f6232901a6e` |
| `requirements.txt` | `fabe482a7fb315b17c467d6d97d46cf03001d762233cdf0bf4d28cafc664b502` |
| `sign_py.py` | `6ef1a6665e8a013ffb091fe906c14ca9b2d2cf497e9f1e8167219b561003591f` |

## Archive rules

1. Preserve this initial directory as the immutable baseline; do not apply
   downstream fixes directly to it.
2. Put a newly fetched upstream version in a sibling dated directory, for
   example `archive/upstream-history/2026-08-28-<short-commit>/`.
3. Each new snapshot must include the upstream license and a short manifest with
   upstream URL, resolved commit/tag, retrieval date, and checksums.
4. Compare the new snapshot with this baseline before changing skill guidance or
   adopting code. Review authentication, request headers, endpoint usage,
   transfer behavior, and configuration persistence especially closely.
5. Never archive account configuration, access tokens, cookies, downloads, or
   user file data.

See [`../references/upstream-maintenance.md`](../references/upstream-maintenance.md)
for the detailed refresh and validation workflow.
