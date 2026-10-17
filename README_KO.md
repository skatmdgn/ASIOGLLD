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


## Batch 8 — 원본 간접 호출/COM 수명 역공학
- [원본 장치 열거·알림·버퍼/클록 수명 및 오류 경로](docs/BATCH8_COM_DISPATCH.md)
- [간접 호출 신규 정적 식별 75곳의 원본 RVA/슬롯/객체 로드 근거](analysis/BATCH8_NEW_CALLS.csv)
- [원본 SHA 고정 호출 주소/슬롯 검사기](tools/batch8_validate_static.py)
- [복원 상태와 미완료 지점](docs/BATCH8_STATUS.md)
- 비-IAT 간접 호출 164곳 중 기존 30 + 신규 75 = 105곳 정적 이름 후보; 59곳 미해결. 기존 배치 포함 로컬 단위 테스트 35개 통과. CI·최적화·원본 변경 없음. 전체 호출 JSON과 강화된 분석 소스는 별도 Batch8 ZIP에 제공.


## Batch 9 — 최종 59개 미해결 간접 호출 정적 분류 / 팩토리 수명 복원
- [CClassFactory 원본 CreateInstance/참조 수명](docs/BATCH9_FACTORY_LIFECYCLE.md)
- [남은 59개 호출 분석 및 정적 판정 한계](docs/BATCH9_LAST59_TRIAGE.md)
- [RVA·원본 바이트 59곳](analysis/BATCH9_LAST59.csv) / [팩토리 핵심 18곳](analysis/BATCH9_FACTORY_PINS.csv)
- [재현 가능한 원본 읽기 전용 검사기](tools/batch9_verify_original.py)
- [이어가기·미완료 목록](docs/BATCH9_STATUS.md)
- 상세 164개 통합 목록, 원본 바이트 23개 핀, 정적 COM 모델 및 신규 테스트 13개는 별도 Batch9 ZIP에 보관. 누적 48개 로컬 검사 통과는 기능 동등성 보증 아님. CI/최적화/원본 수정 없음.


## Batch 10 — 원본 작업 스레드 / 제어 흐름 (로컬 대량 분석 후 한 번 반영)
- [원본 폴링/ASIO 더블버퍼/프리롤/정지 원리](docs/BATCH10_WORKER_CONTROL_FLOW.md)
- [원본 함수 구간 12개, 기본 블록 351개, 분기 연결 512개](docs/BATCH10_CFG_INVENTORY.md)
- [원본 동작 누적 마스크 모델](tools/batch10_worker_model.py) 및 [단위 테스트](tests/test_batch10_worker.py)
- [재개용 상태문서](docs/BATCH10_STATUS.md)
- 전체 CFG(131KB), 75개 원본 opcode 핀, 91개 호출 인덱스와 29개 신규 테스트는 대화 첨부 Batch10 ZIP에 포함. 이전 배치 48개 재검사 포함 로컬 77개 통과. 동적 Windows 검증·동등한 DLL·CI·최적화는 아직 없음.


## Batch 11 — 원본 PCM·ASIO 클록 심층 복원 (CI 보류)
- [PCM/링 버퍼/클록 원본 함수별 복원 명세](docs/BATCH11_PCM_CLOCK.md)
- [이어가기/미해결 기능 체크포인트](docs/BATCH11_STATUS.md)
- [PCM 일부 경로 정적 모델](tools/batch11_pcm_model.py) / [시간 계산 모델](tools/batch11_clock_model.py)
- [원본 SHA/핵심 명령어/직접 호출/시간 상수 확인](tools/batch11_original_checks.py)
- [x64 버퍼 구조체 후보 offset assertions](include/batch11_layout_candidates.hpp)
- [기계가 읽을 수 있는 검증 결과](analysis/BATCH11_SUMMARY.json)

상세한 124개 명령어 바이트/6개 호출/3개 원본 상수 대조표와 34개 신규 테스트, 기존 77개 회귀 검사 전체 기록은 이 대화의 ASIOGLLD_Original_Recovery_Batch11.zip에 있다. 원본과 재현 DLL 간 동작 검증은 아직 전혀 하지 않았다. 최적화와 CI는 0회.


## Batch12 원본 IASIO 24개 메서드 및 채널/레이트 전수 인터페이스 분석
- [원본 IASIO 24 슬롯별 동작 및 반환 계약](docs/BATCH12_ASIO_CONTRACTS.md)
- [포트별 채널 샘플 타입, 레이트 목록, 설정 실패 부작용](docs/BATCH12_CHANNEL_RATE.md)
- [복원 이어가기 및 미완료 상태](docs/BATCH12_STATUS.md)
- [부분 의미 Python 모델](tools/batch12_model.py) 및 [원본 바이너리 spotcheck](tools/batch12_spotcheck.py)
- 19개 메서드/헬퍼 CFG, 206 opcode 핀, 7 direct call, 3 문자열 및 43개 신규 테스트 전체 코드/데이터는 Batch12 ZIP에 포함. 111개 이전 테스트 포함 로컬 154/154 PASS. 동작 동일한 DLL/Ghidra 전체 디컴파일/Windows 동적 검증 미완료. CI/최적화/원본 변경 없음.


