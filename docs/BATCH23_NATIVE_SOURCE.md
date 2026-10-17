# Batch23 independent native components (NOT COMPLETE ASIO DRIVER)

Original x64 RVA 0x23F0 packed-to-interleaved channel scatter, 0x24C0 interleaved-to-packed gather, 0x2900 stereo16 capture and 0x2B5F ring advance have been modeled as unoptimized normal-input C++17 functions, without WASAPI or COM dependencies. Preserve raw byte widths 1/2/4 and original ring **single subtraction**, NOT modulus.

Original EH/CRT indirect callback provenance is expressed as candidate Win64 structs, callback pass-through, zero-extended vs signed relative32 arithmetic and 0xE06D7363 / 0x19930520 guards. Addresses for 13 callbacks are still runtime-dependent and NOT known native function pointers.

CMake Debug build and 2 distinct CTest native test programs passed; 336 synthetic input/output pairs matched the earlier Batch11 Python model. These are two independently authored partial models, **not original-vs-replica dynamic parity**.

Complete 48-file Batch23 ZIP provides fully tested original SHA verifier, 55-site instruction ledger, native CLI and test-only Python cross-check bridge, 540 Python local test logs and two native CTest logs. No original DLL or decompiler dump.
