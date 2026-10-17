# Batch 10: original binary physical CFG coverage

| Analyst-defined RVA window | RVA | Basic blocks | Intra-window edges | CALL positions |
|---|---|---:|---:|---:|
| IASIO getSamplePosition | 0x17E0 | 17 | 24 | 0 |
| WASAPI Initialize | 0x3870 | 51 | 78 | 16 |
| WASAPI Render | 0x4020 | 66 | 104 | 9 |
| WASAPI Capture | 0x4380 | 24 | 35 | 11 |
| COM factory CreateInstance | 0x1F80 | 29 | 16 | 5 |
| AudioPort getTime | 0x4610 | 13 | 19 | 3 |
| Worker thread entry | 0x8F80 | 5 | 5 | 1 |
| Worker start | 0x8FC0 | 40 | 65 | 9 |
| Worker createBuffers | 0x92B0 | 32 | 52 | 10 |
| Worker stop | 0x94B0 | 25 | 38 | 13 |
| Worker bufferSwitchTimeInfo | 0x9610 | 14 | 21 | 3 |
| Worker polling | 0x97B0 | 35 | 55 | 11 |
| **Total** | | **351** | **512** | **91** |

Within these 91 calls: **27 direct**, **23 IAT-imported**, **41 unresolved-directly-via-IAT indirect** (some of the 41 have static interface hypotheses in earlier batch records). Do not confuse this scope with the previously classified 164 non-IAT indirect calls across the entire original DLL.

Method: SHA-pinned x64 PE parser + GNU objdump, basic-block boundaries at local branch destinations and terminators. Linear disassembly and manually bounded physical windows: **not** high-level function reconstruction, actual Windows flow coverage, indirect jump resolution, or COM type proof. Full script, 12-window JSON CFG (block/edge/call positions), call CSV, and 75 pinned original byte addresses are preserved in companion `ASIOGLLD_Original_Recovery_Batch10.zip`; original DLL bytes excluded.

Original untouched. **No optimization, CI, replica binary or parity claim.**