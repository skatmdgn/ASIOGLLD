# Batch23 continuation — original-first native implementation starts

Standing user request: NO optimization or reduced ASIO driver. Restore original x64 Generic Low Latency ASIO Driver COM/IASIO ABI 24 slots, WASAPI shared/exclusive input/output, device enumeration and notification, UI/registry, timing and failure/lifetime paths. Large local batches, ONE final GitHub commit; CI at final verification only.

Original Win64 DLL: 173056 bytes, SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd; duplicate byte-identical; both UNMODIFIED.

New Batch23: 13 previously unspecified runtime CALL sites verified against 55 exact opcode/operand locations, eight direct calls. Source classes: zeroextended-imagebase 2 (0x10654,0x10743), C++ EH callback table 2 (0x1092D,0x1095C), DecodePointer 2 (0x10C7E,0x10C85), CRT thread-state callbacks 2 (0x13B45,0x170FD), signed-relative EH 4 (0x17AF4,0x183CA,0x183F9,0x18EE0), original incoming-argument pass-through 1 (0x1D06E). All 13 runtime *final callee addresses remain unknown*. Do not claim named methods or source text recovery.

Actual standalone C++17 code authored/compiled/tested for input-valid PCM 0x23F0/0x24C0/0x2900/0x2B5F and x64 EH/CRT field arithmetic and offset layout. 2 CTest native executables passed, 336 synthetic C++/Batch11-Python model comparisons matched. No native ASIO DLL yet, no Windows execution, no original-vs-replica parity.

New 34 original-byte/static Python tests + Stage5–Batch22 506 old tests rerun => 540/540 executed PASS, 0 skipped. Batch22 stored SUMMARY snapshot has post-test extra metadata: initial direct regression gave 44/45; isolated copy of old suite reran the original batch22 auditor and normalization, then 45/45 passed, source Batch22 files untouched. Do not hide this test-run history.

Full 48-file Batch23 ZIP in this conversation contains source code, exact byte/operand CSV, C++ ABI headers, CMake, tests, logs. Public repo provides native source/tests and auditable metadata; no original DLL or mass disassembly.

NEXT actual Ghidra Windows headless to verify remaining final runtime callback identities, then continue porting validated IASIO and WASAPI functions to faithful C++ independent DLL; progressively test parity on real Cubase8/Realtek before declaring full original equivalent. CI/optimization 0; original mutation 0.
