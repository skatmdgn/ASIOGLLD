# Batch11 exact-original continuation — 2026-10-17

User directive: exhaustively reconstruct original asioglld.dll first, then build faithful behavior-equivalent replica and verify; optimization ONLY after that with explicit approval. Do not omit exclusive mode, input, UI, errors or COM ABI. Commit to GitHub once at end of each large batch. CI delayed until late/final stage.

Original: 173056-byte PE32+ x64, SHA256 e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd. Both attached copies verified unchanged.

Batch11: original PCM data paths 0x23F0 -> 0x24C0 inverse, 0x2750 generic capture scatter, 0x2900 16-bit stereo fast path, 0x2A90 ring orchestration and quotient/remainder cursor wrap. Their callers are 0x4221, 0x42FA, 0x2B40, 0x2AF3, 0x45C2. Port clock helper 0x4610 called at 0x44AC. Recover original 0x17E0 IASIO getSamplePosition and 0x9610 callback timestamp, including 1.0, -1e9 and ~2^63 static constants.

Original byte checking: 124 instruction locations, 6 direct edges and 3 original double constants match. Analysis-only byte-sample model, bounded clock arithmetic model and offset-checked x64 C++ class sketches. 34 new tests + 77 prior tests = 111 PASSED, 0 skipped (environment bug in one previous batch corrected). No original binary execution, no replica DLL, no runtime parity. Linux g++ -fsyntax-only static_assert PASS. ZIP has 17 files including full byte evidence and detailed Korean documentation, original excluded.

NEXT:
1. Complete Ghidra Windows headless decompilation and source-level CFG/type recovery.
2. Resolve full 0x2A90 early-return + buffer ownership and format/overflow branches; cover both shared/exclusive and render/capture.
3. Validate 64-bit SSE timestamp extreme conversions and all failure cases, and reconcile with true original runtime.
4. Recover COM lifetimes, ASIO states, registry & GUI, then build exact-function replica without optimization.
5. Run original-vs-replica parity on Windows with user permission; no unapproved original driver replacement.

Original unchanged. CI=0, optimization=0. Exact original human-written C++ source text is not guaranteed by compilation artifacts.
