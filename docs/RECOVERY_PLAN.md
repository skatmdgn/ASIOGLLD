# Restoration plan and stop conditions

## Stage A — Static proof map (in progress)
- PE imports/exports, sections, unwind functions, string index, RTTI classes, virtual methods, direct call graph.
- Classify each function: named from ABI; likely from direct references; unknown.
- Record source addresses and explicit confidence; export machine-readable maps.

## Stage B — ASIO and WASAPI control/data flow
- Map indirect COM/vtable calls using object lifetimes, IID GUID xrefs and object layouts.
- Identify exact shared-mode path, channel/samplerate transformations, clock/latency calculations.
- Extract ASIO init/start/stop/createBuffers and teardown pseudocode. Cross-check with official ASIO SDK semantics.
- Enumerate and explain unclassified functions; static full source restoration is not guaranteed.

## Stage C — Dynamic validation on the user's Windows PC
- No-install original load/call test, then trace Cubase ASIO and WASAPI events.
- Capture ETW audio events / Windows Performance Recorder, debugger call stacks, sample positions, actual glitch counters where supported.
- Test simultaneous browser audio and Cubase, and a copy of the same heavy Cubase project.
- Determine whether audio output driver or Cubase's ASIO/VST load actually misses processing deadlines.

## Stage D — Modernize *only validated bottlenecks*
- Prefer isolated source-level reimplementations with proven behavioral equivalence.
- Any binary patch must preserve x64 ABI, unwind/exception handling, thread safety, ASIO contract, and restoration path.
- Do not ship a performance claim until repeatable before/after glitch tests.
- Original DLL must never be overwritten for the initial tests.

## Long-term carry-forward
Always update docs and analyses in this GitHub repository to preserve the project across conversations. Preserve SHA, source provenance, known limitations, tests, and next work, rather than relying on chat memory.