## Batch13 — 원본 포트 포맷 지원 목록의 생성 및 소멸
- [장치별 WASAPI 후보 조사·HRESULT 검사·3계층 목록과 파괴 순서](docs/BATCH13_FORMAT_CAPABILITIES.md)
- [다음 복원 상태 및 미해결 경로](docs/BATCH13_STATUS.md)
- [원본 SHA/후보 테이블/20개 직접 호출 검사기](tools/batch13_original_audit.py)
- [후보 포맷 부분 정적 모델](tools/batch13_format_model.py) / [테스트](tests/test_batch13_format_model.py)
- [C++ x64 계층 구조체 정적 배치 후보](include/batch13_format_tree_layout.hpp)
- 원본에서 116개 opcode/20개 호출/8개 CFG 구간(323블록,467내부 간선) 검증. 신규 38 + 이전 154 = 총 192 로컬 테스트 통과, 스킵 0. 전체 리포트와 원본 바이트 CSV 및 전체 분석기/코드는 대화의 Batch13 ZIP 참고. 원본 DLL/Ghidra 출력/전용 대체 코드 공개 안 함. CI·최적화 없음.


## Batch 15: 원본 COM 장치 알림 객체 두 종류와 서로 다른 동작 복원
- [정확한 원본 IMMNotificationClient 8슬롯 x2, Reset 요청·포트 Stop/COM 수명](docs/BATCH15_COM_NOTIFICATIONS.md)
- [새 채팅 개발 이어가기 상태문서](docs/BATCH15_STATUS.md)
- [Python 제한적 알림 상태 분석 모델](tools/batch15_notification_model.py)
- [검증 결과 JSON](analysis/BATCH15_SUMMARY.json)
- **전체 실제 검사 도구/291 pinned opcode CSV/44 operands/16 direct CALL/10 window CFG/32 신규 테스트/C++ 구조체**는 대화의 `ASIOGLLD_Original_Recovery_Batch15.zip`에 포함. 224 기존 테스트 포함 로컬 총 256 통과, 스킵 0. Windows 실행·동등 재현 DLL·CI·최적화 모두 미완료.


## Batch 16 — 원본 스레드 종료·COM 리스너 등록 실패 시 수명 구조
- [대기 3000ms 결과 무검사·포트 COM 해제·장치 알림 구분](docs/BATCH16_WORKER_COM_LIFETIME.md)
- [모든 미완료와 재개 체크포인트](docs/BATCH16_STATUS.md)
- [정상 조건 일부의 정적 Worker 상태 모델](tools/batch16_worker_lifetime_model.py)
- [검증 수치/미완료 상태 JSON](analysis/BATCH16_SUMMARY.json)
- 자세한 기계어 307곳·64 피연산자·11 직접 호출·10 IAT 호출·10 CFG·293개 로컬 실행 검사 기록 및 Win64 C++ 레이아웃은 이 대화의 별도 Batch16 ZIP에 제공. 원본 DLL·전체 디스어셈블은 공개 저장소에 올리지 않음. 원본 수정 0, CI 0, 최적화 0. 재현 DLL/원본 실행 동등성 검증 미완료.


## Batch17 — 원본 ASIO API 성공 반환과 스레드 생성 실패 상태 연결
- [createBuffers/WorkerPrepare/start/TimeInfo/WorkerStop 정적 실패 경로](docs/BATCH17_FAILURE_PROPAGATION.md)
- [현재 복원 상태와 필수 다음 단계](docs/BATCH17_STATUS.md)
- [정적 검증 총괄](analysis/BATCH17_SUMMARY.json)
- 전체 Python 정적 분석기, 61 원본 opcode 근거, 6개 CFG, 322개 로컬 테스트 결과 및 후보 구조체는 별도 Batch17 ZIP에 포함. 원본 Windows 실행·복원 DLL 패리티·CI·최적화 미완료.


## Batch18 — 원본 COM apartment·알림 등록 실패·CAsio 소멸자 수명 감사
- [원본 CoInitializeEx/CoCreateInstance, 별도 두 리스너, WorkerStop vs 소멸자](docs/BATCH18_COM_LIFETIME.md)
- [Batch18 상태/이어가기](docs/BATCH18_STATUS.md)
- [원본 SHA/리스너 vtable/COM import 축약 검증 코드](tools/batch18_original_spotcheck.py)
- [등록 실패 시 COM OS 소유권을 미확인으로 유지하는 부분 모델](tools/batch18_listener_model.py)
- [테스트 소스](tests/test_batch18_listener_model.py) 및 [분석 통계](analysis/BATCH18_SUMMARY.json)
- 별도 **ASIOGLLD_Original_Recovery_Batch18.zip**에 완전한 188핀 검증기, 9개 CFG(197블록/273내부 간선), Win64 C++ 레이아웃, 이전 322+신규 35=357개 로컬 테스트/전체 로그를 보관. **원본 Windows 실행/재현 DLL 동등성·CI·최적화 미완료.**
