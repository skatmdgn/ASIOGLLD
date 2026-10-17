# Batch23 — original C++ runtime 13 indirect-call origins

Original exact Win64 DLL 173056 bytes, SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. Original SHA pinned, bytes untouched. **STATIC provenance, not original Windows execution, not final callback pointers or full ASIO binary.**

## Recovered original CALL address provenance

| CALL RVA | Static source evidence | Final runtime callback |
|---|---|---|
| 0x10654 | mov eax,[rbx] then add rax,r14 (ZERO extend) | not fixed |
| 0x10743 | mov r8d,[rbx-4] then add r8,r14 (ZERO extend) | not fixed |
| 0x1092D / 0x1095C | r9 from runtime table entry +8, sentinel checks | not fixed |
| 0x10C7E / 0x10C85 | r13 from DecodePointer helper 0xD000, precall 0x10B42/0x10B47 | not fixed |
| 0x13B45 | runtime thread state pointer +0xD0, guarded by null | not fixed |
| 0x170FD | runtime thread state pointer +0xE0 | not fixed |
| 0x17AF4 | C++ EH record magic 0xE06D7363, signed-relative throw callback offset + supplied base | not fixed |
| 0x183CA / 0x183F9 | 0x16DD0 returns stored thread-state image base (+0x130); movsxd metadata+0x18 plus base | not fixed |
| 0x18EE0 | C++ EH code/version guard, 0x16DD0 base + movsxd [throwInfo+8] | not fixed |
| 0x1D06E | incoming rcx callback copied to rax; 0x14320 sets r9=0x19930520 but doesn't alter rax; call rax | not fixed |

**Critical correction:** Both 0x10654 and 0x10743 perform 32-bit **zero extension**, NOT signed extension; 0x183CA/0x183F9/0x18EE0 use `movsxd` and must be treated differently.

The original-instruction auditor verified **55 exact instruction/operand positions**, **eight direct CALL links** and all **13 indirect CALL registers** on both identical original copies. None of 13 has a fully determined final runtime callee; do not misrepresent address provenance as source-level restoration.

## Native C++ actual implementation progress (PARTIAL)

In this batch there is an independently CMake-buildable **C++17** implementation of:
- Original-normal PCM byte widths 1/2/4 per-channel scatter (RVA 0x23F0), gather (0x24C0), 2x16bit capture (0x2900), signed-IDIV nonmodulo ring advance (0x2B5F); separate ABI-free C++ modules, not a substitute driver.
- Original runtime image-relative pointer calculations: zero extended vs signed relative32, C++ EH magic and version gates, candidate x64 CRT thread-state +0xD0/+0xE0/+0x130 and EH record fields.

Two actual CTest binaries compiled in Debug and passed. **336 synthetic C++ PCM inputs/outputs matched the earlier Batch11 Python original-normal semantic model byte-for-byte.** This is ONLY **model-vs-model** matching, NOT original DLL parity. The original binary was never executed in Windows; there is no full independent ASIO DLL.

**Regression**: all previous 506 Python tests plus 34 new = **540/540 executed pass, skipped 0**. Prior Batch22 snapshot contained extended reporting metadata compared to old baseline; isolated copy of that test suite reran its original auditor to normalize the expected JSON and then all 45 passed, without modifying original Batch22 files. Two native CTest programs and 336 C++/Python cross-model comparisons passed separately.

Companion `ASIOGLLD_Original_Recovery_Batch23.zip` has 48 files: full SHA-pinned 55-site original verifier, 13-site CSV and instruction evidence, independent C++ modules, native CLI, CMake, tests and comprehensive previous regression logs. The original DLL and mass-disassembly were deliberately excluded. No CI, no optimizations, no original modifications.

**Next:** actual Windows Ghidra whole-original decompilation, runtime callback type validation, complete original IASIO/COM/WASAPI/UI/lifetime implementation, original-vs-replica real Cubase8/Realtek parity and only then optimization.
