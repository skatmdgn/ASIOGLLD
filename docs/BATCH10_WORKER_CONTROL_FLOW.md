# Batch 10: Original ASIO worker state machine (STATIC)

Original SHA-256: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. RVA offsets only. **Original-first reconstruction, no optimization.** Full evidence, portable model and 75 opcode pins are in the Batch10 companion ZIP.

## Confirmed assembly / inferred semantics

1. `IASIO::createBuffers 0x1C90` → `worker_setup 0x92B0`: traverse two port lists, gate on port flags, call port init `0x3870`, allocate 0x20-byte worker port nodes, keep ASIOCallbacks* at worker+0x10. Set up Windows event and `CreateThread` with entrypoint `0x8F80`. Several error/zero-port branches still unresolved.
2. `IASIO::start 0x1740` → `worker_start 0x8FC0`: reset block counter and double buffer index; **two initial preroll iterations** using output helper `0x4020` and ASIO callback helper `0x9610` (RVA 0x9011 sets loop count 2, 0x904E calls callback), then port clocks / IAudioClient::Start and worker active flag.
3. Thread entry `0x8F80` selects `0x97B0` for the original PollMode flag. Its alternative contains the original `Notification Thread is currently not supported.` MessageBoxA path. Do not assume the default constructor's flag values are the effective runtime registry settings.
4. Poll worker `0x97B0`: register MMCSS, count ports, build expected mask by **32-bit ROL**, wait using `WaitForSingleObject(event,1)`, check worker shutdown/active flags, then enter critical section. Per port: call capture helper `0x4380`, then *if successful* render helper `0x4020`. If both succeed, OR that port's bit into **persistent** completed mask.
5. At `0x9947`, if the persistent mask equals the expected mask, call `0x9610` and **only then reset** the completed mask at `0x9951`. If incomplete, retain bits for following poll iterations. This distinction matters for faithful timing and callback order. `WAIT_FAILED (0xFFFFFFFF)` terminates; `WAIT_TIMEOUT` is not separately checked before attempting work.
6. `0x9610`: clear 0x94-byte ASIOTime-like temporary structure, write timeInfo.flags=7 (RVA 0x9729), load worker+0x10 ASIOCallbacks pointer and +0x08 double-buffer index, call callback table +0x18 (ASIO `bufferSwitchTimeInfo`) with directProcess=1. Increment block counter and toggle double buffer index, even on callback-pointer-null branch.
7. `worker_stop 0x94B0`: set shutdown flag, `SetEvent`, `WaitForSingleObject(thread,3000)`, CloseHandle, and conditional COM/port cleanup. Static code confirms calls, **not** all ownership and timeout guarantees.

## Original CPU mask corner cases

- Zero ports yields target mask zero, so comparison permits callback in a synthetic active-worker path; reachability in Cubase not established.
- Port indices use 32-bit shift-count semantics; if >32 port nodes can occur, bit aliases exist. This is only a **hypothetical original-code edge case**, not a proven defect or performance bottleneck.
- Never replace the rolling success mask with a fresh mask every poll. That would be a behavior change.

## Verification and limits

12 code windows, 351 **basic blocks**, 512 **within-window branch edges**, and 91 **CALL positions** were extracted from the unchanged original using GNU objdump and a PE-aware parser. **Not 351 recovered source functions.** Original bytes at 75 pinned instruction sites and the 24-slot CAsio IASIO vtable match. Pure Python analysis model and parser tests pass, but original Windows execution, COM receiver attribution, exhaustive exception flow, a faithfully rebuilt DLL and original-vs-replica parity remain **NOT TESTED**. No CI or optimization.