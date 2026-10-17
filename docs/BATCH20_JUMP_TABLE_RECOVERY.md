# Batch20 — original static switch-table recovery and unwindless call targets

Original Win64 asioglld.dll, 173056 bytes SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. **Read-only static analysis, NOT Ghidra decompiled source, Windows runtime observation or faithful compiled native ASIO DLL. Original first; no optimization.**

## All seven formerly unresolved indirect JMPs are table dispatches

| jump site RVA | DWORD target table RVA/count | BYTE remap table RVA | selectors | distinct targets |
|---|---|---|---:|---:|
| 0x0E564 | 0x0F148 / 8 | none | 8 | 8 |
| 0x0E8A8 | 0x0F168 / 15 | 0x0F1A4 | 56 | 15 |
| 0x10ADE | 0x10CEC / 6 | 0x10D04 | 21 | 6 |
| 0x1B656 | 0x1BE90 / 12 | none | 12 | 12 |
| 0x1B716 | 0x1BEC0 / 4 | 0x1BED0 | 59 | 4 |
| 0x1B7CC | 0x1BF0C / 3 | 0x1BF18 | 59 | 3 |
| 0x1B850 | 0x1BF54 / 3 | 0x1BF60 | 59 | 3 |

These x64 dispatches use `FF E1` (jmp rcx) or `FF E2` (jmp rdx). Every reachable remapped index was in its table's range. All **274 selector cases** resolve to instruction-boundary destinations within the *same original physical unwind segment/root*; there are **51 distinct site-to-target edges and 45 distinct target addresses globally**. Original data bytes and SHA were checked; this resolves these seven physical-CFG indirect JMPs, **not** the 164 non-IAT indirect CALL locations elsewhere.

## Whole-original CFG corrected, not merely annotated

Identical GNU objdump-based analysis first reproduced Batch19 baseline for all 590 `.pdata` segments: **6331 basic blocks / 8807 internal edges**, with seven unresolved indirect jump sites. Branch-target splitting and the seven recovered switch tables produced **6334 blocks / 8861 internal edges / zero unresolved indirect jump sites in those 590 physical segments**. The extra 54 edges include 51 switch dispatch edges and changes due to newly split basic blocks. Numbers represent bounded *static machine-code CFG*, NOT source C++ functions or runtime coverage.

## All 67 call targets outside .pdata also classified

All 67 original direct-CALL destinations not covered by x64 unwind ranges were examined; 340 direct call sites refer to them. Classification by observed entry preamble: **11 IAT import stubs, 15 direct-tail transfer entries, 10 short return-form routines, 31 longer unwindless helpers or internal entry candidates**. This classification is a conservative first-instruction heuristic, NOT full source function recovery. PCM functions RVA `0x023F0` and `0x024C0` are actual original sample-copy helpers among these unwindless call targets, emphasizing that 369 unwind roots do NOT equal the number of original functions. High-use call destinations include RVA 0x0C370 (94 callsites), 0x0C520 (48), 0x10D50 (34), 0x114D0 (25).

## Reproducibility / tests / next steps

Standalone source `tools/batch20_jump_table_spotcheck.py` uses only Python stdlib, checks original exact SHA and seven tables plus unwind roots; complete CSV-exporting tools for 274 selector rows, 590-window corrected CFG, 67 leaf entries and tests are in the companion `ASIOGLLD_Original_Recovery_Batch20.zip` (37 files, no original DLL). Those tools include copied SHA-pinned Batch19 binutils analysis dependencies.

**Tests actually executed**: Batch20 32 + Batch19 30 + all older regressions 357 = **419/419 PASS, skipped 0**, plus six generated artifacts reproduced byte-identically using duplicate original DLL. These are static/model tests, NOT parity with running original.

Ghidra whole-original decompilation was not performed: no Ghidra in local environment and github.com DNS unavailable for installation. Pending: genuine decompile with function boundaries, 9 cross-root tail jumps, SEH/EH dataflow, unresolved COM calls, fully faithful native DLL, real Windows Cubase+Realtek differential parity. CI 0, optimization 0, original DLL modification 0.
