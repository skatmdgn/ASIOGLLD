# Batch 8 continuation and scope

Directive: **restore original first, faithfully and completely as technically possible, only then optimize with explicit user approval**. Do not replace with an incomplete WASAPI shared-mode-only driver. Include original shared/exclusive, capture/render, UI, error handling and COM lifetime.

User workflow: perform as much local work as possible, commit to GitHub **once at the end**, avoid intermediate CI. This batch: no CI, no optimization.

Original 173056-byte `asioglld.dll`, SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`; duplicate upload matches, original unchanged.

Batch8: of 164 non-IAT indirect call positions, previous 30 + **75** new ABI/receiver provenance candidates = **105** statically named, **59 unresolved**. Store each new call and original operand load anchor in `analysis/BATCH8_NEW_CALLS.csv`. Full 164-site classification and rigorous register-provenance script are in conversation artifact `ASIOGLLD_Original_Recovery_Batch8.zip` (not embedded in public repository). Primary new work: enumerator, collection, default endpoint, notification, PROPERTYKEY DeviceFriendlyName, format verification, client lifecycle and error-time buffer cleanup.

Regressions run locally with original SHA pinned: Batch6 11/11, Batch7 9/9, Stage5 4/4, Batch8 11/11; total 35/35 (unit/static tests **not original-runtime parity**).

Outstanding: Ghidra full-function decompilation, 59 indirect receivers, complete CFG, GUI/settings, OS-specific WASAPI branches, Windows debug/trace, faithful stand-alone replica DLL, original-vs-replica parity **all incomplete**. **No optimizations**.

Continue from this repo and the shared Batch8 ZIP. No Windows source runtime verified; do not claim complete reconstruction.
