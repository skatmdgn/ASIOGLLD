# Batch 12 continuation checkpoint

USER DIRECTIVE: Restore the original asioglld.dll as faithfully as possible, including ALL ASIO, WASAPI shared/exclusive, input/output, COM, UI/settings, clocks and failure paths. Do not optimize or substitute incomplete shared-only implementation. Analyze locally as much as possible, then one GitHub commit, CI deferred to final validation.

Original: SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd; 173056 bytes; both uploaded originals same hash; original untouched.

Batch12 achieved: 19 original IASIO method/helper bounded CFG windows, 152 blocks, 198 internal branch edges, 17 CALL positions; 206 fixed machine instruction pins, 7 direct CALL edges, 24 vtable entries, three embedded string constants verified. Newly reconstructed getClockSources, getChannelInfo 16/24/32-bit channel semantics and partial writes, all-port sample-rate gate, registry helper failure and partially updated setting. Original Windows ABI struct candidates compile-time verified.

New local tests 43 passed; Batch11 previous regression chain 111 passed; TOTAL 154/154 local tests, 0 skipped. This only establishes static evidence/models, NOT Windows original parity. No original DLL executed/installed, no Ghidra present in Linux runtime, no full replica, no parity, no CI, no optimizations.

Companion artifact: ASIOGLLD_Original_Recovery_Batch12.zip contains complete 206-site verifier/CFG extractor, 19-window JSON, independent contract model, 43 tests, previous-regression log, C++ candidate ABI header and Korean docs. Public repo has permanent summary, reproducible abbreviated source and next steps; private original DLL bytes/decompiler dump not committed.

NEXT: Run Ghidra headless on Windows original, verify all 590 .pdata ranges and leaf/funclet boundaries, reconstruct per-device port rate list creation and state flags, intercept original ABI safely with user approval, reconstruct all remaining errors/object lifetimes, THEN build original-equivalent independent DLL and measure parity. No performance optimization until Phase1 completion and user approval.
