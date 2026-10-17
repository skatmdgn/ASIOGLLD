# ASIOGLLD — 원본 역공학 및 완전 재현 우선

**첫 목표: 기존 asioglld.dll의 모든 확인 가능한 내부 로직과 기능을 최대한 빠짐없이 복원하고, 원본과 동일한 동작을 하는 구현을 만든 후 차등 검증한다. 최적화는 그다음이다.**

- [최상위 복원 규칙](docs/PHASE1_ORIGINAL_PARITY_KO.md)
- [상세 단계](docs/RECOVERY_PLAN.md)
- [원본 동등성 체크리스트](docs/ORIGINAL_PARITY_MATRIX.md)
- [현재 상태와 미완료 항목](docs/STATUS.md)
- [ASIO vtable 분석](docs/ASIO_VTABLE.md)
- [WASAPI GUID 참조](docs/WASAPI_GUID_MAP.md)
- [원본 호출 경로](docs/CONTROL_FLOW.md)
- [FlexASIO 비교: 참고자료일 뿐](docs/FLEXASIO_COMPARISON.md)

## 현재 상태
PE/RTTI 및 일부 함수 주소와 호출 관계까지 확보했지만, 원본 소스 전체, 모든 분기, 런타임 상태 전이 및 재현 구현의 동등성은 **미확인**이다. Ghidra 디컴파일은 근거 자료이지 원본 C++을 그대로 재생성한 결과가 아니다.

Cubase Pro 8.0.40에서 유튜브 동시 재생하는 공유 모드가 우선 사용환경이지만, **복원 목표에는 원본 독점 모드/입력/설정/오류 경로도 전부 포함한다**.

Windows Ghidra 자동화 설명: [DECOMPILER_STAGE.md](docs/DECOMPILER_STAGE.md). 원본 DLL은 로컬에서만 처리하며 공개 GitHub에 올리지 않는다.