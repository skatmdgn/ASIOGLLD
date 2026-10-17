# Batch 15 continuation status

**Priority:** faithfully reconstruct original x64 asioglld.dll *before* ANY optimization; retain capture/render, shared/exclusive, COM/ASIO ABI, errors, UI, configuration, callbacks. Large local batches; ONE GitHub commit after batch; CI only at final validation.

Original unchanged SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd` (173056B). Original duplicate independently same hash.

New discoveries: TWO distinct IMMNotificationClient vtables at 0x208C8 and 0x209A8 and their different 5 notification callbacks. Config OnDeviceStateChanged invokes asioMessage(3) only if config+0x68 has ASIOCallbacks, installed at 0x7C8D after successful buffer validation, cleared on disposeBuffers 0x1DA6. Worker notification handles 4 device events with 0x8F20, clearing worker active flag then stopping each bit4 Started port's IAudioClient, clearing bit4 even on stop failure; property change no-op. Port Start bit4 set at 0x9277 only if IAudioClient::Start S_OK, simulated port can bypass. Worker register/unregister+COM refcount paths from 0x1080 ctor to 0x12C0 destructor, and config registration 0x682A/0x687D with cleanup 0x6674/0x1428. Registration HRESULT is ignored at those sites.

Evidence in conversation artifact `ASIOGLLD_Original_Recovery_Batch15.zip` (NO original DLL): 291 byte pin CSV, 44 operand pairs, 16 direct edges, two exact COM 8-slot vtables, two IIDs, 10 CFG windows=108 blocks/117 edges/31 call sites, C++ candidate layouts and Python local behavior model. 32 new + 224 old = **256/256 executed pass, 0 skipped**; strict original SHA checks; no Windows binary tests. Original not modified, no CI or optimization.

Unresolved and NOT justified as complete: Ghidra decompile, concurrent COM ownership and registration failure paths, async device-state callbacks, full ASIO clock and WASAPI errors, Windows original execution, complete native replica, original/replica parity. Do not infer restoration percentage from tests. Original textual C++ cannot always be recovered.

Resume from main and companion Batch15 ZIP. User only wants Phase1 original fidelity now.
