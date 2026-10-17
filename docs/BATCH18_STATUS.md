# Batch18 handoff: all original behaviors first, defer CI

User requirement: reconstruct original Steinberg generic low-latency ASIO x64 DLL as faithfully as possible BEFORE ANY optimization. Include COM/IASIO ABI, shared/exclusive WASAPI, input/output, UI/reg, clocks, errors, ownership. Analyze in large local batches, upload to GitHub **once at end**; CI only for late/final validation. Do not overwrite original or publish full proprietary code.

Original binary: x64 173056 bytes SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`; both user copies unchanged.

Batch18 NEW evidence: `0x65DB` config → `0x67E0` setup → `CoInitializeEx(NULL,0)` at `0x6807`, no immediate HRESULT test, then `CoCreateInstance` at `0x682A`. Original PE static imports do not contain CoUninitialize; **do not infer proven COM leak or imbalance**. Two listener registration HRESULT results at `0x687D`, `0x1196` not checked; cleanup guarded by object pointers, OS reference ownership still UNKNOWN. `CAsio` destructor `0x12C0–0x1475` has NO DIRECT WorkerStop(`0x94B0`) call: releases listeners, calls DeleteCriticalSection, frees worker; cannot conclude it runs while thread active. Separate paths must be traced at runtime.

Batch18 local evidence: 188 exact byte/operand pins; 2×8 notification vtable slots, 6 imported API calls; 9 code windows with 197 basic blocks, 273 edges and 77 CALL positions; candidate Win64 struct layout compiler PASS. 35 new + 322 all previous local tests **357/357 PASS with 0 skipped**. This does NOT imply fidelity or a running DLL.

Detailed original-dependent audit, byte CSV, 9-window flow, all test results and Windows Ghidra plan are in `ASIOGLLD_Original_Recovery_Batch18.zip` from this conversation. Public GitHub stores only nonproprietary reproducer, model and summary.

NOT DONE: Windows Ghidra whole-DLL decompile, full CFG/COM ownership/exception recovery, original runtime trace with user consent, independent native replica and Cubase original-vs-replica parity. **No CI and no optimizations.**
