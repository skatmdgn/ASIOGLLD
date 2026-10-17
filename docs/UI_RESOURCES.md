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
| 1109 | LISTBOX (ordinal 131) | output port selector |
| 1110 | LISTBOX (ordinal 131) | input port selector |
| 1117 | BUTTON | Help |
| 1118 | BUTTON | User definable |
| 1119 | EDIT (ordinal 129) | numeric buffer field |
| 1 | BUTTON | OK |
| 2 | BUTTON | Cancel |

For IDs 1109 and 1110, the binary class value is ordinal **131**, the standard Windows **LISTBOX** class. Button class ordinal is 128; ID 1119's EDIT class ordinal is 129. Actual runtime behavior still needs investigation.

### Important distinction

Resource parsing reveals control IDs, labels and layout. It **does not prove** the original command handlers, enabled/disabled behavior, callback/registry link or runtime state changes. These require dialog-procedure analysis and runtime testing.

The Stage 4 analysis ZIP contains a stricter dialog-template parser and structured resource results; `tools/recovery_v4.py` provides a lighter reproducible resource directory audit.
