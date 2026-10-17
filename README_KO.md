# ASIOGLLD 원본 역공학 프로젝트

원본 DLL 기반 기능/구조 복원을 먼저 진행합니다. Cubase 8.0.40 재생 안정화가 최종 목표이며, **유튜브와 Cubase 동시 재생을 위해 WASAPI 공유 모드를 필수 조건**으로 유지합니다.

## 현재 성과

- 두 번 업로드된 DLL의 SHA-256이 같음을 검증했습니다.
- x64 PE 함수·외부 API·정적 호출 관계를 수집했습니다.
- RTTI 기반으로 `CAsio`의 ASIO 메서드 24개 엔트리를 원본 RVA에 연결했습니다.
- `CClassFactory`, `CMMAudioPort`, `CNotificationClient` 등 객체를 식별했습니다.
- WASAPI `IAudioClient`, `IAudioRenderClient`, `IAudioCaptureClient`, `IAudioClock` GUID와 참조 위치를 식별했습니다.
- 아직 **원본 소스 전체 복원, Cubase 드롭아웃 원인 규명, 바이너리 수정, 성능 개선 검증은 미완료**입니다.

분석 근거: [ASIO VTable](docs/ASIO_VTABLE.md), [WASAPI GUID](docs/WASAPI_GUID_MAP.md), [내부 호출](docs/CONTROL_FLOW.md), [진행 상태](docs/STATUS.md).

## 정적 분석 재현

```sh
python tools/pe_inventory.py "D:\\path\\asioglld.dll"
```

실행은 읽기 전용이며 원본 DLL을 변경하지 않습니다.

## Ghidra 전체 함수 디컴파일 시도

1. 공식 Ghidra 설치 및 필요한 JDK 준비: https://github.com/NationalSecurityAgency/ghidra/releases
2. 원본 `asioglld.dll`을 이 프로젝트 아래 `original/asioglld.dll`로 복사 (원본은 GitHub에 업로드하지 않음).
3. Windows CMD에서 `set "GHIDRA_HOME=D:\\your-ghidra-folder"`로 경로 설정.
4. `tools\ghidra\RUN_GHIDRA_WINDOWS.cmd` 실행.
5. `local_output\decompiled\SUMMARY.txt` 및 `functions.tsv` 확인.

스크립트는 원본 SHA-256을 검사하고 지정된 로컬 출력 폴더에 디컴파일 결과를 기록합니다. **아직 실제 Windows Ghidra 컴파일/실행 검증 전**입니다. 오류가 발생하면 먼저 오류 메시지를 확인하고 스크립트부터 수정해야 합니다.

전체 디컴파일 출력은 저작권과 라이선스 문제를 고려해 **공개 GitHub에 올리지 않고 로컬에 보관**하세요. 원본과 연결된 재현 가능한 분석 문서 및 직접 작성한 코드만 GitHub에 유지합니다.

공개 GitHub 경로: https://github.com/skatmdgn/ASIOGLLD
