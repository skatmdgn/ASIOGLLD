# Recovery plan — original fidelity BEFORE optimization

Read PHASE1_ORIGINAL_PARITY_KO.md first. Current task is Phase 1 ONLY.

## Phase 1A: exhaustive static recovery
- Inventory all PE regions, imports/exports, resources, strings, RTTI, relocations and exception metadata.
- Discover functions beyond the 590 recorded unwind ranges: leaf functions, thunks, unreferenced blocks and indirect dispatch.
- Build verified CFG and direct/indirect call maps, class layouts and per-function unresolved ledger.
- Use Ghidra for all identified functions; generated pseudocode is not original C++.

## Phase 1B: original behavioral specification
- Recover every IASIO slot and COM object lifecycle.
- Recover BOTH WASAPI shared AND exclusive, input AND output, formats, buffers, sample-rate paths, clock, events and worker synchronization.
- Recover settings/UI/registry, device changes, errors and teardown.
- FlexASIO and official SDK are references only, never presumed identical to original implementation.

## Phase 1C: original runtime ground truth
- Trace the original on Windows under compatible hosts and multiple device/format/configuration/error cases.
- Verify COM virtual calls, callback order, buffer content movement, class state transitions and thread timing.
- Keep test conditions and original evidence attached to every behavior claim.

## Phase 1D: unoptimized original-equivalent implementation
- Reimplement complete original behavior in separate project/binary with no shortcuts, modern replacements or omitted features.
- Protect installed original from modification.

## Phase 1E: differential parity
- Run original and replica under matching tests for all API calls, modes, input/output, UI, errors, device recovery and Cubase + YouTube.
- Record PASS/FAIL/NOT_TESTED/UNKNOWN in ORIGINAL_PARITY_MATRIX.md.
- Never claim 'complete' with unresolved, untested or failing required paths.

## Phase 2: deferred
Only after user approval and Phase 1 parity verification: evaluate performance improvements. Do not optimize in Phase 1.