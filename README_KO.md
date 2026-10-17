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

## 2차 정적 역공학 진행 결과

- [원본 WASAPI 초기화·출력·입력 호출 경로](docs/ORIGINAL_WASAPI_DATAFLOW.md): 표준 COM 슬롯 기준 17개 호출 주소 확인.
- [샘플 복사·인터리빙 구현](docs/AUDIO_SAMPLE_TRANSFER.md): 1/2/4바이트 샘플 복사, 스테레오 16비트 인터리빙, 캡처 데이터 처리.
- [함수 경계 주의사항](docs/FUNCTION_BOUNDARY_CORRECTION.md): 590개 unwind 범위를 곧바로 590개 독립 함수로 세면 안 되는 이유.
- [미확인 코드와 정적 분석 범위](docs/COVERAGE_LEDGER.md): 304개 직접 CALL 대상 중 67개는 unwind 범위 밖에 존재.
- [원본 바이트 검증 스크립트](tools/verify_wasapi_calls.py): 정확한 원본 SHA 확인 후 COM 호출 17개·GUID 6개를 검사. GNU objdump 필요.

**여전히 복원·동등성 검증 중이며 완성된 원본 재현 DLL은 존재하지 않습니다. 최적화는 금지된 상태입니다.**
