# Function boundary correction

The PE exception directory (.pdata) consists of **unwind/exception handling address ranges**, not a complete inventory of C++ functions.

Concrete evidence from user original:
- Render transfer: [0x4020, 0x4377).
- Capture transfer entry: 0x4380.
- Compiler-produced adjacent unwind records: [0x4380,0x4393), [0x4393,0x43F4), [0x43F4,0x4401), [0x4401,0x460C).
- A conditional branch from 0x4391 transfers execution directly to 0x4401, which demonstrates that counting these four as separate independent high-level functions is misleading.

Consequences:
1. Do not call the 590 initial .pdata entries '590 original functions'.
2. Cover leaf functions with no unwind record and compiler funclets/exception thunks.
3. Associate code ranges by true CFG branches and call/return behavior; preserve both original ranges and reconstructed logical groupings.
4. Validate all indirect dispatch, not only direct CALL targets.
5. Treat every reconstructed boundary as tentative until substantiated by x86 control flow and/or runtime traces.
