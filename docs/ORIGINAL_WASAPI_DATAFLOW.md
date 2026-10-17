# 원본 WASAPI 오디오 경로 — 기계어 기반 복원 2차

입력: 사용자 원본 `asioglld.dll` SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd` (173,056 bytes, x64).
**Phase 1만:** 원본 기능 그대로 복원. 최적화/대체 API/기능 생략 금지.

## 1. 초기화 경로 (0x3870–0x3CAB)

| 호출 RVA | COM ABI 근거 | 원본 호출 |
|---|---|---|
| 0x38E6 | IMMDevice vtable+0x18 | Activate(IAudioClient) |
| 0x390C, 0x39BF | IAudioClient+0x48 | GetDevicePeriod |
| 0x39D3, 0x3B28 | IAudioClient+0x28 | GetStreamLatency |
| 0x3B0C | IAudioClient+0x18 | Initialize |
| 0x3B7A | IAudioClient+0x20 | GetBufferSize |
| 0x3BC5 | IAudioClient+0x70 | GetService(render/capture) |
| 0x3BE2 | IAudioClient+0x70 | GetService(IAudioClock) |
| 0x3C00 | IAudioClient+0x60 | Reset (conditional) |
| 0x3C2E | IAudioClient+0x68 | SetEventHandle |

Static GUID bytes: IID_IAudioClient @0x20608, IID_IAudioRenderClient @0x20618, IID_IAudioCaptureClient @0x20628, IID_IAudioClock @0x20638; all verified against their standard GUID values.

The original builds a WAVEFORMATEXTENSIBLE structure: wFormatTag 0xFFFE at 0x3A2A, cbSize 22 at 0x3A23, PCM subtype GUID @0x20648. **Do not infer that this is the only possible format.**

At 0x3BAD/0x3BBA, the port mode field +0x80 selects RenderClient service vs CaptureClient service. Shared/exclusive and event-init branches in 0x3Axx–0x3Bxx remain under analysis; don't simplify them.

## 2. Real render path (0x4020–0x4377)

- Port field +0x38 holds IAudioRenderClient after GetService.
- 0x40D7 calls `IAudioRenderClient::GetBuffer` (+0x18).
- 0x424B calls `IAudioRenderClient::ReleaseBuffer` (+0x20).
- Internal sample movement/conversion is visible between them; complete format-dependent data flow **UNRESOLVED**.

## 3. Real capture path (0x4380–0x460C)

- Port field +0x30 holds IAudioCaptureClient.
- 0x44EA calls `IAudioCaptureClient::GetNextPacketSize` (+0x28).
- 0x4580 calls `IAudioCaptureClient::GetBuffer` (+0x18).
- 0x45D5 calls `IAudioCaptureClient::ReleaseBuffer` (+0x20).
- **Important exception-table caveat:** one connected code path crosses four .pdata ranges: [0x4380,0x4393), [0x4393,0x43F4), [0x43F4,0x4401), [0x4401,0x460C). Thus **590 unwind entries ≠ 590 independent functions**. The branch at 0x4391 jumps into 0x4401. All ranges must be included in recovery; function total remains unknown.

## 4. Port object offsets

| Offset | Grounding | Level |
|---|---|---|
| +0x20 | used for IMMDevice::Activate/GetState | STATIC_INFERRED type, call confirmed |
| +0x28 | IAudioClient vtable calls | BYTE_CONFIRMED + ABI |
| +0x30 | GetService IID_IAudioCaptureClient output | BYTE_CONFIRMED + ABI |
| +0x38 | GetService IID_IAudioRenderClient output | BYTE_CONFIRMED + ABI |
| +0x40 | GetService IID_IAudioClock output | BYTE_CONFIRMED + ABI |
| +0x64 | flag bitfield | BYTE_CONFIRMED accesses, individual bit names unresolved |
| +0x68 | IAudioClient::GetBufferSize returned frame count | BYTE_CONFIRMED |
| +0x70 | event handle for IAudioClient::SetEventHandle | BYTE_CONFIRMED |
| +0x78 | GetStreamLatency return value used in calculations | BYTE_CONFIRMED, units/type require validation |

## 5. How to verify

`tools/verify_wasapi_calls.py` is a read-only verifier: it checks the original SHA, 6 interface GUIDs, and 17 indirect COM callsite opcodes. On the currently mounted original: 17/17, GUID 6/6, no mismatches. **This proves byte/ABI consistency only**, not program correctness, a fully decompiled function, runtime parity, or higher performance.

## 6. Remaining obligations

Analyze every original supported mode: shared/exclusive, render/capture, channel layout, format conversion, sample rates, interface lifetime, all configuration/UI, device changes, thread scheduling, exceptions and errors. Trace Windows original runtime, implement matching code without improvements, and run original-vs-replica differential tests. No optimization until the user explicitly approves after parity evaluation.
