# Promptfoo 수동 평가 인계

[PR #322](https://github.com/mols3131d/mols-agent-assets/pull/322)의 비정본 작업 기록입니다. 실행 계약은 코드와 [정본 실행 안내](../../evals/README.md#promptfoo-provider-selection)를 따릅니다.

## 확정 범위

Promptfoo `0.126.0`에서 Ollama와 Codex를 명시적으로 선택하는 수동 평가를 지원합니다. Grader 사용 여부와 모델도 독립적으로 선택합니다. 실제 모델·grader 실행은 사용자가 요청한 경우에 한합니다. Antigravity는 오너 결정에 따라 후속 PR로 분리했습니다. 후속 검토에는 공식 Python SDK와 Gemini API 인증의 적용 조건이 포함됩니다. [Antigravity 공식 FAQ](https://antigravity.google/docs/faq#can-i-use-antigravity-cli-headless-mode-in-third-party-coding-agents-or-automate-account-switching)

## 작업 기준

- 대상은 `main`을 기준으로 한 Draft PR #322와 브랜치 `mols/feat/promptfoo-manual-providers`입니다.
- 최초 인계 시점 HEAD는 [`1f1809a`](https://github.com/mols3131d/mols-agent-assets/commit/1f1809a2ddfb78c6e2b0ad5f952e484c80b0a9a1)였습니다. 당시 Branch Check와 PR Gate는 평가 문서의 링크 fragment 오류로 실패했습니다.
- [Provider 통합 결정](01-plan-provider-integration.md)과 [검증 기준](02-plan-verification.md)을 현재 PR 본문 및 최신 HEAD에 대조합니다. 브랜치·검사 상태는 GitHub에서 확인합니다.

## 작업 경계

기존 fixture와 strict assertion을 유지합니다. 검증에는 고정 fixture와 test double을 사용합니다. 실제 모델 평가, 모델 다운로드, 로그인·계정 전환 및 유료 API 사용은 후속 검증 승인에 따릅니다. CI, hook, bootstrap과 일반 check는 deterministic 검증을 수행합니다.
