# Batch19 — 원본 DLL 전체 x64 unwind 체인·전역 CFG 분석

원본 173056바이트 SHA256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. 바이트 고정 읽기 전용 정적 분석, 원본 실행/성능 최적화/재현 DLL 없음.

## 590개 원본 `.pdata` 레코드를 올바르게 묶기
- 실제 원본 `UNWIND_INFO`: 일반 NONE 285, CHAININFO 221, UHANDLER 30, EHANDLER 10, EHANDLER+UHANDLER 44.
- CHAININFO 221개의 (BeginAddress,EndAddress,UnwindInfoAddress) **전부 실제 `.pdata` 레코드와 일치**. 부모를 따라 연결하면 369개 독립 unwind root, 76개는 여러 연결 구간.
- `IASIO::getSamplePosition` RVA 0x17E0와 0x1845,0x18F8; `setSampleRate` 0x1960와 0x1983,0x1A3C; class factory 0x1F80와 0x1FF2,0x201F,0x2048은 각자의 동일 unwind root 아래 위치. 설정 로딩 0x30C0은 일곱 개 기록이 한 root 아래.
- EH/UH를 가진 84개 부모 root가 참조하는 핸들러 시작은 RVA 0x105C0(30), 0x12510(42), 0x16F80(12)의 세 곳뿐.

## 원본 전 영역 호출/분기
- 전체 objdump 선형 명령어 항목 33,194개; 590 unwind 물리 구간에서 6,331 basic blocks, 8,807 구간 내부 CFG 간선.
- 구간 바깥 분기 240곳 = 동일 unwind root의 다른 구간 224, 타 unwind root 9, 정적으로 목적지 불명인 간접 JMP 7.
- 타 root 이동 사례: RVA 0x8F9B 스레드 진입 -> 0x97B0 폴링 루프.
- 전체 CALL 명령 2,097개 = 일반 direct 1,453, 특수 외부 직접 주소 1, IAT 경유 479, 기타 비-IAT 간접 164. IAT 슬롯 148개. 직접 호출 타깃이 unwind 기록 밖인 RVA 67곳.
- **369 unwind root는 확정 원본 C++ 함수 수가 아님**: EH funclet, no-unwind leaf, thunk, x64 handler, 선형 disassembly의 padding/예외 경로 등이 남아 있음.

## 검증 결과와 현재 미완료
- 새 Python 원본 해시/체인 검증 24개 및 합성 Ghidra manifest 대조 6개, 신규 총 30개 통과. 기존 Stage5~Batch18 357개 재실행 통과. **총 387/387 local PASS, skipped 0**.
- companion `ASIOGLLD_Original_Recovery_Batch19.zip`에 39개 파일: full SHA-pinned parser, 590 segment/369 root CSV, 2946 CALL/JMP CSV, physical CFG CSV, native handler/cross-root jump 데이터, Ghidra Windows 전체 decompile 기존 exporter, post-export bridge, 테스트/로그. 저작권 있는 원본 DLL 및 디스어셈블 원문 전체는 ZIP/GitHub에 넣지 않음.
- **Ghidra 현재 Linux 환경에 설치되지 않아 실제 전체 디컴파일을 하지 못했다.** Ghidra script는 후속 Windows 환경에서 사용자 검토 후 사용해야 한다. 독립 DLL 구현·Windows 실제 원본 테스트·원본과 1:1 parity 미완료. CI 0, 최적화 0, 원본 수정 0.
