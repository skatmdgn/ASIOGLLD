# Batch 12: Original IASIO interface contracts

Original DLL SHA-256: e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd; 173056 bytes x64. All addresses are original RVAs. STATIC RECONSTRUCTION ONLY; NOT ORIGINAL C++ SOURCE OR RUNTIME PARITY.

| Slot | Method | RVA | Original implementation evidence |
|---:|---|---:|---|
| 0 | QueryInterface | 1050 | COM lifetime still partially unresolved |
| 1 | AddRef | 1060 | COM refcount |
| 2 | Release | 1070 | COM lifetime |
| 3 | init | 16B0 | Windows OS version branch and timeBeginPeriod(1) |
| 4 | getDriverName | 1650 | Writes original 32-byte name if output pointer nonnull |
| 5 | getDriverVersion | 1690 | Returns cached CAsio+0x9C |
| 6 | getErrorMessage | 16A0 | Bare return stub; does NOT fill error string |
| 7 | start | 1740 | No worker or 0x8FC0 false: ASE_NotPresent(-1000); else 0 |
| 8 | stop | 1770 | Deactivate and stop clients on flagged ports, returns 0 |
| 9 | getChannels | 1910 | Two valid outputs needed (-998 otherwise), values cached +0x48/+0x4C |
| 10 | getLatencies | 1930 | 2*cached buffer size written for both input/output, null -998 |
| 11 | getBufferSize | 1C50 | All four output pointers needed; positive cached size written to min/max/preferred/GRANULARITY. Size <=0: -1000 |
| 12 | canSampleRate | 1AD0 | Truncated double; all eligible port rate lists must match, else -997 |
| 13 | getSampleRate | 1AA0 | Cached CAsio+0x44 converted to double if positive, otherwise -995 |
| 14 | setSampleRate | 1960 | Compare cached rate, validate at 85D0, update config, acquire registry helper, optional asioMessage(3) |
| 15 | getClockSources | 1BD0 | Unconditionally writes single Internal clock (index=0,group=0,channel=0,current=1), count=1 |
| 16 | setClockSource | 1C00 | Index 0 ->0; any other index -> -998 |
| 17 | getSamplePosition | 17E0 | Block/clock calculation; absent port path may return 0 without writing values |
| 18 | getChannelInfo | 1C10 | Null info or negative index -> -998; 86D0 failure -> -1000 |
| 19 | createBuffers | 1C90 | Invalid arguments -> -998; failed setup 7A80 -> disposeBuffers then -994; following 92B0 -> unconditional 0 |
| 20 | disposeBuffers | 1D40 | Stop worker, traverse both port lists, clear worker callback state, return 0 |
| 21 | controlPanel | 1DC0 | Calls 8D60 on config, returns 0 |
| 22 | future | 5FA0 | Shared zero-return stub |
| 23 | outputReady | 5FA0 | Same stub |

Original distinctions to preserve instead of normalizing: granularity reports actual fixed buffer size; getClockSources performs no null check before writes; getChannelInfo may mutate isActive/group/name before unsupported-width error; setSampleRate can mutate its config before registry helper failure. Actual invalid-pointer behavior must NOT be probed without safe Windows testing.

Locally verified 24/24 vtable slots, 206 original opcode pins, seven direct CALL edges, three embedded strings; 19 bounded method/helper CFG windows yielded 152 basic blocks and 198 intra-window edges. The full reproducible verifier, 206-raw-opcode CSV, CFG and 43 new tests are in the companion Batch12 ZIP. No Ghidra whole-DLL run, original Windows execution, fully faithful DLL or parity tests. No optimization, no CI.
