# ASIO 콜백·스레드 원본 호출 구조 (Stage 3)

원본 DLL SHA-256: `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. 모든 주소는 RVA. **원본 기능 재현 Phase 1 — 최적화 금지.** 정적 명령어 30곳을 원본 파일 및 GNU objdump와 대조하여 일치함을 확인했다. 실제 Windows 원본 실행 및 재현 DLL과의 동등성 검증은 **아직 없다**.

## 확정된 연결 (기계어+ASIO SDK ABI)

| RVA | 확인된 동작 |
|---|---|
| 0x1750 | `CAsio::start`가 worker 시작 함수 0x8FC0 호출 |
| 0x1CE7 | `CAsio::createBuffers`가 worker setup 0x92B0 호출 |
| 0x9412 / 0x9417 | 전달된 `ASIOCallbacks*`가 worker 객체 `+0x10`에 저장 |
| 0x9454 / 0x946C | 0x8F80 스레드 엔트리 준비 후 `CreateThread` |
| 0x8F9B | 모드 검사 분기에서 스레드 엔트리가 0x97B0 이벤트 루프로 tail-jump |
| 0x9890 | `WaitForSingleObject(event, 1ms)` 호출 |
| 0x9916 / 0x992A | 각 포트에 capture 0x4380, render 0x4020 수행 |
| 0x9947 / 0x994C | 처리된 포트 마스크와 기대 마스크 비교, 불일치하면 콜백 호출 생략 |
| 0x9954 | 마스크 충족 시 0x9610 ASIO 시간정보/콜백 함수 호출 |
| 0x9714 / 0x9729 | ASIOTime 구조체 초기화, timeInfo.flags=7 |
| 0x9757 / 0x9760 | worker 콜백포인터(+0x10), 버퍼 인덱스(+0x08) 로드 |
| 0x9768 / 0x976E | directProcess=1, 콜백 테이블+0x18 가상 호출 (=SDK `bufferSwitchTimeInfo`) |
| 0x9771 / 0x977C | 처리 블록 카운트 증가 및 ASIO 더블버퍼 인덱스 반전 |
| 0x9011 / 0x903E / 0x904E | worker 시작에서 출력 helper와 ASIO 콜백 helper 2회 프리롤 경로 |

위 표의 역할은 확인된 opcode에서 유도한 것. 별도 스레드 모드 분기, 오류·재진입, bufferSwitch 구형 콜백 사용 조건 등은 **UNRESOLVED**.

## 객체 상태의 부분 구조

`worker+0x00`: 블록 카운터; `worker+0x08`: 더블버퍼 인덱스; `worker+0x10`: ASIOCallbacks 포인터; `worker+0x18`: 대기 이벤트 핸들; `worker+0x40`: 포트 연결 리스트; `worker+0x48`: 설정 객체 포인터; `worker+0x50`: 상태 비트 필드(각 비트 의미 미완료).

`worker 블록 수 × 설정 객체+0x18 블록 프레임 수`를 기반으로 sample position 값을 만들고, 원본 `CAsio::getSamplePosition`(0x17E0)에도 같은 산술 구조가 존재한다. 밀리초 시간값을 나노초로 환산하는 곱셈(0x1852에서 1,000,000배)도 확인했다. **이것이 모든 OS·장치 조건의 최종 타임스탬프 알고리즘이라는 주장은 아직 하지 않는다.**

## 다음 복원 과제

1. 이벤트 마스크의 정확한 비트 정의 및 조건별 버퍼 콜백 순서.
2. 0x8FC0 프리롤의 실제 입력/출력 샘플 상태와 콜백 호출 조건.
3. 0x9610의 ASIOTime 타임스탬프 양쪽 분기 및 IAudioClock 연동.
4. `getSamplePosition` 결과와 콜백 TimeInfo의 일치 조건.
5. Thread 종료 및 버퍼 재생성·장치 유실 등의 실패 경로.
6. 전체 원본 기능·정적 함수 커버리지·동적 추적·독립 재현 구현·원본 대조. 최적화는 최종 게이트까지 0건.

## 자동 검증

`tools/verify_callback_bytes.py`는 원본 SHA를 확인하고 30개의 opcode 서명을 매칭한다. 단순 일치이지 런타임 동등성 증거가 아니다. 상세 disassembly 피연산자 검사 및 개별 근거는 로컬 Stage 3 분석 패키지의 `tools/verify_asio_callback.py`, `reports/asio_callback_evidence.json` 참고.
