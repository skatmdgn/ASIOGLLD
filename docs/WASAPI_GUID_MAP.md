# Direct Windows Audio interface GUID references

This mapping comes from **actual GUID byte sequences and RIP-relative references in the original DLL**, not from FlexASIO. Values are original file RVAs.

| Windows COM identifier | Data RVA | Code referencing GUID | Status |
|---|---:|---:|---|
| CLSID_MMDeviceEnumerator | 0x20918 | 0x67E0 | confirmed |
| IID_IMMDeviceEnumerator | 0x20928 | 0x67E0 | confirmed |
| IID_IAudioClient | 0x20608 | 0x3870, 0x7D2A | confirmed |
| IID_IAudioRenderClient | 0x20618 | 0x3870 | confirmed |
| IID_IAudioCaptureClient | 0x20628 | 0x3870 | confirmed |
| IID_IAudioClock | 0x20638 | 0x3870 | confirmed |
| IID_IMMNotificationClient | 0x20908 | direct xref not found in first pass | GUID present |

These are GUIDs for standard Windows interfaces. Presence of an IID proves a static dependency but **does not** prove how the interface is used, what concrete audio format was selected, or what the runtime call sequence was.

## Confirmed assembly snippets (conceptual, no original bytes republished)

- At 0x6823 / 0x682A, a COM creation call passes addresses 0x20918 (CLSID_MMDeviceEnumerator) and 0x20928 (IID_IMMDeviceEnumerator) to imported `CoCreateInstance`.
- At 0x38DA, a pointer to IID_IAudioClient (0x20608) is passed to a virtual call at offset +0x18 on a COM object.
- At 0x392B the code caches an integer rate-like input in port object offset +0x60; that is a fact about the instruction, but the precise field semantics require tracing.
- Within 0x3870, later indirect COM method calls access the resulting interface pointer. The detailed `IAudioClient::Initialize`, `GetBufferSize`, `GetService`, event setup, and buffer transfer still need full vtable tracing.

## Inferred path (work in progress)

`CAsio::createBuffers (0x1C90)` -> worker/config `0x92B0` -> `CMMAudioPort` setup `0x3870` -> WASAPI interfaces `IAudioClient`, `IAudioRenderClient`, `IAudioCaptureClient`, `IAudioClock`.

**Caveat:** `0x92B0` invokes 0x3870 under a flag check, so the arrow is a conditional call path, not proof that every buffer setup follows that path.

## Modernization relevance

The actual target is shared-mode audio with browser audio concurrently. `IAudioClient3` GUID was not found in the original, but absence from bytes does not alone prove its API is never used dynamically. Even if a modern API is available, the user's device previously reported a shared-mode minimum/default period of 10 ms, so changing APIs alone does not demonstrate an improvement.

Next: recover the conditional shared-mode vs exclusive-mode flag, the exact interface vtable calls, the callback-to-WASAPI packet handoff, and evidence of underruns.

## Evidence caveats

This is a partial reconstruction. No binary patch was performed and no playback speedup has been measured.
