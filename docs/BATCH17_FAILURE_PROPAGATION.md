# Batch17: IASIO to worker failure-propagation audit

Original Win64 `asioglld.dll`: 173056 bytes, SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. **Only original-machine-code STATIC findings; not tested in Windows, not a parity result.**

At `IASIO::createBuffers 0x1C90`, failed config validation through `0x7A80` triggers `disposeBuffers` and returns `-994`. In contrast, successful validation leads to `call WorkerPrepare 0x92B0` at `0x1CE7`, immediately followed by `xor eax,eax` at `0x1CEC`. The WorkerPrepare return is therefore not forwarded to the ASIO host.

WorkerPrepare `0x940E–0x9494` sets Worker+0x30 stopByte to 0 at `0x942D` **before** CreateEventA and CreateThread. Its visible failed-creation branch returns false at `0x9492`, without rolling stopByte back to 1. **Therefore a successful createBuffers return can coexist with a missing worker thread under those failure preconditions.**

`IASIO::start 0x1740` returns `-1000` if the CAsio+0xC8 Worker pointer is missing or WorkerStart returns false; otherwise returns 0. `WorkerStart 0x8FC0–0x92AF` has **one RET** and does not require the thread/event handle in its visible code; `0x929C` unconditionally sets Worker+0x50 active bit0, and `0x92A3` yields true. Therefore, given a valid Worker/config object, `start` can also return 0 despite failed event/thread creation.

If Worker+0x40 port list is null, `0x8FDE` skips clock collection and `0x9011` still enters a **2-iteration preroll**. Each iteration calls `0x9610` at `0x904E`. The TimeInfo helper only calls `bufferSwitchTimeInfo` when Worker+0x10 host callbacks pointer is nonnull (`0x9757–0x976E`), but increments block count and toggles double-buffer index regardless (`0x9771–0x977C`). Two preroll helper invocations therefore do not guarantee two actual host callback invocations.

WorkerStop `0x94B0` conditionally wakes/waits only when stopByte=0 and event/thread handles both exist; otherwise skips wake/wait to common cleanup `0x951C` and may leave stopByte=0. An actual WaitForSingleObject failure/timeout is not checked before cleanup. **No Windows failure, audio drop, crash or bug was observed or claimed.** Native exception paths and OS/host reachability remain unverified.

Batch17 local evidence: 61 exact original opcode/operand checks, four direct CALLs, six Win32 IAT calls, six bounded physical CFG windows (123 blocks / 190 internal edges), x64 C++ offset asserts. **29 new tests + 293 prior regressions = 322/322 executed and passed, skipped 0**. Full verifier and evidence CSV/CFG JSON and test logs are in the companion `ASIOGLLD_Original_Recovery_Batch17.zip`, without original DLL or full disassembly.

**Remaining:** Ghidra whole-DLL decompilation, native Windows original-runtime tracing (user consent/registry backup), complete independent original-equivalent DLL and real-device Cubase differential parity. **No CI or optimization.**
