# Project status — 2026-10-17

## USER'S ABSOLUTE PRIORITY
FIRST reverse engineer and reproduce the existing original asioglld.dll **as faithfully and completely as possible**, without optimization. ONLY AFTER tested original parity and explicit user approval consider Phase 2 performance changes. No limited shared-mode ASIO rewrite as substitute for original restoration.

Authoritative: PHASE1_ORIGINAL_PARITY_KO.md, RECOVERY_PLAN.md, ORIGINAL_PARITY_MATRIX.md.

## Static work reported so far
- User original/duplicate SHA-256 identical; original preserved.
- First pass: 590 unwind ranges, 148 imports, 33,194 disassembly rows, 983 direct-call edges, 11 pointer-run vtable candidates.
- CAsio IASIO vtable slots mapped and WASAPI GUID references identified.
- Partial original method control flow and class state offsets recorded in CONTROL_FLOW.md.

## Not yet done
- Exhaustive function/branch/indirect-call graph and field semantics.
- Full ASIO and shared/exclusive WASAPI behavior map, original dynamic traces.
- Working full-fidelity replica, comparisons and parity sign-off.
- **NO ORIGINAL-BASED OPTIMIZATION PERMITTED YET.**

## Next
Finish/validate Windows Ghidra decompilation; maintain per-function unknowns; reconstruct original branches, error handling and data paths; trace original runtime; only then reproduce same algorithms and compare.
Never overwrite the original or commit proprietary DLL bytes.

## 2026-10-17 Phase 1, static pass 2
- Re-validated supplied SHA-256 against mounted user file; read-only.
- Identified original WASAPI initialize (0x3870), render transfer (0x4020), capture transfer (0x4380–0x460C); see ORIGINAL_WASAPI_DATAFLOW.md.
- Verified 17 COM vtable callsites and 6 Windows audio GUIDs against actual DLL instructions/bytes (static only, runtime UNVERIFIED).
- Corrected **590 .pdata ranges != 590 independent functions**; capture routine spans 4 unwind entries.
- No replica built, no full semantic reconstruction, no parity test, and **no optimization**.
- Next: exact sample format conversions, callback transfer, mode flags, exception/port lifecycle, missing function coverage, then original Windows runtime tracing.


## Phase 1, static pass 2b
- Mapped output sample interleaving 0x41B0–0x41CF and specialized/general copy helper at 0x23F0; original code (0x23F0) has no unwind entry.
- Mapped capture GetNextPacketSize/GetBuffer/helper 0x2A90/ReleaseBuffer and called helpers 0x2900 and 0x2750.
- Stage 1 direct-call map contains 304 unique direct targets; 67 are outside all 590 unwind ranges. These are **candidates, not a validated function count**.
- See AUDIO_SAMPLE_TRANSFER.md and COVERAGE_LEDGER.md. Still no original-executable parity test or complete source reconstruction.


## 2026-10-17, Stage 3: callback/worker reconstruction
- Derived original ASIO callback pipeline from createBuffers, worker setup/CreateThread, 0x8F80 entry, 0x97B0 event dispatcher, and 0x9610 callback helper.
- Verified 30/30 opcode/pointer or control-flow sites against the original SHA. Source: `docs/ASIO_CALLBACK_PIPELINE.md`, `tools/verify_callback_bytes.py`.
- Found the conditional initial 2-buffer pre-roll path and all-ports-mask gating before ASIO callback. Recovered limited worker object fields and timeInfo.flags=7.
- No original runtime debugger tracing or fully reconstructed code or replica parity yet. No optimization.
