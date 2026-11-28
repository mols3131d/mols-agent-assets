# Provider 통합 구현 결정

[인계 요약](00-handoff-promptfoo.md)의 확정 범위에 따라 Promptfoo `0.126.0`과 Ollama·Codex를 사용합니다. 사용법과 환경 변수는 [평가 README](../../evals/README.md#promptfoo-provider-selection)가 소유합니다.

- Runner는 저장소 suite 하나와 명시적 모델 선택을 검증한 뒤 해당 설정만 임시 디렉터리에서 실행합니다. Promptfoo의 필터·출력 옵션을 전달하며 입력·provider·공유를 바꾸는 옵션은 거부합니다.
- Native Ollama는 chat 메시지와 HTTP 요청 제한을 사용합니다. `mols-test-design`은 JSON과 Reference metadata를 구성하는 Python Ollama 경로를 유지합니다.
- Native Codex는 고정 SDK와 CLI를 선택할 때만 npm으로 해석합니다. Agent prompt, structured output, 별도 case 제한 및 읽기 권한을 사용합니다. ChatGPT 로그인 방식은 전용 Codex home을 사용하며 API 방식은 임시 home과 지정 키를 사용합니다. [Promptfoo SDK 구현](https://github.com/promptfoo/promptfoo/blob/0.126.0/src/providers/openai/codex-sdk.ts)
- `--grader none`은 semantic rubric을 제외하고 deterministic assertion을 적용합니다. Semantic grader는 선택한 Ollama 또는 Codex를 호출합니다. Calibration은 고정 응답을 Echo로 재생하고 선택한 grader만 호출합니다.
- 최신 `main`의 자산 퇴역을 반영해 현재 native suite 두 개를 연결하고 fixture smoke에는 부트스트랩 설계 사례를 사용합니다.
- Antigravity는 후속 작업에서 공식 Python SDK와 Gemini API 인증의 허용 범위를 확인합니다.

[검증 기준](02-plan-verification.md)을 따라 실제 모델 실행과 fixture 배선 근거를 구분합니다.
