# Original COM/ASIO class-factory ABI — Stage 4

Evidence is the original user-supplied `asioglld.dll` with SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. Addresses are file RVAs and all findings are static (not runtime or replica parity).

## Identifiers verified from actual raw GUID bytes

- Original ASIO driver CLSID at **0x26690**: `{52EBAE30-47E4-483F-B87B-770314306005}`.
- Standard `IID_IUnknown` at **0x205F8**: `{00000000-0000-0000-C000-000000000046}`.
- Standard `IID_IClassFactory` at **0x1E560**: `{00000001-0000-0000-C000-000000000046}`.

## Object construction

- `DllGetClassObject`, exported at **0x20B0**, compares the requested interface IID, searches the DLL's class template range from 0x266A0 to 0x266C0 and creates the class factory. The range is exactly **one 32-byte template entry** on this binary.
- The class template references the original CLSID at **0x26690** and factory's `CreateInstance` helper at **0x1520**.
- `0x216C` allocates **0x18 bytes** for a class-factory object; its vtable pointer is from **0x203E8**.
- `0x153A` allocates **0xD0 bytes** for a `CAsio` driver object; `0x1557` invokes its constructor at **0x1080**.
- The CAsio constructor at `0x10D5` calls the embedded configuration initializer `0x6120`.
- `DllCanUnloadNow`, exported **0x21D0**, checks two process-local counters at **0x27AB0** and **0x27AA4**. The exact ownership conditions for every counter need deeper tracing; apparent zero condition returns S_OK, other cases S_FALSE.

## Identified COM error paths in DllGetClassObject

- **0x210F**: `E_NOINTERFACE` = `0x80004002`.
- **0x215C**: `CLASS_E_CLASSNOTAVAILABLE` = `0x80040111`.
- **0x219F**: `E_OUTOFMEMORY` = `0x8007000E`.

A no-memory failure in the ASIO object creation helper and the exact AddRef/Release lifetime under aggregation remain to be verified separately.

## Original-only reproduction rules

Phase 1 implementation must match the original COM ABI, GUIDs, object lifetime and externally observable error codes in matched tests. **Do not register a new replica under the same CLSID** or overwrite the original for preliminary tests: use a safe isolated or no-registration test host first. The static verifier `tools/verify_com_factory.py` checks GUIDs, allocations and error immediate values against exact original bytes.

This does **not** mean the class lifetime, thread teardown, aggregation and other COM methods are fully recovered.
