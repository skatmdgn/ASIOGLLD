# Batch 7 — original WASAPI initialization, clock, COM provenance

**Phase 1 only: reconstruct original ASIOGLLD exactly as observed, NO optimization or feature trimming.** Source SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, 173056 bytes. All RVAs refer to that exact DLL.

## Newly recovered original branches

Original `IAudioClient::Initialize` argument setup `0x3AA7–0x3B0C`:
- `duration100ns = requestedDurationMs * 10000`.
- `shareMode = (original r13b == 1 ? exclusive 1 : shared 0)`.
- If **exclusive AND an upstream stack condition byte [rsp+0xF0] is zero**, `streamFlags=0x40000` (EVENTCALLBACK), `hnsBufferDuration=duration100ns`, `hnsPeriodicity=duration100ns`.
- Otherwise (including **shared mode**), `streamFlags=0`, `hnsBufferDuration=duration100ns*2`, `hnsPeriodicity=0`.
- The upstream meaning and full provenance of the stack condition byte still need tracing; do not simplify this to “all exclusive sessions use events.”

Original **render/capture** selection is a *separate* branch `0x3B9D`: port field `+0x80==0` -> GetService(`IID_IAudioRenderClient`) into `+0x38`; otherwise GetService(`IID_IAudioCaptureClient`) into `+0x30`. An `IAudioClock` is requested separately at `0x3BE2` and placed in port `+0x40`.

The original event path creates an event using `CreateEventA` (`0x3C15`), stores it at port `+0x70`, and calls `IAudioClient::SetEventHandle` (`0x3C2E`). There is a conditional `Reset` call (`0x3C00`). Failed setup has a dedicated cleanup path releasing clock, capture and render COM pointers (`0x3C4D,0x3C60,0x3C73`). Other conditional cleanup occurs around `0x9552–0x95A8`; do not infer double-free from two code locations because ownership depends on the path.

## Original clock paths

Port's `IAudioClock` interface at `+0x40` has `GetPosition` at `0x46D5` (vtable +0x20) and `GetFrequency` at `0x46F1` (+0x18). Code around `0x4703–0x470C` computes `sampleRate * position / frequency` with a zero-frequency fallback. Other conditions use `timeGetTime` (`0x4628`) with additional wrap/elapsed-time arithmetic. Full original timeInfo composition is NOT yet recovered.

## Indirect-call coverage

- **643** indirect CALL instructions; **479** linked to original PE imports.
- **164** indirect calls do not resolve immediately to IAT imports.
- **30** positions now have a statically grounded interface/method identity (this **includes** earlier 17 WASAPI positions), **134 remain unknown**.
- The 30 are call *positions*, not number of original source functions and not overall restoration progress.
- Companion Stage 7 ZIP includes local reproducible short backward-register provenance analyzer and 164-entry JSON, as well as original opcode checks. New GitHub script `tools/batch7_original_wasapi.py` reproduces the key fixed-byte ABI checks.

## Validation & limits

- Original 30 pinned opcode sites + 3 Windows IAT name entries matched original binary.
- Local unit tests: Batch 6 11/11, Stage 5 4/4, Batch 7 9/9, **24 passed** in total. These are parser/static/model tests, **NOT** original-vs-replica runtime parity.
- Windows COM factory probe source is included with the companion ZIP, **not built or run** here; loading/creating original objects may touch HKCU ASIO settings, so user's explicit approval and backup are required.
- No Ghidra whole-DLL decompilation, no Windows runtime tests, no full-fidelity reconstructed DLL, no parity check, **no optimization and NO CI**.

**Next:** preserve per-call and object lifetime ledgers; bulk Ghidra decompilation, original Windows tracing, exact ASIO/WASAPI error/state semantics, faithful reconstruction, then controlled parity tests.