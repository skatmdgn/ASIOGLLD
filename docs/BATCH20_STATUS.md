# Batch20 checkpoint (original behavior first)

User mandate: full behavioral restoration of original ASIOGLLD x64 DLL (all IASIO/COM, WASAPI shared/exclusive, render/capture, device selection, callback, clock, GUI, registry, error and lifecycle), not a reduced implementation, **before optimization**. Do as much work as possible locally and commit GitHub once at end; CI only near final validation.

Original SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd, 173056 B. Two copies independently verified identical and untouched.

Batch20: resolved 7 indirect JMP switch tables in 590 unwind records: 274 reachable selector cases, 51 distinct site-destination edges, 45 global targets, all same physical unwind segment and instruction boundary. Corrected whole-DLL physical CFG 6331->6334 basic blocks and 8807->8861 within-segment edges, unresolved segment indirect JMP 7->0. 67 call destinations outside pdata / 340 incoming call sites categorized into 11 import stubs, 15 direct-tail entries, 10 short-return helpers, 31 other unwindless support/code entries. Neither 369 roots nor 67 targets equals source function count.

Local Batch20 artifact contains complete original SHA-fixed Python/binutils tools, 274-row targets CSV, 590-segment corrected CFG csv, 67 gap-target CSV, cross-run identical outputs and 32 new test logs, plus previous 30 Batch19 and earlier 357 tested: **419/419 tests PASSED, 0 skipped**. Original not installed/run; no CI; no optimization. All 6 key derived outputs same with duplicate original.

NEXT: Ghidra in environment with installer access (not available here), run user-reviewed headless on original copy, use Batch19 Ghidra bridge to reconcile root/funclets and these switch tables. Then restore and implement whole original native COM/IASIO/WASAPI/Cubase functionality and strict Windows behavior parity. DO NOT claim full original source or compiled faithful DLL yet.
