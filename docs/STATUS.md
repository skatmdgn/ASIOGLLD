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

## Stage 3b: original IASIO response semantics
- Confirmed via instruction and 13 file-byte checks: getChannels (0x1910) returns object+0x48 / +0x4C; getLatencies (0x1930) returns twice object+0x3C for both directions; getSampleRate (0x1AA0) converts positive object+0x44 to double.
- Confirmed getBufferSize (0x1C50) copies positive object+0x3C to **min, max, preferred AND granularity**; do not silently 'correct' this unusual original behavior during reproduction.
- getDriverVersion (0x1690) directly returns object+0x9C.
- Method details and error branches: docs/IASIO_BASIC_METHODS.md. No runtime original/replica parity yet.


## Phase 1 Stage 4: configuration, registry, resource and missing-leaf coverage
- Verified original embedded config initialization: BufferDuration=10, SampleRate=44100, flags bit0 ExclusiveMode=1; PollMode bit1=0; UserDefinedBufferSize bit2=0. Registry can override these defaults. See CONFIG_REGISTRY_RECOVERY.md.
- 23/23 config opcode checks, 9 registry key strings validated. Hash mutation is rejected.
- Parsed 11 PE resource leaves, 7 dialog templates (main ID 130 has 28 controls, 6 languages including neutral), 0 parser exceptions. See UI_RESOURCES.md.
- Confirmed 305 direct CALL targets (vs previous 304 with narrower .pdata-owned caller filter), 67 outside unwind. See COVERAGE_LEDGER_STAGE4.md.
- Existing 30 callback and 13 IASIO basic checks re-executed: all match original; no new Windows runtime parity.
- Stage 4 comprehensive Python tools/data available in the Stage4 analysis ZIP, plus reproducible summary script tools/recovery_v4.py. Still no faithful replica and no optimization.


## Stage 4b — original COM class-factory metadata
- Verified original driver CLSID 52ebae30-47e4-483f-b87b-770314306005 from raw bytes at RVA 0x26690, standard IUnknown and IClassFactory IIDs.
- Confirmed COM factory allocation 0x18 bytes, original CAsio allocation 0xD0, and DllGetClassObject primary error paths. tools/verify_com_factory.py: 9/9 passes against original.
- DllCanUnloadNow references 0x27AB0 and 0x27AA4 counters; full object lifetime still unresolved.
- UI document corrected IDs 1109/1110 to raw Windows LISTBOX ordinal 131 (not SysListView32).

## Phase 1 Stage 5 — registry and UI message dispatch; leaf triage

- Read-only original hash checked; 30/30 registry/UI opcode signatures match original; buffer table [10,50,100] matches; local full auditor independently verifies 11/11 PE import names.
- Corrected older misnaming `RegOpenKeyExA` to actual imported `RegOpenKeyA`, with `RegCreateKeyA` fallback; generic config root is HKCU Software\\ASIO\\Generic Low Latency ASIO Driver.
- Identified original dialog handler 0xB6D0, WM_DRAWITEM (0x2B), WM_INITDIALOG (0x110), WM_COMMAND (0x111), WM_VSCROLL (0x115), control IDs 1/2/1086/1092/1090, and user-defined range 10–100 or preset [10,50,100].
- Full .text virtual size ends at RVA 0x1D0BA; 305 distinct direct call targets. Previous 304 came from an incorrect <0x1D000 cutoff (omitted 0x1D050).
- 67 direct targets outside unwind: 11 resolved PE import thunks, 2 ret stubs, 1 internal jump stub, 53 unresolved candidates. See `docs/UNWIND_LEAF_TRIAGE_STAGE5.md`.
- Remaining: exact registry failure semantics, UI handlers and persistence, all indirect COM paths, all original functions, Ghidra/Windows runtime, faithful replica and differential parity. NO optimization.


## Phase 1 Stage 5b — original GUI buffer-value transforms
- Traced 0xB280 (buffer duration -> slider index) and 0xB310 (slider index -> duration). Uses original [10,50,100] data table, 10–100 custom clamp, midpoint cutoffs 30 and 75, and unusual >100 ordinary-mode fallback to index 0.
- Added pure analysis model and four unit tests; local tests passed. This is NOT the original Windows runtime and NOT replica parity. See docs/BUFFER_SLIDER_ORIGINAL_ALGORITHM.md.
