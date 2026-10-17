# Batch 13 — original WASAPI capability tree and lifetime

Source: user-supplied original x64 asioglld.dll, 173056 bytes, SHA-256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd. All addresses are RVAs. This is evidence-backed STATIC analysis, not original developer C++ and not running-original/replica parity.

## Newly traced original chain

At RVAs 0x6B6E / 0x6B84 / 0x6B97 / 0x6BAA the driver invokes function 0x7D00 four times: modes 1,1,0,0 across the two audio endpoint lists.

In the ordinary non-special-device branch, 0x7D99 invokes IMMDevice::Activate to obtain IAudioClient, and 0x7DC7 invokes IAudioClient::GetDevicePeriod. Function 0x7D00 builds a PCM WAVEFORMATEXTENSIBLE candidate (wFormatTag=0xFFFE, cbSize=22, subtype from 0x20648). IAudioClient::IsFormatSupported (COM slot+0x38) is called at 0x7F59. The following 0x7F5C / 0x7F5E checks require HRESULT == 0 (S_OK); S_FALSE or failing HRESULT does not enter the allocation branch.

### Original arrays, not guaranteed hardware support

- RVA 0x26640: DWORDs 44100, 48000, 96000, 0 (frequency candidates).
- RVA 0x204C4: WORDs 2, 0 (candidate channel count, sentinel).
- RVA 0x204C8: DWORD 3 (channel mask for the candidate).
- RVA 0x204DC: WORDs 16, 0 (candidate sample depth, sentinel).

Thus the visible default probing loop constructs stereo 16-bit integer PCM candidates at three sample rates (subject to control-flow assumptions and device/port state). Do NOT generalize this to 3 rates supported by every device. The user-selected per-port 16/24/32-bit values in the separate registry path 0x30C0–0x35C2 must still be reproduced; they cannot be discarded because this discovery probe uses 16-bit.

### Nested original storage

Port field +0x48 holds successful WAVEFORMATEXTENSIBLE snapshots, node allocation 0x40 bytes at 0x7F67, with rate at node+0x10 and copied format starting at +0x14.

Port +0x50 is the shared-mode supported-frequency list, port +0x58 is the exclusive-mode supported-frequency list; selector at 0x7FD7. In these lists:
- Frequency node 0x20 bytes (0x8006); next +0, rate DWORD +0x10, channel-child pointer +0x18.
- Channel node 0x20 bytes (0x805C); next +0, channel count WORD +0x10, depth-child pointer +0x18.
- Bit-depth node 0x18 bytes (0x80BC); next +0, bit depth WORD +0x10.
Existing nodes are searched and reused before insertion. Full out-of-memory branch semantics and ownership still unresolved.

Destructor function 0x2E80–0x3053 calls original recursive list releases: 0x4EA0 (rates and descendants), 0x4E50 (channels and descendants), 0x4E20 (depths). Reverse traversal / post-order cleanup is not to be freely replaced in the fidelity replica.

### Flags and settings

Port constructor instances have initial flag values 0x40 at 0x697B and 0x41 at 0x6AD6: bit0 distinguishes direction; bit6 enters a special/synthetic-port path that bypasses IAudioClient probing. bit1 is toggled by port-selection checks around 0x6F18,0x70D8 and 0x88FD/0x8905. bit2 is set in the discovery path and cleared near 0x8570; exact lifetime semantics require more tracing. These are static field observations, not assured user-facing UI semantics.

## Reproduction evidence and limitations

Original SHA pinned. Local full Batch13 package includes 116 byte-pinned original instructions, 20 verified direct-call edges, four candidate table checks, eight analyst-bounded CFG windows with 323 basic blocks and 467 in-window edges, candidate C++ struct offset assertions, Python original analyzer and synthetic behavior model.

All previous 154 local tests were rerun; 38 new tests passed; 192/192 executed passed with 0 skipped. These are static/partial-model tests, NOT original-vs-replica parity. The original DLL was never installed, modified, registered or run. Ghidra whole-DLL decompilation, Windows runtime, full original equivalence and replica are still NOT DONE. CI not run, no optimization.
