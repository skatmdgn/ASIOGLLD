# Static coverage ledger — current pass

All counts are from the user's original binary and Stage 1 `function_map.json` / GNU objdump direct-CALL extraction; none is 'complete functions reconstructed'.

| Evidence category | Count | Meaning |
|---|---:|---|
| x64 PE .pdata unwind address ranges | 590 | Unwind entries, not high-level function count |
| Decoded linear instruction rows | 33,194 | A disassembler pass, may include code/data ambiguity |
| Distinct caller→target direct CALL edges | 983 | Indirect calls excluded |
| Distinct direct CALL target RVAs | 304 | Direct target addresses only |
| Direct CALL targets outside all unwind ranges | **67** | Leaf-function/thunk/helper candidates to inspect individually |
| RTTI-backed IASIO vtable slots | 24 | ABI addresses identified, not bodies reconstructed |
| Verified WASAPI COM indirect callsites | 17 | Fixed addresses and ABI offset matching only |
| Verified standard audio GUIDs | 6 | Binary GUID references, not runtime proof |

## Known omissions

- Leaf functions not listed by .pdata (for example 0x23F0).
- Compiler funclets split across adjacent .pdata ranges (for example 0x4380–0x460C).
- Calls through vtables, callbacks, exports, message dispatch, jump tables, thread entrypoints and dynamically resolved APIs.
- Cold/unreached code, errors, resources, configuration UI, ASIO inputs/outputs and all variations in operating environment.

**No static metric above constitutes complete reverse engineering.** The next full coverage audit must classify every reachable basic block and unresolved target, documenting non-executable sections and intentionally unreachable code as well.

## Original first

No optimization and no new replacement API. Reproduce the original's algorithmic behavior, validate runtime and compare before modernization.
