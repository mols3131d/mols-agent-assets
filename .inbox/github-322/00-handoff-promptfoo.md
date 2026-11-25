# Promptfoo 수동 평가 인계

[PR #322](https://github.com/mols3131d/mols-agent-assets/pull/322)의 후속 구현을 위한 비정본 작업 자료다. 목표와 작업 상태는 PR, 확정된 실행 계약은 코드와 정본 문서가 소유한다.

## 목표

Promptfoo 안정 릴리스를 Exact pin으로 갱신하고 Codex, Antigravity, Ollama를 선택해 평가할 수 있도록 한다. **평가는 사용자가 요청한 경우에만 선택한 대상·provider·model로 실행한다.** Grader 호출도 동일한 승인 범위에 포함된다.

## 재개 지점

- 대상: `mols-agent-assets`, PR #322 (Draft)
- Base: `main` / [`0a3e41016e8266276f2a5124a19a229844bd7a98`](https://github.com/mols3131d/mols-agent-assets/commit/0a3e41016e8266276f2a5124a19a229844bd7a98)
- 작업 브랜치: `mols/feat/promptfoo-manual-providers`
- 인계 전 구현 기준: [`b4ea994aa5edcef857448389a035d128f6716798`](https://github.com/mols3131d/mols-agent-assets/commit/b4ea994aa5edcef857448389a035d128f6716798)
- 비교: [구현 기준 diff](https://github.com/mols3131d/mols-agent-assets/compare/0a3e41016e8266276f2a5124a19a229844bd7a98...b4ea994aa5edcef857448389a035d128f6716798)

재개할 때 최신 PR head와 base, 작업 트리, 변경 소유권을 확인한다. 위 SHA는 인계 문서 커밋 이전의 구현 기준이며 현재 head를 대체하지 않는다. 기존 변경을 보존하고 같은 PR에서 이어서 작업한다.

## 현재 상태

| 항목 | 확인한 상태 |
| --- | --- |
| CLI 버전 | 0.122.0 → 0.126.0 pin 변경 완료; 설치·실행 호환성 미검증 |
| 수동 실행 | 인수 없는 `mise run eval`은 사용법 출력 후 종료하도록 변경; 회귀 테스트 작성, 미실행 |
| 정책 | CI·평가·Promptfoo 문서에 자동 모델 평가 금지 반영 |
| Provider 선택 | 기존 환경변수 및 Ollama 기본값 유지 중; 명시 선택 강제 미구현 |
| Codex | upstream native provider 확인; repository 연동 미구현 |
| Antigravity | 공식 headless 경로 조사; 인증·약관 경계와 adapter 구현 미완료 |
| 검증 | 실제 모델·grader 호출, CLI smoke, 단위 테스트 실행, 최종 self-review 미수행 |

PR의 미완료 항목을 최신 diff와 대조하여 진행한다. 특히 bare eval만 차단했으므로 현재 `eval --filter-...`처럼 config를 생략하는 실행이나 기존 모델 fallback까지 안전하다고 간주하지 않는다.

## 읽을 자료

- [01-plan-provider-integration.md](01-plan-provider-integration.md): 구현 선택지, 정본 경로, provider별 조사 근거와 위험.
- [02-plan-verification.md](02-plan-verification.md): 모델 호출 없는 검증, 수동 평가 인계 및 완료 기준.
- [루트 AGENTS.md](../../AGENTS.md): 해당 경로의 추가 지침과 함께 적용한다.
- [평가 정책](../../docs/development/evaluation.md), [평가 사용법](../../evals/README.md), [Promptfoo 도구 정책](../../docs/tools/promptfoo.md): 변경할 정본이다.

## 작업 경계

평가 실행, 모델 다운로드, 로그인·계정 전환, 원격 API 호출을 작업 준비나 검증의 일부로 자동 수행하지 않는다. 설치·버전 확인과 모델 실행을 구분한다. Antigravity 개인 구독의 제3자 앱 연동은 공식 허용 근거가 확보되기 전까지 활성화하지 않는다. 기존 fixture·assertion 의미를 보존하며 자동화 확대나 별도 평가 플랫폼 도입은 범위 밖이다.

PR은 구현과 검토를 이어가기 위한 Draft 상태다. 완료 판단과 merge는 저장소 정책 및 승인 조건에 따른다.
