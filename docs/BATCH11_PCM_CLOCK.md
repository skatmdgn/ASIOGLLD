# Batch 11 — PCM samples and timestamp reconstruction (original first)

Source: user-owned original x64 asioglld.dll, 173056 bytes, SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd. All addresses below are RVA.

**This is evidence-backed STATIC reconstruction, not the original developers' source, not a working ASIO driver and not original-vs-replica parity. No optimization.**

## Raw sample movement recovered

| Original RVA | Instruction-backed behavior |
|---|---|
| 0x23F0 | Channel-packed samples -> designated interleaved lane; 1-, 2- or 4-byte copy; source advance by sample width and destination by width*channel stride. Called at 0x4221. |
| 0x24C0 | Inverse per-channel copy from interleaved stream to planar buffer; supports starting frame offset; widths 1,2,4. Called at 0x42FA. |
| 0x2750 | Generic capture scatter to channel buffers, per-channel cursor, min(remaining frames in chunk, requested frames), source stride=channels*sampleWidth. Called at 0x2B40. |
| 0x2900 | Dedicated 16-bit stereo deinterleave: load consecutive left/right WORDs from a 4-byte frame into separate destinations, advance both channel cursors. Called at 0x2AF3. |
| 0x2A90 | Capture ring orchestrator selecting 2ch/16bit fast path when +0x14==2 and +0x1C==2, otherwise channel-by-channel 0x2750; ring cursor and counters at 0x2B5F..0x2B88. Called at 0x45C2. |

### Candidate source object layout (not a recovered original C++ definition)

Buffer-like object: +0x04 maximum frame count, +0x08 sample width, +0x0C count of channels, +0x10 per-channel cursor array, +0x18 channel data pointers.

Capture ring-like object: +0x00 intra-frame offset, +0x04 completed/advanced blocks, +0x0C circular buffer index, +0x14 interleaved channel stride, +0x18 frames per block, +0x1C sample width, +0x20 buffer count, +0x28 buffer object pointer array. Other fields remain unknown.

Original ring update uses **signed division**, remainder added to offset, then **at most one subtraction** for frame-offset wrap, then **at most one subtraction** for circular index wrap. It must not silently be rewritten as unconditional modulo; upstream bounding behavior and corruption cases remain unresolved.

These routines copy raw integer-width samples. This does NOT prove the entire driver has no resampling or float conversion elsewhere.

## Time and clock paths

Exact little-endian 64-bit doubles in the original: RVA 0x20A98 = 9.223372036854776e18 (around 2^63), RVA 0x20AA0 = 1.0, RVA 0x20AB0 = **-1000000000.0**.

- IASIO::getSamplePosition at 0x17E0 uses worker block count * frames per block; time starts from port timestamp +0xD0 * 1000000. If worker flags bit 0 is set, correction is (port+0xC0 + 2*frames - samplePosition) * (1/sampleRate) * **(-1e9)**. Writes the 64-bit sample/timestamp as upper DWORD then lower DWORD. Its SSE float-to-64-bit extreme cases and NULL/absent-port side effects still need parity testing.
- Worker callback function 0x9610 uses a corresponding time-correction sequence, writes ASIOTime timeInfo.flags=7 (0x9729), calls ASIOCallbacks bufferSwitchTimeInfo with directProcess=1 at 0x976E, increments worker block count and flips the double buffer index after that (0x9771..0x977C). No-valid-port fallback is different.
- Port clock getter 0x4610 calls timeGetTime at 0x4628, and depending on port flags bit 6 either calculates from 32-bit tick elapsed or uses IAudioClock::GetPosition (+0x20, 0x46D5) and GetFrequency (+0x18, 0x46F1). In its clock branch it computes sampleRate*clockPosition/frequency when the frequency is nonzero. Port helper time units must NOT be blindly equated with the separate callback ASIOTime units.

## Static ground truth and verification

A local read-only x64 PE parser and GNU objdump verifier checked **124 exact opcode sites**, **6 direct helper CALL edges** and **3 double constant values** against the original, with SHA pinned. Original and duplicate original are unchanged.

The accompanying Batch11 ZIP contains the full 124-site opcode baseline CSV, verifier, independently authored PCM/clock domain-limited Python models, C++ partial struct sketches with offset static_assert checks, README and continuation docs.

Regressions: 77 previous tests rerun with BOTH required original-path environment variable names set (avoiding earlier skipped tests) + 34 new tests, **111/111 executed and passed, 0 skipped**; Linux-only structural/model tests, **not** Windows host parity.

## Remaining gates

Full Ghidra decompilation, all source semantics, all corner/error paths and dataflow, actual Windows Cubase 8.0.40/Realtek shared/exclusive tests with user authorization, complete native original-equivalent DLL and differential parity remain NOT DONE. The original binary was not patched or installed; **CI 0; optimization 0**.
