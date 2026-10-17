# Batch16 continuation — original first, CI deferred

**Fixed user mandate:** Original Win64 `asioglld.dll` all behavior (COM/IASIO, WASAPI shared/exclusive, capture/render, configuration and GUI, timing, callbacks, failure cleanup) must be reconstructed and verified first; NO optimization before this. Large LOCAL batches then a single final GitHub commit; defer CI.

Binary SHA-256: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, size 173056 B. Both user original copies matched and remained unchanged. Do not put binary or complete disassembly into public repo.

**New Batch16:** Code `0x94B0` waits for worker max **3000ms** but does not branch on return; cleanup continues with port COM releases and critical section. The wake/wait portion is conditional on stop byte/event/thread handles; the following critical-section cleanup is common. Worker notification `0x8F20` deactivates/stops ports but does NOT terminate worker. Worker thread setup sets stop byte=0 before CreateEvent/CreateThread and does not reset it in inspected failure branches. Config/worker RegisterEndpointNotificationCallback return is ignored; cleanup Unregister guarded by pointers, not tracked registration success.

**Local evidence:** 10 code windows, 84 basic blocks/110 in-window edges, 307 original byte sites (165 not in Batch15 pins), 64 operand sites, 11 direct calls, 10 imported Win32 calls, 7 exact successor pairs. Candidate Worker (0x88 bytes), Notification (0x18), PortNode (0x20) x64 memory layouts compiled successfully. 256 previous regressions and 37 new tests **293/293 pass, 0 skipped**, full local logs and baseline in separately provided `ASIOGLLD_Original_Recovery_Batch16.zip`.

**Next:** full Windows Ghidra headless decompiler pass, interprocedural COM/exception lifetime and error conditions, carefully authorized real Windows original execution trace and recorder, faithful independent native DLL, original-vs-replica differential Cubase test. **Not complete yet. CI=0/optimization=0.**
