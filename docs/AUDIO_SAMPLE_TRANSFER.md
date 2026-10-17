# Recovered PCM transfer internals — original-only investigation

This is read-only static reconstruction from the original x64 binary (SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`). Address values are RVA. Not source equivalence or runtime parity.

## Render path and byte interleaving

- `0x4020` handles audio transfer, with an output path and additional conditional control/stream branches. Do **not** assume the entire function is render-only.
- `0x40D7` calls `IAudioRenderClient::GetBuffer` using port field +0x38.
- `0x41B0–0x41CF` is a concrete 2-channel, 16-bit **interleaving loop**: loads 16-bit sample from each of two source pointers, stores into adjacent 16-bit positions in a 4-byte interleaved frame, advances source pointers by 2 and destination by 4, repeats per frame.
- `0x4221` conditionally calls **0x23F0**, an important **unwind-unlisted leaf function**.
- `0x424B` calls `IAudioRenderClient::ReleaseBuffer`.

## Leaf function 0x23F0 (no .pdata entry)

Directly invoked from the original render routine. Inspection of its own machine code demonstrates size-directed copy branches:
- when an internal width/category field equals 1, it copies a **1-byte** sample per iteration;
- when it equals 2, copies a **2-byte** sample per iteration;
- when it equals 4, copies a **4-byte** sample per iteration;
- increments destination with a caller-supplied stride while source advances by the sample width;
- validates channel/index/available buffer pointer and returns without copying in unsupported/missing cases.

This is a directly observed sample-copy primitive; the internal field's full semantic meaning and the full format compatibility matrix are not yet reconstructed.

**Coverage implication:** .pdata has no record at 0x23F0 even though this routine has direct CALL xrefs and RET instructions. An inventory restricted to 590 .pdata entries is incomplete.

## Capture path and buffer handling

- The path beginning at `0x4380` is linked across 4 adjacent unwind ranges, culminating before `0x460C`.
- `0x44EA`: `IAudioCaptureClient::GetNextPacketSize`.
- `0x4580`: `IAudioCaptureClient::GetBuffer`.
- `0x45C2`: helper `0x2A90` is invoked to process captured samples.
- `0x45D5`: `IAudioCaptureClient::ReleaseBuffer`.
- Helper `0x2A90` contains a special case invoking `0x2900` and a general per-channel branch invoking `0x2750`, then updates internal index/cursor fields. Exact channel layout, wrap arithmetic and error handling remain unresolved.

## Static call-target coverage audit

From the existing Stage 1 direct-call graph:
- **304 distinct direct-call target RVAs** were recorded;
- **67 of them do not coincide with any .pdata start and lie outside all .pdata ranges** (may include true leaf routines, compiler helpers and thunks);
- the earlier count of 590 unwind ranges is neither complete function discovery nor a guarantee of 590 unique source functions.
- **This 67 count is a triage result**, not proof that all 67 represent independent functions, and excludes indirect/virtual call-only targets.

A complete reconstruction must inspect those 67 targets and all indirect/virtual/exception-dispatched targets in addition to the original 590 unwind ranges. Code can also be unreferenced through simple static CALL scanning.

## Required follow-up

1. Recover complete bodies and inputs/outputs for 0x23F0, 0x2900, 0x2750, 0x2A90 and each caller.
2. Determine exact sample type mappings, endian/width/routing, copy stride and handling of invalid buffers.
3. Reconstruct lifetime/state and shared/exclusive branches.
4. Dynamically confirm on Windows with original DLL before calling behavior verified.
5. Later implement **matching**, unoptimized behavior and differential tests; do not change algorithms.
