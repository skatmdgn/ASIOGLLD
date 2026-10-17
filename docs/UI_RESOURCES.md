# Original UI resource reconstruction — Stage 4

Direct inspection of the original PE `.rsrc` resource directory using a custom Windows dialog-template parser, **not** a reconstructed running user interface.

- **11 resource leaf entries**: 2 bitmaps, 7 dialog templates, 1 version entry and 1 manifest entry.
- Dialog resource ID 129: 3 controls, title 'Generic Low Latency ASIO Driver' (neutral language).
- Main dialog resource ID 130: **28 controls** per language variation.
- Main dialog templates appear in neutral English (resource language 0) and translated resources with language identifiers 16, 1031, 1036, 1041, 3082 (Italian, German, French, Japanese, Spanish). The parser successfully read all seven dialog templates, with **zero parsing exceptions**.

### Main dialog IDs (original resource, language 0)

| ID | Class or function | Literal caption if present |
|---:|---|---|
| 1086 | BUTTON | Allow ASIO host application to take exclusive control of selected port configuration |
| 1090 | msctls_trackbar32 | buffer-size slider |
| 1109 | SysListView32 | output ports |
| 1110 | SysListView32 | input ports |
| 1117 | BUTTON | Help |
| 1118 | BUTTON | User definable |
| 1119 | EDIT | numeric buffer display/input |
| 1 | BUTTON | OK |
| 2 | BUTTON | Cancel |

The `SysListView32` names are resolved from Windows dialog standard class ordinal **0x83** (LISTBOX) in the raw record? Original parser reports class ordinal 131, which is Windows LISTBOX, **not SysListView32**. Therefore the **correct raw class** is ordinal 131, and no control should be relabeled as SysListView32 without runtime proof. For ID 1109/1110 the original ordinal is 131. Button ordinal 128. ID 1119 original edit ordinal 129.

### Important distinction

Resource parsing reveals control IDs, labels and layout. It **does not prove** the original command handlers, enabled/disabled behavior, callback/registry link or runtime state changes. These require dialog-procedure analysis and runtime testing.

The Stage 4 analysis ZIP contains a stricter dialog-template parser and structured resource results; `tools/recovery_v4.py` provides a lighter reproducible resource directory audit.
