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