# Batch 6: Original audio port and worker evidence

Source: original SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. This is a **read-only static reconstruction**, not rebuilt original C++ or verified behavior parity.

## Port object

- RVA `0x68A6`: original allocates **0xF8 (248) bytes** for a CMMAudioPort object; constructor initializes fields and assigns the vtable at `0x68CC`.
- `+0x60=44100` from `0x68F2`; `+0x64=0x40` from `0x697B`.
- `+0xA0=2` exclusive-mode channels, `+0xA4=2` shared-mode channels, `+0xA8=16` exclusive bits/sample, `+0xAC=16` shared bits/sample. These are initial values **before per-device registry overrides**.
- Unwind-unlisted helper `0x2CB0` selects `+0xA0/+0xA4` by mode; `0x2CD0` selects `+0xA8/+0xAC`; `0x2CF0` returns bit depth using the original signed arithmetic shift-right by 3.
- `0x3CB0` receives the config's original `ExclusiveMode` flag from the `0x7AE8` path; its mode branch selects `+0xA0` versus `+0xA4`. Input/output *direction* and shared/exclusive *mode* must be reconstructed separately.

## Worker thread mode

- `0x8F80` accesses `[worker+0x48]` config; tests `[config+0x70]` bit 1 (PollMode). When set, tail-jumps to `0x97B0` event/port processing.
- When clear, references embedded title `ASIO WASAPI`, message **“Notification Thread is currently not supported.”**, calls `USER32!MessageBoxA` at import `0x1E3B0`, then returns zero.
- The static constructor has PollMode off initially, but registry/configuration and call preconditions are not dynamically verified. **Do not conclude this message necessarily appears during normal Cubase playback.**

The public reproducibility script `tools/batch6_verify_original.py` checks all 24 CAsio interface pointers and 38 original opcode signatures. Full function-index tools and derived callsite reports are provided in the separately shared Batch 6 ZIP, without original DLL bytes.
