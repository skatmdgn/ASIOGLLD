# Project status and continuity note

## Done
- Verified that the duplicate user-uploaded DLL and original had identical SHA-256.
- Original stays unmodified; duplicated working copy not needed.
- Created this GitHub project and documented user requirement: Cubase 8.0.40 *with YouTube audio concurrently*, therefore WASAPI **shared** mode.
- Derived 590 unwind function ranges, 148 imports, 33,194 decoded disassembly instruction rows, 983 static direct-call edges, 11 vtable pointer-run candidates in first pass (only RTTI-linked runs accepted as strong candidates).
- Identified RTTI-backed CAsio IASIO vtable (24 slots), class factory, port and device notification classes.
- Mapped core method call chain and partial CAsio field offsets in `CONTROL_FLOW.md`.

## Not done
- No complete source reconstruction.
- No debugger-backed verification of indirect COM calls, WASAPI data path or ASIO bufferSwitch invocation.
- No binary patch and no verified performance improvement.
- No Windows x64 runtime testing of the recovery scripts in this repo.

## Artifacts
- `tools/pe_inventory.py` regenerates PE import/export/unwind/RTTI candidate inventory from a local DLL. Original DLL bytes should not be committed.
- Full first-pass static call graph and disassembly-derived mapping are available in the companion downloadable analysis ZIP from the working conversation. Reproducible analysis uses `objdump` and the local original.
- `docs/ASIO_VTABLE.md`: high-confidence ABI slot map.
- `docs/ARCHITECTURE.md`: evidence and uncertainty.
- `docs/FLEXASIO_COMPARISON.md`: external reference and distinctions.
- `docs/RECOVERY_PLAN.md`: next steps and stopping conditions.

## Immediate next implementation
Reconstruct the body of 0x8FC0 and the 0x92B0/0x97B0/0x94B0 call cluster; identify actual WASAPI shared-mode buffer write and ASIO callback deadlines. Preserve byte-level evidence for every proposed function name and every COM interface guess.

Never make undocumented changes to the installed Steinberg DLL.
