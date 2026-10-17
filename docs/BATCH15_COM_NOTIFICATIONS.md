# Batch 15 — original COM endpoint notifications and ASIO callback lifetime

Source: user-supplied original `asioglld.dll`, x64 173056 bytes, SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. RVAs below refer ONLY to that binary. Static original-only reconstruction, **no replacement DLL, optimization, CI, original execution or runtime parity**.

## Two different IMMNotificationClient implementations

Original IID at RVA **0x20908**: `{7991EEC9-7E89-4D85-8390-6C703CEC60C0}`. The two original 8-slot vtables were verified from exact x64 pointers:

| Slot | Method | Config vtable RVA 0x208C8 | Worker vtable RVA 0x209A8 |
|---:|---|---|---|
| 0 | QueryInterface | 0x5EC0 | 0x5EC0 |
| 1 | AddRef | 0x5E80 | 0x5E80 |
| 2 | Release | 0x5E90 | 0x8EF0 |
| 3 | OnDeviceStateChanged | **0x5F70** | **0x8F20** |
| 4 | OnDeviceAdded | 0x5FA0 | 0x8F20 |
| 5 | OnDeviceRemoved | 0x5FA0 | 0x8F20 |
| 6 | OnDefaultDeviceChanged | 0x5FA0 | 0x8F20 |
| 7 | OnPropertyValueChanged | 0x5FA0 | 0x5FA0 |

`0x5FA0` is a zero-return stub. Two objects share QueryInterface/AddRef and the same IID but have **materially different reactions** to device changes.

### Configuration listener: host reset request

At `0x5F70`, callback object +0x10 references `CWasapiConfig`. If `config+0x68` contains `ASIOCallbacks*`, it calls that struct's `asioMessage` at slot +0x10 with **selector=3 (kAsioResetRequest), other arguments zero**, ignores the host return and returns 0. This happens **only for OnDeviceStateChanged** on the config listener.

The host callback pointer is stored at **0x7C8D** only after the `createBuffers` prevalidation succeeds in `0x7A80`. `disposeBuffers` clears it at **0x1DA6**, i.e. `CAsio+0x88 == (CAsio+0x20 config)+0x68`. Without a callback pointer, this listener does not send reset.

### Worker listener: stop currently started ports

At `0x8F20`, listener +0x10 refers to Worker. It clears Worker+0x50 bit0; traverses Worker+0x40 port-node list, each node+0x18 containing CMMAudioPort*. For each port with **port+0x64 bit4 (0x10)**, if `port+0x28` is nonnull, it calls `IAudioClient::Stop` (vtable +0x58). It then **clears bit4 regardless of Stop result or client pointer**, continues and returns 0. This action is shared by four event methods and **does not itself call ASIOCallbacks::asioMessage**.

The original port-start code `0x9270/0x9277` sets bit4 only after S_OK from IAudioClient::Start for actual clients. Special simulated-port (flag bit6) path skips client Start yet can also set bit4. Never conflate worker callbacks with config callbacks, and do not assume Windows invokes the two registered listeners in a deterministic order.

### Registration, refcounts and teardown

- Config setup `0x682A` CoCreateInstance of enumerator → 0x18-byte config listener → AddRef `0x6871` → RegisterEndpointNotificationCallback `0x687D`.
- `CAsio` ctor `0x10FD` allocates 0x88-byte Worker; `0x1157` allocates another 0x18-byte listener, owner pointer is Worker and held at Worker+0x58; AddRef `0x1189`, RegisterEndpointNotificationCallback `0x1196`.
- Both registrations' HRESULT results are not explicitly tested at the indicated call sites. Windows ownership and all failing paths are NOT proven.
- CAsio destructor unregisters worker listener `0x1354` then releases `0x1363`, deletes critical section and frees Worker/list, then unregisters config listener `0x1428`, releases enumerator `0x1439` and listener `0x144C`. Another configuration cleanup path has unregister at `0x6674`.
- AddRef/Release use a **32-bit interlocked xadd** on listener +0x08; count-zero Release destroys the corresponding listener, but complete concurrent lifetime remains unknown.

## Reproducible static proof and limits

Companion Batch 15 ZIP contains SHA-pinned GNU objdump/PE verifier and **291 exact opcode sites**, **44 operand matches**, **16 direct call references**, 2 GUIDs, 2 vtables (8+8), 3 imports, **10 bounded code windows (108 basic blocks, 117 internal edges, 31 CALL positions)**, a strictly partial Python behavior model and x64 C++ field-offset assertions.

All **32** new local tests and **224** prior regressions executed and passed (**256/256, skipped 0**). Only static/parser/model checks: **NOT original Windows execution, source-perfect reconstruction, native replica or parity**.

Next: prove all registration failure and async notification ownership cases, GetDevicePeriod and format errors, full interprocedural Ghidra analysis, Windows original runtime observation with user approval and registry backup, native original-behavior replica, then comprehensive differential tests. CI/optimization deferred.
