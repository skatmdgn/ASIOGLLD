# Batch21 continuation checklist

**Standing request:** reverse engineer and independently reproduce **all original functionality first** (COM/IASIO, WASAPI input/output, shared+exclusive, device selection, GUI/registry, clocks, callbacks, error/COM lifetime). No premature optimization. Analyze in large local batches; one GitHub commit at end; CI only final. Never patch/replace the user-supplied original or publish its binary/full disassembly.

Original SHA256: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, Win64 PE32+, 173056B, two source copies match. Latest preceding GitHub main from Batch20 was `57a2c4fad2f3423916a954936cd092d2ebdccca9`.

Batch19: 590 .pdata records, 221 chains, 369 independent unwind roots (NOT full source function count). Batch20: 7 original switch tables recovered, physical CFG 6334 blocks/8861 within-range edges and zero unresolved indirect JMP in those 590 windows.

**Batch21 new:** crosschecked all 164 non-IAT indirect original CALL instructions; prior 105 statically associated calls remain only inferred ABIs. Previously unresolved 59 split into **17 driver/factory/COM-like** and **42 CRT/SEH/initialization-like**. **6 of 42** have named function/proven original immutable targets: two EncodePointer sites, one DecodePointer site, one mscoree!CorExitProcess site, two static .rdata pointers. **36 still without fixed callee** (8 decoded pointer results, 5 callback-array, 4 mutable-global, 19 unknown exact provenance). No number is a completion percentage.

Tests: 42 new (PASS), Stage5-Batch20 prior 419 rerun (PASS), **461/461 executed, 0 skipped**. Original duplicate gives identical CSV/JSON output; all hashes unchanged. Companion Batch21 ZIP 35 files includes fully reproducible local verifier, original 164-site evidence, old 8th batch JSON baseline, Windows Ghidra CALLIND Pcode exporter / CMD **not executed**, tests & logs. Public repo stores only non-proprietary classification metadata, a compact checker and docs. Do not assert Ghidra execution/Windows parity/fully compiled replica.

**NEXT:** actually run Windows Ghidra with user review; check 164 CALLIND and unwind roots, COM object dataflow, native IASIO/WASAPI state/exception/lifetime, then implement complete original-equivalent native DLL and differential Cubase 8/Realtek tests. CI=0, optimization=0, original mutation=0.
