# Batch 9 checkpoint (original-only)

Original `asioglld.dll`: 173056-byte PE32+ x64, SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. Duplicate uploaded copy same hash; original not modified.

**User mandate:** exhaustively reverse-engineer original and reconstruct its features/algorithms before optimization. No feature-reduced ASIO replacement. Perform substantial local analysis and unit tests; one final GitHub commit per batch; CI only in late-stage validation.

9차 성과: remaining 59 non-IAT indirect-call sites 59/59 original bytes checked; 17 driver/COM/callback-related role candidates + 42 CRT/exception/initialization support-like code sites (not actual target identities). Original class-factory vtable and CreateInstance success, error, aggregation and lifetime branches traced. Strong local verification 59/59 call opcodes + 23/23 semantic pins. Previous 35 tests and new 13 tests rerun PASS = 48/48. **No Windows original DLL execution or faithful replica parity**.

GitHub contains a compact reproducible version of 59 opcode + 18 factory pin checks, and key findings. Complete Stage9 raw call provenance/164-call ledger and all 23 semantic pins and analysis tests in the conversation downloadable `ASIOGLLD_Original_Recovery_Batch9.zip`.

Remaining: original 42 runtime callback actual target identities, unresolved COM receiver types, full CFG, Ghidra whole-function decompilation, Windows static/dynamic crosscheck, original-equivalent DLL, complete input/output/shared/exclusive/GUI/error parity. Exact original C++ textual source cannot be guaranteed due to compiler information loss. **CI 0, optimization 0.**