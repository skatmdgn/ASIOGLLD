# FlexASIO cross-reference — useful analogy, NOT original source

FlexASIO is an open-source, PortAudio-backed ASIO driver: https://github.com/dechamps/FlexASIO

The reference source explicitly supports WASAPI shared and exclusive mode, with PortAudio providing the backend. Key files: `src/flexasio/FlexASIO/flexasio.cpp`, `portaudio.cpp`, `cflexasio.cpp`, `config.cpp`, `comdll.cpp`, `BACKENDS.md`.

| Subsystem | ASIOGLLD original | FlexASIO reference | Recovery use |
|---|---|---|---|
| ASIO ABI | CAsio vtable mapped from RTTI and IASIO interface | Separate ASIO COM interface implementation | Match method semantics, buffer and callback lifecycle |
| Windows audio | WASAPI COM evidence, configs present | PortAudio backend supports WASAPI shared/exclusive | Compare possible audio pipeline stages, not identical algorithms |
| Configuration | Registry and strings for exclusive, sample rate, buffer | User-level config file | Infer candidate settings meanings; validate through xrefs/runtime |
| Buffer scheduling | Thread/event/MMCSS evidence, exact processing path unresolved | PortAudio host stream and ASIO callback bridging | Identify what needs to be measured at runtime |
| Simultaneous YouTube | User's existing ASIOGLLD setting uses shared path | FlexASIO shared backend supports concurrent Windows audio | Required behavior for eventual equivalent implementation |

The two projects do **not** share a demonstrated source lineage. Never fill unknown original functions with copied FlexASIO logic and call it 'recovered'. Also respect FlexASIO/PortAudio and Steinberg SDK license terms before borrowing code.

Priority: first match observable ASIO and WASAPI behavior; only after proof of an actual problem should we consider safe replacement.
