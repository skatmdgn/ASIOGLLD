# Batch10 checkpoint — 2026-10-17

**MANDATORY:** faithfully reconstruct entire original asioglld.dll before any optimization; no shared-only substitute. Keep original and duplicate unchanged. No mid-batch GitHub commits / CI; finalize local analysis once then commit once.

Original: x64 DLL, 173056 bytes, SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`.

**Batch10 verified local static outputs:** 12 analyst-defined code windows covering original WASAPI init/render/capture, COM factory, getSamplePosition, audio clock and worker setup/start/poll/stop/timeInfo. 351 basic blocks, 512 intra-window branch edges and 91 CALL positions; these are **not source function counts**. 75 exact instruction byte sites + 24 CAsio vtable entries match original. Six original API imports and four floating-point timestamp constants checked. The work includes corrected **persistent port success bitmask** (RVA 0x9933, 0x9947, 0x9951), 2-iteration initial callback preroll, stop 3000ms wait and double buffer toggling.

**Tests:** 29 new Batch10 (after fixing one assertion about report wording) + 48 previous Batch6–9 all **77/77 local PASS**. Read-only original SHA remains unchanged. These are static/parser/synthetic-model checks, NOT running-original or replica parity.

**Package:** `ASIOGLLD_Original_Recovery_Batch10.zip` available in this conversation, 15 files, original DLL excluded, ZIP integrity OK. Includes full 12-window graph `analysis/cfg_windows.json`, 91-call CSV, 75 site CSV, Python CFG and model sources, 29 tests, Windows/Linux reproduction instructions. This public repo keeps a compact document/portable worker model and status to avoid committing massive proprietary disassembly.

**Not yet achieved:** full Ghidra run, all function/cfg/dataflow semantics, actual Windows host/debugger execution, original-equivalent ASIO DLL, input/output/share/exclusive UI/error test parity. **CI run 0, optimization 0.**

**Next:** Windows Ghidra decompiler export, reconstruction of COM object lifetimes and all indirect calls and exception edges; recover 16/24/32-bit PCM conversion and true sample clock arithmetic; original Windows traces with informed approval; only then build original-fidelity replica and verify its behavior.