# ASIOGLLD — evidence-based binary recovery

Reverse-engineering research into the original Steinberg Generic Low Latency ASIO driver `asioglld.dll`, with emphasis on reliable **Cubase 8.0.40 playback while browser/YouTube audio works at the same time** (WASAPI shared mode).

## Project rules

- **No claim of complete restoration:** the exact original source and variable names cannot be recovered from an optimized x64 DLL.
- **Preserve the original binary:** never patch or replace the installed driver during analysis.
- **Evidence vs hypothesis:** mark every recovered claim as `CONFIRMED`, `INFERRED`, `REFERENCE_ONLY`, or `UNVERIFIED`.
- **FlexASIO is a comparative reference**, not evidence that ASIOGLLD uses the same internal code or algorithms.
- **Shared mode is mandatory** for the user's use case; exclusive-only benchmarks are not an optimization target.
- **No redistribution of proprietary DLL bytes.** Use the locally held authorized original file with the scripts; commit hashes, metadata, derived maps, and our own code only.
- **No claimed speedup until measured** in Cubase with repeatable dropouts/ASIO peak A/B tests.

## Reference input (user-supplied, not committed)

`asioglld.dll` (64-bit), 173056 bytes

SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`

The second uploaded copy has the same SHA-256 and does not require separate analysis.

## Initial scan (read-only)

- PE exception table provides **590 unwind function ranges**, *not* necessarily all functions.
- Import table: **148 imported entries**.
- Static disassembly: **33,194 decoded instruction lines**.
- Direct-call graph: **983 distinct caller→target edges**.
- **11 candidate** runs of executable pointers (potential vtables; not all proven).
- No robust packer/encryption signature in the conventional PE structure; absence is not proof.

## Workflow

1. Recreate a machine-verifiable PE/function/import/call graph inventory.
2. Map COM class factory and vtables, ASIO interface callbacks, WASAPI interfaces, synchronization, buffer transforms, and configuration.
3. Triangulate with the open-source FlexASIO architecture, marking inferences explicitly.
4. Use Windows runtime tracing to verify indirect COM calls and event timing.
5. Only after evidence of a bottleneck, implement reversible changes and compare Cubase A/B results.

See `docs/` and `analysis/` for findings and the source of each hypothesis. No original DLL bytes are included.
