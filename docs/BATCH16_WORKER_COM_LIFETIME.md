# Batch 16 — original worker shutdown, registration and resource lifetime

This is an instruction-backed **STATIC** reconstruction of the original 173056-byte Win64 `asioglld.dll` with SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. All addresses are original RVA, not replacement implementation addresses. **Original-first and no optimization.**

## Worker setup and partial state

The worker initialization segment at `0x9410–0x9494` checks stop byte Worker+0x30 before setup. **At `0x942D` it stores zero to stopByte BEFORE CreateEventA and CreateThread**. When CreateEventA or CreateThread fails, the visible cleanup closes an existing event handle and nulls Worker+0x18, but does **not** roll stopByte back to one in that branch. Returning false cannot be described as full state rollback. Earlier `createBuffers 0x1C90` does not check the return of worker setup `0x92B0` on its normal post-validation path.

## Worker stop is two conditionality levels, not one

Original `0x94B0–0x960B` has a **conditional** wake/wait section, then a **common** cleanup section.

If stopByte==0 and Worker+0x18 event and Worker+0x20 thread handle are nonnull, `0x94E3` sets stopByte=1; `0x94E7` calls SetEvent; `0x94F1` passes **3000ms** to `WaitForSingleObject` at `0x94F6`. The very next instruction **`0x94FC` loads the thread handle, without checking the returned wait status**. It then closes the thread handle `0x9500`, event handle `0x9512`, and clears the fields. If the wake/wait preconditions are not met, the code jumps to **`0x951C`**, skipping only this part.

In **either case** `0x9520` enters Worker+0x60 critical section. For linked port nodes under Worker+0x40:
- port+0x64 bit3 `0x08`: release capture `+0x30`, render `+0x38`, audio clock `+0x40`, then close per-port event `+0x70` if each exists (0x9546–0x958E).
- bit2 `0x04`: conditionally release IAudioClient `+0x28`; clear bit2 (0x9592–0x95AF).
- always clear bit3 (0x95B3).

At `0x95C3–0x95E4` linked worker ports are freed and Worker+0x40 becomes null. `0x95E8` calls LeaveCriticalSection and `0x95F8` clears worker+0x10 ASIOCallbacks pointer. **Timeout/WAIT_FAILED therefore are not followed by an in-function branch preventing cleanup.** Windows CloseHandle does not terminate a still-running thread. This observation signals a runtime concurrency question; it is **not proof** of crashes, timeout occurrence, or a memory bug in Cubase.

## Device notification is not worker teardown

The worker IMMNotificationClient callback `0x8F20` clears worker+0x50 active bit0, conditionally calls IAudioClient::Stop for ports with started bit4, and clears their started bits. It does **not** set worker+0x30 stopByte, SetEvent, WaitForSingleObject, free the port list, or enter the worker critical section in its observed code. Original worker polling `0x97B0` separately checks active and termination state. Never merge the two source state transitions just because both stop audio.

## Notification registration failure and ownership

- Config registration `0x682A`: CoCreateInstance, with **result pointer** null check at `0x6830`; 24-byte listener allocation `0x683A`; conditional AddRef `0x6871` and RegisterEndpointNotificationCallback `0x687D`. The next instruction does not test the **registration HRESULT**.
- Worker registration `0x1152–0x1196`: worker/listener/enumerator pointer checks, 24-byte listener allocation, AddRef then Register; HRESULT not tested at site.
- Config/worker destructors' Unregister calls `0x6674`, `0x1354`, `0x1428` are conditioned on **stored pointers**, not on a separately recorded registration-success Boolean. Calls are followed by Release as appropriate.

Accordingly **registration attempted** and **confirmed registered in Windows** are different. Actual COM refcount effects, callback concurrency, and every failure path remain unverified by Windows runtime. Do not declare a proven double-free or leak.

## Verification and evidence limits

10 analyst-defined code windows; **84 basic blocks and 110 within-window edges** (38 CALL positions). **307 fixed original opcode positions**, **165 positions absent from immediately prior Batch15 pin list**, **64 exact operand checks**, **11 direct CALL edges**, **10 Win32 import callsites**, **7 adjacent-instruction conditions**. These are physical program structure measures, NOT number of complete original high-level functions or a progress percentage.

Original-bin SHA checked before reading; candidate Win64 C++ struct layouts compiled by GCC. **256 prior plus 37 new tests, 293/293 executed and passed, skipped 0**. These are static and synthetic-model tests only. The separate private Batch16 ZIP includes the 307-site CSV, disassembly-free CFG JSON, auditable scripts, all test logs, and a 14-row Ghidra investigation queue. The public repository does **not** include the original DLL or a mass disassembly.

No Windows original runtime trace, complete Ghidra decompilation, faithful independent native DLL or original-versus-replica parity exists yet. **CI 0; optimization 0; original modifications 0.**
