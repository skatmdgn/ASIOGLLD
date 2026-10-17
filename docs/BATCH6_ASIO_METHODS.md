# Batch 6: Additional original ASIO method semantics

**All 24 CAsio IASIO vtable entries at RVA 0x202F8 match** their original target addresses. This validates interface entrypoint mapping only, **not** full functions or original/replica parity.

- **setSampleRate 0x1960**: converts requested double to integer with `cvttsd2si`, compares with `CAsio+0x44`; unchanged integer rate immediately returns 0. Changed rate calls `0x85D0` validation; on rejection returns `ASE_NoClock (-995)`. The accepted path writes the `SampleRate` registry DWORD through `RegSetValueExA`, then calls host ASIOCallbacks's `asioMessage` function pointer at offset `+0x10` using selector **3** (`kAsioResetRequest`) if available. Registry failure behavior, all validation branches and callback outcomes remain unresolved.
- **canSampleRate 0x1AD0**: truncates requested sample rate and traverses original port lists at `CAsio+0x68/+0x70`; compares number of eligible ports with number supporting the requested rate. Failure path returns **`ASE_InvalidMode (-997)`**. It is not a simple fixed list of 44.1k/48k.
- **getSamplePosition 0x17E0**: validates both output pointers, computes frame count from worker blocks and config's frames-per-block, and optionally calculates a sample-clock-based timestamp from port state and sample rate. Some no-worker/no-eligible-port paths return 0 without writing outputs. Full time arithmetic remains to be checked.
- **setClockSource 0x1C00**: index 0 returns 0, nonzero index returns `ASE_InvalidParameter (-998)`.
- **getErrorMessage 0x16A0** is an immediate return stub and does not populate the supplied error string in its original code path.
- **future/outputReady** point to the same zero-return stub at `0x5FA0`. Do not implement imaginary future-mode support during original reproduction.
- Previously mapped **getBufferSize** has unusual behavior: returns the same positive frame size in min/max/preferred/**granularity** fields. Reproduction must retain that behavior.

Every assertion above is from original x64 instructions, with control-flow inferences explicitly limited by unexamined branches. Windows original-execution tracing and compiled replica have **not** been performed.
