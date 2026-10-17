# Ghidra headless decompilation stage

This optional script attempts to decompile *all functions that Ghidra recognizes*. It is more comprehensive than PE unwind enumeration, but is **not** guaranteed to reconstruct all C++ sources or types. Current script compatibility with Ghidra on Windows is **unverified**.

1. Get a current Ghidra release from https://github.com/NationalSecurityAgency/ghidra/releases and follow its JDK requirements.
2. Copy the user-provided original to `original/asioglld.dll` in the project directory. **Do not commit it.**
3. Set `GHIDRA_HOME` to the extracted Ghidra folder.
4. With Cubase closed, run `tools/ghidra/RUN_GHIDRA_WINDOWS.cmd`.
5. Inspect `local_output/decompiled/SUMMARY.txt`, `functions.tsv`, and `functions/*.c`.

The original SHA-256 is checked before running. It **does not install, register, or patch** any DLL, and only writes its derived files to `local_output/`.

Keep full decompiler output local, rather than uploading proprietary reconstructed code or the original DLL to this **public** repository. It may be appropriate to share limited traces or independently authored findings.

The method labels are suggested from the RTTI-backed ASIO vtable, not a claim that decompiled source is identical to the original. Any runtime optimization requires trace-backed evidence and Cubase A/B testing.
