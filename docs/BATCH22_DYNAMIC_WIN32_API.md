# Batch22: original Win32 dynamically resolved API calls

Original SHA256: e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd (173056B, x64). The supplied DLL was READ ONLY and never loaded/registered/patched. All addresses are RVA in exact source original.

## Six verified original API-name/dataflow chains

| CALL RVA | Actual GetProcAddress name | Stored encoded pointer RVA | Original DecodePointer helper CALL RVA | Prior Batch21 role |
|---|---|---|---|---|
| 0x10FB2 | USER32.DLL!GetProcessWindowStation | 0x27600 | 0x10F91 | Unknown |
| 0x10FD5 | USER32.DLL!GetUserObjectInformationA | 0x27608 | 0x10FA0 | Unknown |
| 0x1102E | USER32.DLL!GetActiveWindow | 0x275F0 | 0x11024 | Decoded target unknown |
| 0x11051 | USER32.DLL!GetLastActivePopup | 0x275F8 | 0x11044 | Decoded target unknown |
| 0x1107B | USER32.DLL!MessageBoxA | 0x275E8 | 0x1105D | Unknown |
| 0x13CA4 | kernel32.dll!InitializeCriticalSectionAndSpinCount OR original fallback RVA 0x13BD0 | 0x27918 | 0x13C17 (cache path) | Unknown |

All six names have original ASCII literals and their references, KERNEL32!GetProcAddress indirect import calls, original EncodePointer helper 0xCE40, original storage slot and DecodePointer helper 0xD000 checked against original machine instructions. This proves a specific optional API name being resolved, NOT the address returned by OS at runtime, whether Windows executes the branch or full behavioral fidelity. The critical section fallback RVA 0x13BD0 directly calls imported InitializeCriticalSection and returns 1; its cache-decode branch is distinct from the initial lookup/encoding branch.

Two additional previously unknown sites are confirmed as calls of DecodePointer wrapper results: 0xEB49 → 0xEB79, 0xF2BA → 0xF2DD. The eventual callback identities are still unknown.

## Correct accounting

The six newly named calls include FOUR formerly fully-unclassified sites and TWO already categorized by Batch21 as calls of decoded pointers; do not double count six as six newly classified sites. Of the 19 previous unknowns: 4 newly named APIs, 2 newly traced through DecodePointer, and **13 with only generic register/SEH callback origin patterns and no proven target identity**. These 13 are NOT solved.

The 42 original runtime-related calls now include 12 named API or original fixed pointee, 8 other decoded-pointer-source callback calls, 5 callback-array calls, 4 mutable globals and 13 general C++ runtime register/scope callback source patterns. All dynamically resolved Windows API addresses remain OS-dependent. No unsupported assignment of those 13 runtime sites to Windows audio interfaces.

## Reproduction

Full companion file ASIOGLLD_Original_Recovery_Batch22.zip (41 files) includes: the original-SHA-pinned 164-call GNU objdump validator, exact original dataflow chains for all six APIs, 164-row old and corrected provenance CSVs, synthetic optional-API model, Windows x64 candidate C++ function pointer types, tests and full logs.

**Ran 45 Batch22 tests + 419 Stage5–Batch20 + 42 Batch21 tests = 506/506 actual local PASS with zero skipped.** Original independent duplicate produces byte-for-byte identical two output CSV and one JSON; G++ C++17 ABI type candidate syntax passed. This is only static/partial-model evidence, **NOT Ghidra whole-DLL decompilation or original-versus-replica parity**. Original modification 0; CI 0; optimization 0; faithfully equivalent native ASIO DLL NOT BUILT.
