# Architecture recovery status

## Verified from the supplied original

- PE32+ x64 DLL, 173,056 bytes, 6 sections, PE timestamp 2008-07-24 (timestamp does not prove code authorship/date).
- Import table has 148 entries, including Windows audio-related COM creation (`CoCreateInstance`, `CoInitializeEx`), MMCSS (`AvSetMmThreadCharacteristicsA`, `AvSetMmThreadPriority`), WinMM timer (`timeBeginPeriod`), event operations and critical sections.
- .pdata unwind table has 590 function *ranges*. The real function total can be larger due to leaf functions, thunks and other unrecorded code.
- 33,194 disassembler-decoded instruction rows and 983 direct call edges in first-pass static analysis; no claim of exhaustive control-flow recovery.
- RTTI identifies `CAsio`, `IASIO`, `CClassFactory`, `CMMAudioPort`, `CWasapiConfig`, `CNotificationClient`, `CNotificationClient2`.
- Config strings directly present in original include `ExclusiveMode`, `SharedModeChannels`, `ExclusiveModeChannels`, `BufferDuration`, `UserDefinedBufferSize` and `SampleRate`.
- `Pro Audio` and `MyWasapiEvent` are present; direct AVRT-related calls are also imported.

## Investigative targets (not yet reconstructed)

1. CAsio init/start/stop and COM factory state transitions.
2. Enumeration of IMMDevice endpoints; creation/activation of IAudioClient and IAudioRenderClient.
3. WASAPI shared/exclusive selection, formats, sample-rate handling and endpoint opening.
4. ASIO double buffer to WASAPI packet transfer, any buffering/conversion or resampling.
5. Event/thread/critical-section scheduling and actual real-time callback deadline misses.
6. Configuration persistence and backward compatibility.
7. Teardown, device loss, recovery and concurrent Windows audio streams.

## Important correction: event polling

`WaitForSingleObject(..., 1ms)` was observed at RVA 0x988A in a function beginning around RVA 0x97B0. The surrounding assembly traverses linked port objects and applies an event/bitmask-based dispatch. It is **not proven to be the audio output delivery loop** or a performance defect. No change to that constant should be made without a runtime call trace.

## Observed environment (not proof about this DLL)

- User's Windows 11 Realtek device reports 10 ms default/minimum WASAPI shared period and 22 ms stream buffer at 48 kHz.
- Shared-mode silence playback test logged zero API timeouts during 120 s, whereas Cubase on a heavy project still has intermittent dropouts and historically high Average Load.
- Exclusive mode is not the target because Cubase must coexist with YouTube and other applications.

## Confidence levels

- **CONFIRMED**: raw bytes, PE directories, imports, exports, RTTI, pointer table locations.
- **INFERRED**: object responsibilities, class relationships beyond RTTI, guessed control-flow role.
- **REFERENCE_ONLY**: patterns suggested by FlexASIO or official ASIO SDK.
- **UNVERIFIED**: anything about CPU gains, latency reductions or playback dropouts without reproducible A/B test.

Sources: original user-supplied DLL, official ASIO SDK (audiosdk/asio), FlexASIO repository. Proprietary DLL bytes deliberately excluded from GitHub.
