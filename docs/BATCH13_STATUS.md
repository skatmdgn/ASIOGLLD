# Batch 13 continuation — original-first, CI deferred

User instruction: fully reverse engineer and faithfully reproduce original asioglld.dll, including ASIO COM, WASAPI shared/exclusive, input/output, timing, GUI, errors and object lifetime, before any optimization. Do substantial local analysis and tests; commit once at end; delay CI to late/final validation. Never overwrite installed original.

Original x64 DLL: 173056 bytes; SHA-256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd; both uploaded copies match.

Batch13 traced 0x6B6E/0x6B84/0x6B97/0x6BAA -> 0x7D00 -> IAudioClient Activate/IsFormatSupported -> 3-level per-mode rate/channel/depth tree, successful-format snapshots +0x48 and nested trees +0x50/+0x58. Source candidate sample rates (44100,48000,96000), 2 channels, channel mask 3, 16-bit PCM; NOT guaranteed hardware support. Registry overrides remain a separate original path. Nested recursive destructor helpers at 0x4E20,0x4E50,0x4EA0, called from 0x2E80–0x3053.

8 static CFG windows: 323 physical basic blocks, 467 intra-window branch edges; local package contains original-exact 116 opcode pins, 20 direct calls, original data tables, JSON and C++ candidate layout. 38 new tests and all 154 earlier tests rerun PASS = 192/192, no skipped. This measures static evidence/model consistency ONLY.

NEXT major blockers: Windows Ghidra full decompiler export and native runtime tracing (with user approval/registry backup); interprocedural dataflow/indirect calls, entire registry/UI/per-device format policy and fail paths, all COM lifetimes; complete independent native original-behavior replica and full parity suite. Do not claim source-code 100% restoration, numeric % based on partial tests, or performance improvements.

CI 0; optimization 0; original binary untouched.
