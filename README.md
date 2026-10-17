# ASIOGLLD — original fidelity first

**Phase 1 ONLY:** exhaustively reverse engineer original asioglld.dll and reproduce its behavior without optimizations, skipped features or modern substitutes; verify original-vs-replica parity before Phase 2. Both WASAPI shared and exclusive branches, input/output, ASIO COM ABI, settings, errors and device behavior are in scope.

See [binding Phase 1 instructions](docs/PHASE1_ORIGINAL_PARITY_KO.md), [roadmap](docs/RECOVERY_PLAN.md), [parity matrix](docs/ORIGINAL_PARITY_MATRIX.md), and [current status](docs/STATUS.md).

Exact original developer-written C++ variable names, comments or source layouts cannot be guaranteed after compilation. The target is maximum evidence-backed semantic recovery and high-fidelity behavioral equivalence, clearly documenting unresolved paths. FlexASIO is external reference only.

Initial PE and RTTI-based mapping exists, but full dynamic tracing, replica and parity are NOT done. No optimization allowed until validated and approved.