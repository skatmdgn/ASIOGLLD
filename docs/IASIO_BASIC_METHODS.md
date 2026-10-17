# 원본 IASIO 기본 메서드의 반환값 및 객체 필드 — 정적 복원

최상위 목표: 원본 그대로 기능 재현. 바이너리 SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. 실제 기계어를 확인한 결과이며 Windows 런타임 및 복제본 동등성은 아직 미검증.

## 1. `getChannels` RVA 0x1910

- 두 출력 포인터(`numInputChannels`, `numOutputChannels`)가 유효하면 객체 `+0x48`과 `+0x4C`의 정수 값을 각각 반환하고 `ASE_OK`(0).
- 어느 출력 포인터라도 NULL이면 `ASE_InvalidParameter`(-998). 확인: 0x1910–0x192D.
- 두 필드가 어떻게 계산/갱신되는지는 아직 복원 중.

## 2. `getLatencies` RVA 0x1930

- 양쪽 포인터가 유효하면 객체 `+0x3C`의 32비트 값을 **두 배** 계산해 input/output latency 모두에 기록. 두 방향 모두 같은 값을 반환. 확인: 0x193A–0x194B.
- NULL 인수는 `ASE_InvalidParameter`(-998).
- 이 값은 보고용 레이턴시이며 물리 장치의 실제 왕복 지연과 동일하다고 확정할 수 없음.

## 3. `getBufferSize` RVA 0x1C50 — 원본의 비표준처럼 보이는 동작도 유지할 것

- 네 출력 포인터 `minSize, maxSize, preferredSize, granularity`를 검사 (0x1C50–0x1C67).
- 어떤 포인터라도 NULL이면 `ASE_InvalidParameter`(-998).
- 객체의 `+0x3C` 값이 0 이하이면 `ASE_NotPresent`(-1000).
- 양수면 **네 출력 값 모두 같은 버퍼 크기**로 설정하고 `ASE_OK` 반환 (0x1C69–0x1C7D).
- 주의: 일반적인 ASIO SDK 샘플에서는 고정 버퍼라면 `granularity=0`을 보고할 수도 있으나, **이 원본 DLL은 실제로 granularity까지 버퍼 크기 자체를 쓴다.** Phase 1에서는 이 동작을 '교정'하거나 '정상화'하면 안 됨. 반드시 원본과 동일하게 재현해야 함.

## 4. `getSampleRate` RVA 0x1AA0

- 출력 포인터 NULL: `ASE_InvalidParameter`(-998).
- 객체 `+0x44` 정수 샘플레이트가 양수: 이를 64비트 double로 변환해 출력하고 `ASE_OK`.
- 0 이하: `ASE_NoClock`(-995).
- 실제 설정/동기화 경로는 별도 복원 필요.

## 5. `getDriverVersion` RVA 0x1690

- 단순히 객체 `+0x9C`의 32비트 값을 반환. 구성 시 해당 필드를 누가 설정하는지는 미복원.

## 근거와 범위

13곳의 추가 명령어(opcode) 주소를 실제 원본 파일 바이트와 대조해 일치함을 확인했다. 각 메서드의 모든 간접 분기, 객체 필드 수명, 호출자가 비정상 값을 전달할 때 외부 관측 결과는 Windows 동적 추적이 필요하다.

다음 단계는 설정 로더·생성자에서 `+0x3C,+0x44,+0x48,+0x4C,+0x9C`의 값이 정해지는 경로까지 역추적해 원본 제어판 설정과 연결하는 것.
