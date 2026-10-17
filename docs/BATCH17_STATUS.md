# Batch17 continuation checkpoint

**Mandatory user instructions:** Exhaustive original-only reverse engineering and unoptimized faithful reconstruction first; include COM/IASIO, shared+exclusive WASAPI, input/output, configuration/UI, timing, error paths, object lifetime. Do long local analysis/tests, one final GitHub commit; defer CI.

Original x64 173056 bytes SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, duplicate matches, unmodified.

Batch17 traced the same ASIO setup error **through multiple native functions**: `createBuffers` discards the WorkerPrepare error; thread setup can fail with stopByte=0; WorkerStart sets active and returns success without checking thread/event handle; pre-roll TimeInfo helper executes twice even with empty port list; actual callback pointer nullable; common WorkerStop cleanup skips wait for absent handles. This is conditioned STATIC reachability, **not demonstrated Windows runtime occurrence**.

Local package `ASIOGLLD_Original_Recovery_Batch17.zip`: 61 native instruction pins, 4 direct calls, 6 IAT calls, 6 CFG windows/123 blocks/190 edges; Python branch replay, 29 new unit tests, 293 prior regression logs, candidate C++ structs. **322/322 PASS, 0 skipped**. Original not run/modified; no native replica, parity, optimization or CI.

Next mandatory gate: Windows Ghidra whole-DLL decompiler, full port/error/exceptions/COM lifecycle, safe authorized original runtime recording then independent native replica and differential Cubase tests. Preserve README and stage status in GitHub; detailed evidence remains in this conversation ZIP.
