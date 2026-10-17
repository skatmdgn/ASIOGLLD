# Original configuration & registry recovery — Stage 4

**Source**: user-supplied original `asioglld.dll` SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. All addresses are RVAs, not actual process addresses. **No optimization or replica**.

## Embedded CWasapiConfig constructor

- CAsio constructor at `0x10D5` invokes `0x6120` on the embedded object at `CAsio+0x20`.
- `0x612D` writes `10` to config `+0x20`: **BufferDuration initial value**.
- `0x6134` writes `44100` to config `+0x24`: **SampleRate initial value**.
- `0x613B` writes `1` to config `+0x70`: **initial flags**.
- Registry settings may override these initial values before device setup.

| Bit in config+0x70 | Registry key | Set/clear opcode RVAs | Initial state |
|---|---|---|---|
| 0x1 | `ExclusiveMode` | 0x632B / 0x6331 | set |
| 0x2 | `PollMode` | 0x624F / 0x6255 | clear |
| 0x4 | `UserDefinedBufferSize` | 0x63FF / 0x6405 | clear |

`0x6120` references five keys: `PollMode` at string RVA 0x20808, `ExclusiveMode` at 0x20818, `UserDefinedBufferSize` at 0x20828, `BufferDuration` at 0x20840, and `SampleRate` at 0x201D0.

The config reader uses imported `RegQueryValueExA` (IAT 0x1E020) and the write code uses `RegSetValueExA` (IAT 0x1E028). Configuration read path calls `0x66B0`, which constructs the registry-path helper. The original also refers to `Software\\ASIO` and driver-specific identifiers; exact behavior under all registry redirection/ACL/failure conditions is **UNRESOLVED**.

Known write references: `0x794A` for ExclusiveMode; `0x7992` for UserDefinedBufferSize; `0x79CC` for BufferDuration; `0x7A06` for SampleRate. Other branches write settings too. Nothing in the static evidence proves that a specific Windows user has the constructor defaults.

There are further per-port strings: `ExclusiveModeChannels` 0x20450, `SharedModeChannels` 0x20468, `ExclusiveModeBitsPerSample` 0x20480, and `SharedModeBitsPerSample` 0x204A0. Their read/write code occurs around 0x3248 and 0x373E. The complete meaning of every value and fallback condition is not yet reconstructed.

## Validation

`tools/recovery_v4.py` checks SHA, 23 opcode signatures, nine key strings, their static xrefs, coverage counts, and resource entries. On the current original: **23/23 checks pass**. Additional standalone tools and machine-readable findings are preserved in the Stage 4 ZIP. These are byte-level checks, **not Windows behavior equivalence**.

## Remaining

Reconstruct per-device settings selection and validation; registry failure fallback; GUI-event mapping and settings change application; exact buffer-duration units; every shared/exclusive and capture/render state. Preserve original semantics even when behavior appears unusual.


**Stage 5 verified correction:** `0x66B0` formats `Software\\ASIO\\Generic Low Latency ASIO Driver` under **HKEY_CURRENT_USER**; original IAT imports are **RegOpenKeyA** at 0x1E008 and **RegCreateKeyA** at 0x1E010, with value APIs RegQueryValueExA 0x1E020 and RegSetValueExA 0x1E028. See ORIGINAL_REGISTRY_UI_STAGE5.md.
