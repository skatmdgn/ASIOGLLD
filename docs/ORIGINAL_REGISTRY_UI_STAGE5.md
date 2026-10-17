# Stage 5: Original registry and dialog behavior (STATIC, original-only)

Original SHA-256: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. All addresses are RVAs. No modernization or replacement DLL.

## HKCU generic driver setting root

- Function `0x66B0` formats `%s\\%s` at 0x20850 from **`Software\\ASIO`** (0x20430) and **`Generic Low Latency ASIO Driver`** (0x201B0).
- `0x66EE` allocates a 0x118-byte helper object; `0x6767` loads the predefined `HKEY_CURRENT_USER` handle (0x80000001).
- `0x6773` invokes **`RegOpenKeyA`**; if no handle is obtained, `0x6795` invokes **`RegCreateKeyA`** on this root.
- Important **correction** to older documentation: this original's import table uses `RegOpenKeyA` (IAT 0x1E008) and `RegCreateKeyA` (IAT 0x1E010), **not** `RegOpenKeyExA`/`RegCreateKeyExA`. Value I/O is `RegQueryValueExA` (0x1E020) and `RegSetValueExA` (0x1E028).
- Other functions also access other registry roots; do not generalize this HKCU path to all settings or COM registration.

## Dialog dispatch

`0xB41C` supplies original handler **0xB6D0** to `DialogBoxIndirectParamA` at `0xB42E`. Handler explicitly branches by original Windows message:

| Message | Numeric | Control path |
|---|---:|---|
| `WM_DRAWITEM` | 0x002B | 0xC28D |
| `WM_INITDIALOG` | 0x0110 | 0xBEC9 |
| `WM_COMMAND` | 0x0111 | 0xB7E2 |
| `WM_VSCROLL` | 0x0115 | 0xB723 |

For `WM_COMMAND`: control ID **1** passes through 0xB9B7 and closes dialog with result 1; ID **2** uses 0xB9A8 and result 0. ID **1086** goes to 0xB8AF and toggles a working-settings bit 0, then refreshes controls; ID **1092** goes to 0xBAEA and toggles working-settings bit 1. The whole post-OK save/application state machine is not yet reconstructed.

The vertical trackbar path uses control ID **1090** (`0x442`), asks it for its position using `SendDlgItemMessageA`, and produces a buffer setting. When the user-defined flag is set, `0xB74D`/`0xB758` impose bounds **10–100**. Otherwise `0xB76B` looks up the table at `0x204B8`, whose exact three unsigned DWORD values are **[10,50,100]**. A GUI unit and actual stream frames must be established through all downstream paths before claiming exact timing semantics.

The separate event handlers, listbox selection, all failure behavior and immediate-vs-deferred persistence are **UNRESOLVED**. Resource IDs and command branches are not a complete GUI recreation.

## Byte-level reproducibility

- `tools/verify_registry_ui_stage5.py`: 30 pinned opcode sites plus buffer preset table, original SHA check, no external packages.
- The Stage 5 companion ZIP includes `original_registry_ui_audit.py`, which independently parses the PE import table, verifies **11/11** named imports and **30/30** opcode sites, and writes a machine-readable control-flow summary.
- Original-only static tests passed here; no original Windows debugger session, no replica, no parity, no optimizations.
