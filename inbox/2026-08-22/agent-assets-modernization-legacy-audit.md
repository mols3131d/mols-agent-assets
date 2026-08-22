# Agent Asset Modernization — Legacy Audit

Current `main`의 canonical reusable Agent Asset을 기준으로 legacy modernization 1차 결과를 기록한다.

- Baseline: `2eda71db25779b64874cb13319e5e91d718efe80`
- Canonical source: `src/rulesync/.rulesync/`
- Scope: reusable Skills + reusable Subagents
- Current reusable Rule assets: 없음
- 이 문서는 완료 checkpoint이며 영구 registry가 아니다. 이후 audit은 current source를 다시 조사한다.

## Verdict

| Status | Count | Meaning |
| --- | ---: | --- |
| 🔴 Legacy | 0 | 현재 canonical source에 confirmed legacy가 남아 있지 않음 |
| 🟠 Review candidate | 0 | disposition이 필요한 legacy 후보가 남아 있지 않음 |
| 🟡 Experimental | 1 | 의도적으로 experimental lifecycle을 유지하는 자산 |
| 🟢 Current | 24 | 현재 architecture에서 독립 책임이 있고 legacy evidence가 없음 |
| **Total** | **25** | 22 Skills + 3 Subagents |

`Current`는 legacy evidence가 없다는 뜻이며 모든 자산의 deep quality validation이 완료됐다는 뜻은 아니다.

## Completed Dispositions

### `load-context-github` — removed

기존 이름은 `github-context` migration을 위한 temporary compatibility alias였다.

PR #123에서 다음을 완료했다.

- root `rulesync.jsonc` self-consumer를 `github-context`로 전환
- `rulesync.lock` refresh
- canonical `load-context-github` Skill 삭제
- `route/skills.jsonl`에서 legacy alias 제거
- Rulesync source, route, deterministic verification 통과

따라서 confirmed legacy Skill은 현재 0개다.

### `review-*` family — keep + modernize

`review-lead`, `review-quality`, `review-adversarial`은 Agent Asset-specific validator와 책임이 겹치는 것처럼 보였지만, 실제로는 generic bounded technical review라는 독립 책임이 남아 있었다.

PR #125에서 family-level disposition을 `keep + modernize`로 확정했다.

- `review-lead` → read-only dual-perspective coordinator와 final assessment owner
- `review-quality` → intended behavior/correctness/regression/integration/validation specialist
- `review-adversarial` → reachable failure/trust-boundary/recovery/hidden-assumption specialist
- specialist는 candidate claims와 unknowns만 handoff하고 최종 disposition은 lead가 소유
- Copilot IDE/CLI, Antigravity IDE/CLI target metadata를 current Rulesync semantics에 맞춤
- 세 reviewer 모두 reviewed target을 직접 수정하지 않음

새 `Subagent Orientation` pattern과도 정합성을 확인했다. Lead는 role-oriented 쪽, 두 specialist는 bounded capability/handoff 쪽에 더 가깝지만 모두 mixed orientation을 허용한다.

### `caveman-ko` — experimental by choice

Legacy가 아니라 experimental style Skill로 유지한다.

후속 현대화에서 다음 mismatch를 정리했다.

- 일반적인 brevity/token-saving 요청에는 auto-trigger하지 않고 explicit caveman-style intent에만 activation
- semantic preservation과 required clarity를 invariant로 강화
- activation lifetime을 명시
- package 내부 WIP README 제거
- experimental capability eval 추가
- upstream provenance/license metadata 정리

따라서 experimental 상태와 discovery behavior가 모순되던 기존 문제는 해소됐다. Stable 승격 여부는 향후 실제 사용 evidence에 따라 별도 판단한다.

## Current Context Family

Legacy alias 제거 후 context-oriented Skill 이름은 다음 current set으로 정리됐다.

- `coding-context`
- `github-context`
- `guidance-context`
- `notion-context`

## Completion

Legacy modernization 1차 campaign은 다음 기준을 충족한다.

1. confirmed legacy asset이 canonical source와 active route에 남아 있지 않다.
1. review candidate는 `keep + modernize` disposition을 갖는다.
1. experimental asset은 maturity와 discovery behavior가 충돌하지 않는다.
1. current asset은 legacy cleanup 때문에 불필요하게 재설계하지 않았다.

앞으로는 파일 길이, supporting file 수, vendor metadata, 내부 consumer 부재, compatibility 책임만으로 legacy를 판정하지 않는다. Superseded owner, temporary migration bridge, responsibility absorption, obsolete architecture/workflow coupling, 또는 사라진 current need 같은 evidence를 요구한다.

완료된 migration history는 Git history와 PR이 소유한다.
