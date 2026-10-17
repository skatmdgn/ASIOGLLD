# Original-to-replica parity matrix

Initial state: ALL ITEMS NOT_TESTED. The matrix describes REQUIRED future verification, not existing success.

| System | Required comparison | Status |
|---|---|---|
| DLL/COM | exports, CLSID, registration, interface QI/AddRef/Release | NOT_TESTED |
| IASIO ABI | all 24 vtable slots, return values, invalid arguments | NOT_TESTED |
| Callback | bufferSwitch, timeInfo, outputReady, double buffer order | NOT_TESTED |
| Devices | endpoint enumeration, default-device and device-change handling | NOT_TESTED |
| WASAPI shared | original formats, buffers, YouTube concurrency | NOT_TESTED |
| WASAPI exclusive | original format, mode and ownership behavior | NOT_TESTED |
| Inputs | capture channels and timing | NOT_TESTED |
| Outputs | channel maps, samples, conversions, timing | NOT_TESTED |
| Settings | configuration, UI, persistence and defaults | NOT_TESTED |
| Clock | position, output/input latency, sample rate | NOT_TESTED |
| Workers | synchronization, event handling, MMCSS and teardown | NOT_TESTED |
| Failures | bad calls, device loss, state transitions and recovery | NOT_TESTED |
| Host | Cubase Pro 8.0.40 and concurrent audio | NOT_TESTED |

For every result record original RVA(s), evidence, conditions, replica method, measured difference, and test confidence.
A successful Ghidra decompilation alone is NOT parity verification.