# Static code coverage ledger — revised Stage 4

**Directly reproduced on the original** with `tools/recovery_v4.py`:

| Category | Count | Interpretation |
|---|---:|---|
| x64 .pdata unwind ranges | **590** | NOT a count of logical C++ functions |
| objdump-decoded instruction rows | **33,194** | linear disassembly rows, not verified CFG coverage |
| Distinct in-.text direct CALL targets, all disassembly | **305** | not necessarily distinct source functions |
| Direct CALL targets *outside every* .pdata range | **67** | leaf/helper/thunk candidates needing manual review |
| PE resource leaf entries | **11** | raw Windows resource entries |
| Dialog templates | **7** | one ID 129 + six locale variants of ID 130 |

The previous **304** distinct direct CALL targets was from the older analysis, which counted calls owned by a recognized .pdata range only. The Stage 4 scanner considers the whole disassembled .text region, yielding **305**. The 67 outside-unwind candidates are consistent between scanners. The old count is not a second independent verification of complete coverage.

**Do not equate 67 with 67 newly confirmed functions.** Some targets are jump stubs/runtime helpers. Indirect COM calls, vtables, jump tables, exception handlers and unanalyzed data/control flow remain unresolved.

The full 67-address triage list is in Stage 4 ZIP `reports/coverage.json`. Tests performed are static only; no running original/replica parity yet.
