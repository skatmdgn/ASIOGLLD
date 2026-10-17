# 9차 원본 COM 클래스 팩토리 역공학

검증 대상: x64 원본 `asioglld.dll`, SHA-256 `e2a9088a71e61362b4b1cf9d11717a1278ef26c940e7ca716290cab7a93c5cfd`. 모든 주소는 RVA. **최적화·바이너리 수정 없이 원본 동작만 연구한다.**

원본 `CClassFactory` vtable은 **0x203E8**이고 엔트리 5개의 진입점은 **0x1EB0 (QueryInterface), 0x1F50 (AddRef), 0x1F60 (Release), 0x1F80 (CreateInstance), 0x2090 (LockServer)** 로 매핑된다. `DllGetClassObject`는 0x18바이트 팩토리 객체를 할당하고 `AddRef`를 호출한다.

## `CClassFactory::CreateInstance`의 제어 흐름

- 출력 포인터 null이면 `E_POINTER` (`0x80004003`).
- 집계 객체가 전달되었고 요청 IID가 `IID_IUnknown`이 아니면 **원본은 `E_NOINTERFACE` (`0x80004002`)**. 일반 관례에 맞춰 다른 에러로 임의 교체하지 않는다.
- 팩토리 템플릿의 생성 함수를 간접 호출한다 (RVA **0x1FFF**); 콜백은 객체 포인터와 별도 HRESULT를 반환하는 구조.
- 포인터가 null이면 `E_OUTOFMEMORY` (`0x8007000E`).
- 생성 콜백의 HRESULT가 실패면 별도 가상 소멸자 슬롯 **+0x18**에 delete 플래그 1을 주어 정리 (**0x2031**), 해당 HRESULT를 반환한다.
- 성공 시 객체 `AddRef` (**0x204E**) → `QueryInterface` (**0x205D**) → 임시 `Release` (**0x206A**) 순서로 호출하고 QI 결과를 반환한다. QI가 실패해도 Release 경로를 지난다.

또한 **0x13F5, 0x140A, 0x6646, 0x6659**에서는 설정 객체의 **+0x48/+0x50**에 보관된 포인터의 vtable **+0x10** 슬롯을 호출해 해제하며, 구체적인 인터페이스 타입은 미확인이다. **0x8D4C**도 리스트 정리에서 같은 슬롯을 호출한다. **0x226D**는 DLL 초기화/종료 관련 선택적 함수 포인터 호출이지 WASAPI 메서드로 확인된 호출은 아니다.

분석용 별도 모델 및 23개 클래스 팩토리 명령어 대조표, 13개 신규 단위 테스트는 대화의 **Batch9 전체 ZIP**에 포함한다. GitHub의 간이 원본 검사기는 이 중 주요 18개 핀과 마지막 59개 호출 바이트를 검사한다. **Windows에서 실제 COM 동작·드라이버 동등성은 아직 미검증**이다.