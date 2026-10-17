# Batch 14 — original port selection and simulated device behavior

Phase 1 original-only reverse engineering. No ASIO driver replacement, optimization, CI or original DLL execution.

Original DLL SHA-256: e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd (173056 bytes).

## New findings

- The original UTF-16 strings **Simulated Port**, **Simulated Device**, and **No Selection** are connected to port naming and selection branches. Port flag 0x40 is associated with the simulated-device branch, which bypasses regular WASAPI device activation and format probing.
- The original endpoint selection routine (RVA 0x87F0) checks UTF-16 device names, active state through IMMDevice::GetState for real endpoints, the shared/exclusive rate list, and adjusts the port selection flag 0x2 accordingly.
- An input-side No Selection name match has a special early-success branch without itself setting the selected flag.
- Format probing (RVA 0x7D00) uses a temporary flag 0x4. It is set in the simulated or successfully activated path, and cleared at the end of completed probing. The original calls GetDevicePeriod without testing its HRESULT at the subsequent flag-setting instruction.
- Only S_OK from IsFormatSupported enters format-list insertion; S_FALSE and failing results skip that insertion. At probe completion, an IAudioClient pointer is conditionally released.
- Possible ownership of the pClosestMatch out-parameter remains unverified. Do not characterize it as a proven leak.

## Verified local artifacts

Batch14 companion ZIP contains the exact-byte original evidence: 137 instruction pins (112 distinct from the Batch13 pin set), 44 operand checks, 12 direct call edges, three UTF-16 strings, and eight bounded CFG windows with 138 basic blocks / 201 internal edges. These counts are NOT independent original source functions or reconstruction percentage.

Prior 192 static/model tests and 32 new tests were actually run: **224/224 PASS, zero skipped**. Win64 C++ candidate field-offset assertions also compile successfully. The original was not modified or executed; no Windows runtime parity, decompiled complete DLL or replica exists.

## Continue from here

Recover remaining COM ownership/error branches, per-device configuration persistence and endpoint change behavior. Run Ghidra whole-DLL decompilation and carefully authorized original Windows traces before building and comparing a faithful standalone ASIO DLL. Defer CI and all optimization until the appropriate final validation stage.
