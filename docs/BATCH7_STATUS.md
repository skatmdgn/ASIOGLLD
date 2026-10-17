# Batch 7 continuation checkpoint — 2026-10-17

**Highest user instruction:** FIRST reconstruct original `asioglld.dll` as faithfully and comprehensively as possible. NO optimization or partial shared-mode-only substitute. Shared and exclusive, capture and render, all settings/errors/time/COM behavior must be covered.

**User workflow:** do as much LOCAL original analysis/tests as possible; only commit to GitHub once at the end of a substantial batch; **NO per-step CI, defer CI to final stages**.

Original: SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, size 173056 bytes. Duplicate uploaded copy hash identical. Original not modified.

New Batch 7: decoded exact `IAudioClient::Initialize` shared vs exclusive event/poll branch at 0x3A9A–0x3B0C; render/capture GetService direction at 0x3B9D; CreateEventA/SetEventHandle and failure cleanup 0x3C36–0x3C7A; clock GetPosition/GetFrequency 0x46D5/0x46F1 and timeGetTime branch. 30 of 164 non-IAT indirect CALL positions have static ABI/method names, 134 still UNRESOLVED. See `docs/BATCH7_ORIGINAL_WASAPI.md`.

Verification 30/30 opcode byte pins and 3/3 IAT identifiers; 9 new local unit tests pass. Prior 11+4 pass again = 24. NO Windows DLL execution, Ghidra exhaustive decompilation, replica, runtime parity, optimization or CI.

Original DLL/complete extracted disassembly NOT committed to public GitHub. A standalone companion Batch 7 ZIP with full analysis tool and 164-site JSON is available as a conversation artifact. The included Windows COM probe is NOT RUN; might access/create HKCU registry ASIO settings if run later. Require user's explicit informed go-ahead.

Next: recover remaining 134 indirect call types using interprocedural COM receiver tracing; trace x64 exception funclets/CFG, original start/stop/callback and clock sample math, full configuration GUI; run original on Windows only with user's approved procedure; build unoptimized behavior-faithful DLL later, compare parity. Keep all uncertainty explicit.