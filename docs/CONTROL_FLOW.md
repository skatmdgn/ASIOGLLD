# Partial recovered CAsio control flow — original binary

**Evidence type:** PE x64 disassembly and RTTI/vtable mapping from `asioglld.dll`, SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. Addresses are RVAs (not run-time addresses), and this is **not** the original source.

| Method | RVA | Observed code behavior | Confidence |
|---|---|---|---|
| `init` | 0x16B0 | Calls `GetVersionExA`; accepted OS branch calls `timeBeginPeriod(1)` | Confirmed |
| `start` | 0x1740 | Reads object pointer `[this+0xC8]` and invokes 0x8FC0 | Confirmed |
| `stop` | 0x1770 | Clears processing flag and traverses port list, calls an indirect virtual method at vtable offset 0x58 when needed | Confirmed instructions; meaning inferred |
| `getBufferSize` | 0x1C50 | Validates 4 output pointers, copies positive 32-bit `[this+0x3C]` into all four values | Confirmed |
| `createBuffers` | 0x1C90 | Checks arguments; calls 0x7A80 and then 0x92B0 | Confirmed |
| `disposeBuffers` | 0x1D40 | Calls 0x94B0, walks lists at `[this+0x68]` and `[this+0x70]`, invokes 0x3EA0 on marked items; zeroes `[this+0x88]` | Confirmed instructions |

## Direct call relationships

- `start 0x1740` -> `0x8FC0`
- `createBuffers 0x1C90` -> `0x7A80`, `0x92B0`
- `disposeBuffers 0x1D40` -> `0x94B0`, `0x3EA0`
- `0x92B0` -> `0x3870`, `0xC400`, `0x4E20`, `0xC370`
- `0x97B0` -> `0xC316`, `0xC322`, `0xC310`, `0x4380`, `0x4020`, `0x9610`, `0xC31C`

## Candidate CAsio state fields

| Offset | Observation |
|---|---|
| +0x3C | positive buffer-size value |
| +0x68 | first channel/port list pointer |
| +0x70 | second channel/port list pointer |
| +0x88 | pointer cleared when disposing buffers (possibly callback state) |
| +0xC8 | processing/worker state pointer |

Field names and ownership are provisional, even where instruction offsets are confirmed.

**Next unresolved challenge:** most WASAPI methods are COM vtable calls, not PE imports. Reconstruct the IAudioClient/IAudioRenderClient object identities and call sequences with indirect-call analysis and debugger traces. We have not yet located a confirmed underrun and must not call the 1 ms event wait a performance bug.
