# Batch 6 reproducible static inventory and open gaps

Full original SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. GNU objdump + PE table code were run locally in one batch, without installing/modifying the original.

| Raw structural measure | Count | Important limit |
|---|---:|---|
| PE sections | 6 | Sections are not code functions |
| Imported API entries | 148 | Mostly Windows API dependencies |
| PE exports | 5 | COM entrypoints and registration |
| x64 .pdata unwind ranges | 590 | Not equivalent to high-level functions |
| Disassembly instruction rows | 33,194 | Linear decoding may include ambiguous data |
| Distinct direct relative CALL targets | 305 | Some targets are compiler stubs |
| Direct CALL targets outside all unwind ranges | 67 | 11 import thunks, 2 return stubs, 1 jump stub, **53 unresolved candidates** |
| Candidate entrypoint anchors (union) | 677 | Neither logical function count nor recovery percentage |
| Indirect CALL instructions | 643 | 479 resolve to imported IAT, **164 still require receiver-object identification** |
| Branches crossing unwind ranges | 232 | Funclets, split ranges, other control edges |
| ASIO vtable slots validated | 24/24 | No complete behavior parity |
| Additional port/thread opcode checks | 38/38 | Raw code matches only |
| Local unit tests | 11 passed | Parser, ABI, models; **not** running-original tests |

**64-bit original not decompiled in entirety; no faithful compiled replacement and no original-vs-replica test yet.** Our larger Batch 6 ZIP includes the runnable Python standard-library original analyzer, full address-level JSON, 164 unresolved callsite queues, tests and explanations. The public GitHub repository keeps reproducible conclusions and original-independent source/tools, not the proprietary DLL or a mass-disassembly dump.

Next work: bulk Ghidra decompilation and class/dataflow recovery, Windows debugger tracing for COM/ASIO thread paths, original behavior specification, no-shortcut replica, then differential test. **No modernization and no CI workflow was run in this batch.**
