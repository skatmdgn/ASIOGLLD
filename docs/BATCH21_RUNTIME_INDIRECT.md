# Batch 21 — 164 original non-IAT indirect CALL provenance review

Original x64 DLL: 173056 bytes; SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. All RVAs refer to that exact original and all conclusions are **static**. Original DLL unchanged and never executed. This is NOT complete decompiled source, Windows runtime parity or an ASIO replica.

## Previously unresolved 59 sites reviewed

Previous 164 CALL sites: 105 had original-static ABI or COM receiver evidence (NOT confirmed runtime identity), 59 remained unresolved. Batch21 rechecked all 164 original opcodes and categorized the 59 remaining sites as:

- **17 driver/COM/factory-lifetime-related**: CAsio factory `0x204E AddRef`, `0x205D QueryInterface`, `0x206A Release`; `0x1FFF` factory-provided allocator callback; `0x2031` failure deleting destructor. Stored config list receivers `0x13F5`/`0x140A`/`0x6646`/`0x6659` invoke COM-style vtable +0x10 Release, but **their exact interface identity remains unresolved**.
- **42 runtime/CRT/SEH/initialization-related**: only **6** have a pinned named API call or original immutable code-pointer target. The other **36** still have no statically fixed concrete runtime callee. The 36 comprise 8 decoded callback pointers, 5 callback-array calls, 4 mutable callbacks and 19 insufficiently attributed callsites.

## Named APIs found through original strings and imports

- Native runtime helper at `0xCE40` and `0xCF10` resolves `KERNEL32.DLL!EncodePointer` via `GetModuleHandleA` and `GetProcAddress`; `0xCEF6` and `0xCFD5` invoke it, with FLS cache / fallback branches. Helper `0xD000` resolves `DecodePointer`; `0xD0B6` invokes it. **Do not confuse these CRT security APIs with WASAPI.**
- Eight further CALL sites (0xC345, 0xDAFD, 0xEB9F, 0xEBBF, 0xF7C9, 0x1102E, 0x11051, 0x13B75) directly call a pointer returned by helper `0xD000`. The **provenance** is visible, but decoded output points to runtime-dependent callbacks and the final callee is NOT established.
- Runtime `0xF541` calls a `GetProcAddress` result for `mscoree.dll!CorExitProcess` if available. This is a conditional CLR-termination compatibility branch, not audio processing.
- Immutable original `.rdata` pointers **0x20D38→0x174B0** (called at 0xF678) and **0x20D50→0x17AC0** (called at 0x1068C) were checked against the image base and CALL RIP-relative operand. Their static target addresses are established, not full runtime semantics.

The original import names `KERNEL32!GetModuleHandleA`, `GetProcAddress`, `FlsGetValue` and original literal strings `KERNEL32.DLL`, `EncodePointer`, `DecodePointer`, `mscoree.dll`, `CorExitProcess` were also verified.

## Verification and scope

Full local companion **ASIOGLLD_Original_Recovery_Batch21.zip** contains 35 files: a GNU objdump+Python3 original-SHA-pinned 164 CALL evidence verifier, 164-site original-byte/operand CSV, previous Batch8 site provenance JSON, Ghidra targeted CALLIND Java and Windows runner (PREPARED BUT NOT RUN), synthetic and pinned 42 new tests and the complete logs for 419 prior regressions. The original DLL and full proprietary disassembly are excluded.

**42 new + 419 previous = 461/461 local tests executed and passed; 0 skipped.** Re-analysis of original and duplicate original produced byte-for-byte identical ledger and JSON. This is NOT a functional parity or restoration percentage. Ghidra absent from local runtime, so there is no real decompiled output. Windows original runtime tests, independent fully faithful DLL, original-vs-replica parity, CI and optimization are all **NOT DONE**.

Next step: run Ghidra whole-DLL headless + targeted 164 CALLIND pcode exporter on a user-reviewed original copy and join TSV with the static call ledger; classify exception/CRT callback provenance, then complete native implementation and Windows Cubase8/Realtek original-vs-replica differential tests. Exact original Steinberg C++ textual source is not necessarily recoverable from stripped binary.
