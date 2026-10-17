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

## Stage 3 — 원본 ASIO 스레드/콜백의 실제 호출 관계

- [콜백 처리 전체 연결, worker 필드, 초기 2회 프리롤, 포트 마스크 게이트](docs/ASIO_CALLBACK_PIPELINE.md)
- [원본 IASIO 기본 메서드의 반환값·버퍼 보고 규칙](docs/IASIO_BASIC_METHODS.md)
- [원본 DLL의 30개 스레드/콜백 opcode 서명 검사](tools/verify_callback_bytes.py)

원본의 주요 지시어 30곳과 IASIO 기본 메서드 13곳을 실제 바이트로 대조했다. **이 숫자는 복원한 함수 개수나 동작 동일성 비율이 아니다.** 정적 근거를 확장한 것이며 원본 전체 분석, 실행 추적, 재현 DLL은 아직 미완료다.

Phase 1의 **원본 그대로 기능·알고리즘 재현 우선 원칙**은 변하지 않는다.


## Stage 4 원본 정적 복원 — 설정·UI·함수 누락 후보
- [CWasapiConfig 생성자 및 레지스트리](docs/CONFIG_REGISTRY_RECOVERY.md): 초기값과 비트 필드, 실제 API 읽기·쓰기 RVA.
- [원본 UI 템플릿](docs/UI_RESOURCES.md): 7개 대화상자 리소스와 28개 컨트롤; GUI 메시지/동작은 미복원.
- [코드 타깃 커버리지](docs/COVERAGE_LEDGER_STAGE4.md): 590개 unwind 범위, 305개 직접 CALL 타깃, unwind 외부 67개 후보.
- [로컬 재검증 도구](tools/recovery_v4.py): Python3 + GNU objdump, 원본 읽기 전용, 23 opcode 서명 확인.
- 결과는 모두 정적 근거이며 **완전 복원이나 성능 개선의 증거는 아닙니다.**

- [원본 COM CLSID·클래스 팩토리·객체 크기](docs/ORIGINAL_COM_FACTORY.md): GUID와 3가지 실패 반환 코드 확인.
- [원본 COM 바이트 검증기](tools/verify_com_factory.py): 원본 SHA 고정, GUID/객체 할당/오류 코드 9곳 대조.


## Stage 5: 원본 설정창/레지스트리와 누락 함수 분류
- [레지스트리 루트 및 대화상자 메시지 분기](docs/ORIGINAL_REGISTRY_UI_STAGE5.md)
- [67개 예외정보 외부 직접 호출의 분류](docs/UNWIND_LEAF_TRIAGE_STAGE5.md)
- [설정/UI 정적 검증 스크립트](tools/verify_registry_ui_stage5.py)
- 검증된 원본 명령어 30/30, 레지스트리/GUI API import 11/11, preset [10,50,100]. 동등성 구현/최적화는 아직 없음.

- [원본 버퍼 ↔ 슬라이더 변환 알고리즘](docs/BUFFER_SLIDER_ORIGINAL_ALGORITHM.md), [정적 Python 모델](tools/buffer_slider_model.py), [경계값 단위 테스트](tests/test_buffer_slider_model.py).


## Batch 6 — 대량 정적 복원 (마지막에 한 번 업로드)
- [원본 오디오 포트·스레드 분기](docs/BATCH6_PORT_WORKER.md)
- [원본 IASIO 메서드 동작](docs/BATCH6_ASIO_METHODS.md)
- [전체 함수·간접 호출 커버리지와 미확인 사항](docs/BATCH6_COVERAGE.md)
- [읽기 전용 원본 검증 스크립트](tools/batch6_verify_original.py)
- 별도 배포 Batch 6 ZIP에는 전체 함수/점프/간접 호출 JSON, 본격 분석 도구, 11개 로컬 테스트가 포함됨. 아직 Windows 런타임 동등성/복제 DLL 없음. CI 반복 실행은 보류.


## Batch 7 — 대량 역공학 (CI 보류, 마지막에 일괄 커밋)
- [원본 WASAPI 공유/독점 Initialize 분기·클록·COM 수명·간접 호출 근거](docs/BATCH7_ORIGINAL_WASAPI.md)
- [이어가기 상태와 미완료 목록](docs/BATCH7_STATUS.md)
- [원본 바이트/IAT 검증 및 초기화 인수 분석 코드](tools/batch7_original_wasapi.py)
- [원본 분기 정적 모델 테스트](tests/test_batch7_original.py)
- [Batch 7 수치와 검증 상태 JSON](analysis/BATCH7_SUMMARY.json)
- 전체 164개 호출 주소와 호출 포인터 역추적 결과, Linux에서 검증한 Python 도구, 안전장치가 있는 미실행 Windows COM 테스트 소스는 Batch 7 별도 분석 ZIP에 보관. 기존 DLL 무변경, 최적화·CI 0회.
