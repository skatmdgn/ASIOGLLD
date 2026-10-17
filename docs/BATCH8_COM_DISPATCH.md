# Batch 8 — Original COM dispatch and device lifecycle reconstruction

Source is SHA-pinned **original** x64 `asioglld.dll`: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`.

## Outcomes (STATIC_INFERRED, not runtime or function-level completion)

- Original non-IAT indirect CALL positions: **164**.
- Earlier ABI/method candidates: **30**.
- New Batch8 candidates linked to COM vtable slots and object/receiver origins: **75**.
- Total static method candidates: **105**, unresolved: **59**.
- All **75** new positions are in `analysis/BATCH8_NEW_CALLS.csv` with exact call RVA, proposed interface and method, vtable slot and instruction RVA of the nearby receiver/object load.
- `tools/batch8_validate_static.py` checks the original file SHA and 75 call-site slots and receiver anchors. **The full original-instruction argument checks and all 164 rows, including unresolved sites, are in the companion Batch8 ZIP.**

These 105 are *call positions*, not original C++ function count, and **105/164 is not a restoration percentage**.

## Recovered original paths

- `0x682A`: create IMMDeviceEnumerator. `0x687D`: RegisterEndpointNotificationCallback; `0x6674` / `0x1428`: Unregister.
- `0x8981` EnumAudioEndpoints → `0x89A7` GetCount → `0x89E4` Item → `0x8A24` collection Release. `0x8AB0` separately queries GetDefaultAudioEndpoint.
- `0x49F0` IMMDevice::OpenPropertyStore → `0x4A24` IPropertyStore::GetValue → `0x4A9C` Release; `0x4AB4` IMMDevice::GetId. The PROPERTYKEY at original RVA 0x20798 is **PKEY_Device_FriendlyName**, GUID `a45c254e-df1c-4efd-8020-67d146a850e0`, PID **14**, confirmed by raw bytes.
- `0x7D99` IMMDevice::Activate with IID_IAudioClient, `0x7DC7` GetDevicePeriod and `0x7F59` IsFormatSupported.
- `0x9270` IAudioClient::Start and `0x17BA` / `0x8F5B` Stop; `0x916D` IAudioClock::GetPosition and `0x918F` GetFrequency.
- Multiple IAudioClient, IAudioCaptureClient, IAudioRenderClient, IAudioClock and IMMDevice Release paths in `0x2E80–0x2F77` and `0x7600–0x7800`. Branch conditions determine actual lifetime: **not** evidence of double-free.
- Original IASIO::createBuffers failure path at **0x1D04** calls `disposeBuffers` through its own IASIO vtable slot **+0xA0**.
- ASIOCallbacks::asioMessage(3 = kAsioResetRequest) at `0x1A23`, `0x5F91`, and `0x8E5C`.

## Verification

Local tests re-run: Batch6 **11**, Batch7 **9**, Stage5 **4**, Batch8 **11**; total **35/35 passed**. These validate Python analysis, hash identity, original instruction slots and model consistency. **No Windows-running DLL comparison or faithful recompiled replica yet.**

## Required follow-up

59 unresolved non-IAT indirect call positions; complete original CFG and code/type/data recovery; Ghidra bulk decompilation; Windows original runtime verification; independent no-shortcut replica; differential ASIO/COM/WASAPI parity tests. No original binary bytes or verbatim decompiler dumps committed. **No CI, no optimization, no original modifications.**
