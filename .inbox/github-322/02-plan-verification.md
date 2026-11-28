# 검증 및 완료 기준

[인계 요약](00-handoff-promptfoo.md)과 [구현 결정](01-plan-provider-integration.md)을 최신 PR diff와 확인합니다.

## 모델 호출 없는 검증

| 대상 | 검증 기준 |
| --- | --- |
| Runner | 도움말, 누락·빈 값·구성 교체 옵션은 provider 호출 전에 종료 |
| Provider 선택 | Ollama·Codex 또는 고정 fixture에 명시한 대상만 전달 |
| Grader | 독립적인 모델 선택, `none`에서 deterministic assertion 보존, Echo calibration에서 명시적 grader 요구 |
| 입력·응답 | Ollama 채팅, Codex agent 입력, Python provider와 assertion 연결을 fixture 또는 test double로 확인 |
| 인증·격리 | 가짜 키와 상태 응답으로 ChatGPT/API 경로 분리, 빈 작업 디렉터리와 제한 설정 확인 |
| 버전·형식 | Promptfoo `0.126.0` 버전, CLI help와 config schema, Node 하한 확인 |
| 저장소 | 전체 pytest, 변경 파일 source quality, frontmatter, 생성물 검증 및 최신 HEAD의 Branch Check·PR Gate 결과 확인 |

Promptfoo CLI의 fixture smoke 및 provider test double 결과는 plumbing evidence로 기록합니다. 일반 테스트 및 CI에서는 평가 명령을 시작하지 않습니다.

## 실제 provider 검증

사용자가 대상 case, provider/model, 필요한 grader와 인증·전송·비용 조건을 지정할 때만 최소 실제 평가를 시작합니다. 모델 다운로드와 별도 유료 호출도 요청 범위를 따릅니다. 실제 provider 가용성, 계정·플랫폼 호환성과 모델 품질은 미실행으로 기록합니다.

## 완료 판정

Ollama와 Codex 구현·정본 문서·검증 결과를 PR 본문과 맞춥니다. 최종 HEAD의 검사 근거를 Saki에게 넘기고 Akane 리뷰를 요청합니다. Draft 전환과 merge는 오너의 권한에 따릅니다.
