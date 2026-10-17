# Batch22 original-fidelity recovery checkpoint

USER PRIORITY: Reconstruct full original x64 Steinberg Generic Low Latency ASIO driver behavior before any performance optimization. Restore all COM/IASIO, shared/exclusive WASAPI, inputs/outputs, UI/configuration/registry, timing, notifications, errors and object lifetime. Work locally in substantial batches; ONE GitHub commit at end; no CI until near final validation. Do not upload, install, modify or bulk publish the proprietary original DLL or disassembly.

Original Win64 DLL size 173056B; SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd; both original copies verified unchanged.

Batch22 NEW: verified original GetProcAddress/EncodePointer/cache/DecodePointer provenance and actual optional API names of 6 sites: GetProcessWindowStation 0x10FB2, GetUserObjectInformationA 0x10FD5, GetActiveWindow 0x1102E, GetLastActivePopup 0x11051, MessageBoxA 0x1107B, InitializeCriticalSectionAndSpinCount 0x13CA4 (or original fallback 0x13BD0). IMPORTANT last function has decoded cached path and new GetProcAddress path; they are not a single mandatory serial Encode→Decode path. Old Batch21 unknown 19: 4 named, 2 more DecodePointer predecessor proofs (0xEB79,0xF2DD), 13 still UNRESOLVED runtime callback targets, with some general register/source-pattern evidence only. Of new API names 2 had already been categorized as decoded-pointer calls in Batch21. All 164 original indirect CALL opcodes were reverified.

Local 45 newly executed tests + 419 earlier tests + Batch21 42 rerun = **506/506 PASS, zero skipped**. SHA-pinned original and duplicate yielded byte-identical two CSV and one JSON summary; C++17 x64 function-pointer header syntax/type checks PASS. Companion ZIP ASIOGLLD_Original_Recovery_Batch22.zip contains comprehensive 164-site auditor, original evidence, detailed Korean docs, test runs, candidate C++ WinAPI types. NOT a substitute native ASIO DLL.

NEXT: Actually run Ghidra headless Windows exporter with user review and reconcile unknown 13 C++ CRT/exception callback targets (prior Batch19/20 unwind CFG data), then trace remaining native IASIO/WASAPI path with real original runtime and build fully faithful independently compiled DLL; test Cubase8/Realtek parity before *any* optimizations.

NO Ghidra actual whole-original decompilation, NO original Windows execution, NO fully functional compiled replica, NO runtime parity, NO CI, NO optimization.
