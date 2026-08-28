# Archived client behavior

This reference is derived from the current archived source, not from official
123 网盘 documentation. It describes the snapshot in
`archive/upstream-123pan/` and must not be read as a guarantee that a service
endpoint or protocol continues to work.

## Components and contracts

| Component | Evidence | Responsibility |
| --- | --- | --- |
| `Pan123Core` | `pan123_core.py` | Authentication, headers, API requests, directory state, file metadata, sharing, trash/restore, upload negotiation, and download-link resolution |
| `Pan123Tool` | `pan123_core.py` | JSON configuration persistence and local file/folder downloads |
| `Pan123CLI` | `pan123_cli.py` | Interactive command parsing and user-facing progress output |
| `sign_py.py` | `sign_py.py` | Standalone signing helper; it is not imported by the archived core or CLI |

`Pan123Core` public methods return dictionaries shaped as
`{"code": int, "message": str, "data": Any}`. In the archived source, `0`
indicates ordinary success; `1` is a local download-file conflict and `5060`
is the reported duplicate-name upload conflict. The CLI uses one-based list
numbers, while `Pan123Core` methods that accept an item index use zero-based
indexes.

## Confirmed operation paths

| Category | Methods in the snapshot | State effect |
| --- | --- | --- |
| Login/session | `load_config`, `login`, `check_login`, `init_login_state`, `logout`, `clear_account`, `get_user_info` | Login and config writes can expose or alter credentials/token state |
| Browse | `list_dir`, `list_dir_all`, `refresh`, `load_more`, `cd`, `cd_up`, `cd_root`, `get_folder_details` | Reads remote metadata and updates in-memory navigation state |
| Remote file changes | `mkdir`, `trash`, `trash_by_index`, `restore`, `share`, `upload_file`, `upload_directory` | Creates, changes, shares, trashes, restores, or uploads remote content |
| Download | `get_download_url`, `get_item_download_url`, `Pan123Tool.download_file`, `download_directory`, `download_url` | Reads remote content; may create, overwrite, or remove local files depending on options |
| Configuration | `Pan123Tool.load_config_from_file`, `save_config_to_file`, `set_protocol` | Reads/writes configuration or alters request-header behavior |

The core supports `android` and `web` protocol modes. It builds mode-specific
headers and uses a direct API base URL. The initial default is `android`.
`Pan123Tool.save_config_to_file()` serializes `userName`, `passWord`,
`authorization`, device fields, and protocol as cleartext JSON.

## Transfer behavior that affects implementation decisions

- `upload_file` computes an MD5 and sends an upload request. If the service
  reports reuse it finishes without a multipart transfer; otherwise it uploads
  5 MiB parts to pre-signed URLs, asks the service to merge them, then confirms
  completion.
- `upload_directory` recursively creates remote directories, then transfers
  files. Its `duplicate` argument is `0` for a reported conflict, `1` for
  overwrite, and `2` for keeping both according to the source docstring.
- `download_file` and `download_directory` can overwrite or skip an existing
  local file. The default returns a conflict instead of overwriting. Downloads
  use a temporary `.123pan` suffix and rename the file after completion.
- A directory passed to the download-link resolver uses the service's batch
  download path; `Pan123Tool.download_directory` instead recursively fetches
  individual child items.

## Constraints and risks

1. **Unofficial, compatibility-sensitive protocol.** The archive defines direct
   endpoint paths and client-emulation headers. These are implementation facts,
   not official API documentation. Do not claim their current validity without a
   user-authorized, controlled test.
2. **Secret persistence.** The configuration writer stores password and Bearer
   authorization in cleartext. Do not create it inside the skill repository,
   commit it, or echo it to a user.
3. **TLS verification is disabled in one path.**
   `Pan123Core.get_item_download_url()` calls `requests.get(..., verify=False)`
   while resolving a redirect and disables related warnings. Treat this as a
   security issue to assess and test before any production or sensitive use; do
   not normalize it as a safe default.
4. **Mutating operations need scope confirmation.** Upload, create-directory,
   share, trash, restore, and overwrite options have real remote or local side
   effects. Explain the target and conflict strategy before proceeding.
5. **No automated tests are present in this snapshot.** Python syntax can be
   checked locally, but account, protocol, and transfer behavior remain
   unverified until exercised against a user-authorized test account.
