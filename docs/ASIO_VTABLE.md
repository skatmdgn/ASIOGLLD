# Recovered CAsio virtual interface (high confidence)

This table reconstructs the **method-entry address mapping**, not the original C++ source. Evidence: MSVC x64 RTTI complete-object-locator at RVA 0x20F28, class type descriptor CAsio, vtable RVA 0x202F8, 24 consecutive method pointers, and the official IASIO method order from the Steinberg ASIO SDK.

| Slot | ASIO SDK method | Original DLL function RVA |
|---:|---|---|
| 0 | `QueryInterface` | `0x1050` |
| 1 | `AddRef` | `0x1060` |
| 2 | `Release` | `0x1070` |
| 3 | `init` | `0x16B0` |
| 4 | `getDriverName` | `0x1650` |
| 5 | `getDriverVersion` | `0x1690` |
| 6 | `getErrorMessage` | `0x16A0` |
| 7 | `start` | `0x1740` |
| 8 | `stop` | `0x1770` |
| 9 | `getChannels` | `0x1910` |
| 10 | `getLatencies` | `0x1930` |
| 11 | `getBufferSize` | `0x1C50` |
| 12 | `canSampleRate` | `0x1AD0` |
| 13 | `getSampleRate` | `0x1AA0` |
| 14 | `setSampleRate` | `0x1960` |
| 15 | `getClockSources` | `0x1BD0` |
| 16 | `setClockSource` | `0x1C00` |
| 17 | `getSamplePosition` | `0x17E0` |
| 18 | `getChannelInfo` | `0x1C10` |
| 19 | `createBuffers` | `0x1C90` |
| 20 | `disposeBuffers` | `0x1D40` |
| 21 | `controlPanel` | `0x1DC0` |
| 22 | `future` | `0x5FA0` |
| 23 | `outputReady` | `0x5FA0` |

The first 3 entries implement IUnknown; slots 3–23 follow the ASIO SDK IASIO virtual method order. Slots 22 and 23 both point to 0x5FA0, likely an unsupported-operation stub, **not proof of a working implementation**.

For a function address, add PE image base `0x180000000` to the RVA for the preferred in-file virtual address. ASLR changes addresses at runtime.

Other RTTI-confirmed vtable associations:
- `CUnknown` 0x201F8 (4 entries)
- `IASIO` 0x20228 (pure virtual placeholder functions; not a working implementation)
- `CAsio` 0x203C0 (secondary vtable, offset 8)
- `CClassFactory` 0x203E8 (5)
- `CMMAudioPort` 0x205E0 (3)
- `CNotificationClient` 0x208C8 (8)
- `CNotificationClient2` 0x209A8 (8)

**Recovery status:** methods mapped from RTTI and ABI. Bodies and state transitions are not yet completely decompiled or validated on Windows.
