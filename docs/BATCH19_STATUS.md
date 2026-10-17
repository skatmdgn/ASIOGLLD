# Batch19 resume checkpoint

USER REQUIREMENT: original x64 asioglld.dll original-fidelity recovery first; COM/IASIO, full WASAPI shared+exclusive and render+capture, UI/registry, clock, errors, device callbacks and ownership. No performance optimization until original functional parity; large offline local batches then one GitHub commit; CI deferred.

Original: 173056 B; SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`, duplicate unchanged.

Batch19 new: parsed ALL 590 .pdata RUNTIME_FUNCTION records and UNWIND_INFO x64 flags. 221 CHAININFO triples exactly match existing records; 369 parentless root groups, 76 multiple segments. EH/UH handler mappings 84 -> 0x105C0(30), 0x12510(42), 0x16F80(12). Entire original static physical CFG 590 windows, 6331 basic blocks / 8807 within-window edges; 240 exits = same-root 224, other-root 9, unresolved indirect 7. CALL sites 2097 = direct text 1453, direct other 1, IAT 479, non-IAT indirect 164. 67 direct-call targets not in pdata; 148 unique IAT slots. 30 new + 357 prior = 387/387 original-pinned static/synthetic tests pass, no skipped.

COMPANION: verified `ASIOGLLD_Original_Recovery_Batch19.zip` from conversation, 39 files, includes complete script, 369 root/590 segment + 2946 call/jump CSV, CFG, tests, logs, Windows Ghidra export script and offline functions.tsv bridge. Full Ghidra NOT RUN because not installed. Do not conflate 369 unwind roots with 369 original source functions.

NEXT must do: Ghidra whole-DLL decompile in Windows private environment with SHA-pinned original, bridge Ghidra TSV to these unwind roots, classify exception funclets, remaining 7 indirect JMP/164 non-IAT CALL, trace callbacks and GUI/error methods, build independent native original-fidelity DLL with strict tests, then Windows Cubase original-vs-replica parity. No original patch/install/Windows runtime/CI/optimization so far.
