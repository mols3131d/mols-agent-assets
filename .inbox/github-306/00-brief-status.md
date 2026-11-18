# PR #306 작업 현황 브리프

**2026-11-18 KST 기준:** [PR #306 — Skill 탐색 컨텍스트 비용 축소](https://github.com/mols3131d/mols-agent-assets/pull/306)는 열려 있으며, 병합하지 않았습니다. 변경 커밋 [`fa0ec41`](https://github.com/mols3131d/mols-agent-assets/commit/fa0ec41cf078459c241b7ab4cf0dc5916d7f0dc2)이 현재 PR head입니다. 최신 `main` [`df82086`](https://github.com/mols3131d/mols-agent-assets/commit/df82086d0fac43f96dea17ff92a64466605e9402)과 결합한 후보 [`76a4bfe`](https://github.com/mols3131d/mols-agent-assets/commit/76a4bfe320a8576d16b08503a8223deeb1b54147)의 PR Gate는 통과했습니다. 이 문서는 로컬 인계용 보조 자료이며 GitHub의 검증·승인 상태를 대신하지 않습니다.

| 항목 | 확인 상태 |
| --- | --- |
| PR 브랜치 | `mols3131d/perf/agent-route-context-cost` · local과 remote가 [`fa0ec41`](https://github.com/mols3131d/mols-agent-assets/commit/fa0ec41cf078459c241b7ab4cf0dc5916d7f0dc2)에서 일치 |
| 현재 원격 `main` | [`df82086`](https://github.com/mols3131d/mols-agent-assets/commit/df82086d0fac43f96dea17ff92a64466605e9402) |
| 최신 PR Gate | [run 44287224662](https://github.com/mols3131d/mols-agent-assets/actions/runs/44287224662) · merge candidate `76a4bfe` (`df82086` + `fa0ec41`) · 성공, 테스트 479개 통과 |
| 현재 PR 상태 | `OPEN` · auto-merge 비활성 · 병합하지 않음 |

## 구현된 변경

- [경량 `skills-brief.jsonl`](../../route/skills-brief.jsonl)은 정본 Skill 설명의 첫 문장과 `Also use`, `Also apply`, `Always load`로 시작하는 적용 조건을 보존합니다. 36개 이름·정본 URL·순서는 전체 [Skill 목록](../../route/skills.jsonl)과 일치하며, 전체·경량 목록은 LF 기준 25,968자에서 14,931자로 42.5% 줄었습니다.
- 경량 목록을 읽거나 파싱할 수 없으면 [상위 route 목록](../../route/routes.jsonl)의 Skill 항목이 제공하는 `fallback`으로 전체 목록을 읽습니다. 경량 목록을 읽었지만 후보가 없거나 적용 여부가 불분명할 때는 `_meta.fallback`을 따릅니다.
- [탐색 진입점](../../route/ROUTE.md)의 direct-load 예외는 정본을 아는 자산에만 적용합니다. 다른 자산의 발견이 필요하면 같은 유형이라도 route 탐색을 유지합니다.
- JSONL 파싱은 LF 경계로 레코드를 읽어 문자열 내부 `U+2028`을 보존합니다. 테스트는 `Also apply`, fallback, Unicode 입력을 포함합니다.

## 검증 근거와 한계

- 로컬 `mise run generated sync`와 `mise run generated validate` 성공. 전체·경량 Skill route의 이름·source·순서 일치 및 full Skill/Subagent route 비변경을 확인했습니다.
- 변경 파일 중심 결정론적 테스트 75개 통과; Lefthook pre-push의 전체 테스트 444개 통과.
- [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/44287224662): 실제 merge candidate `76a4bfe`에서 source frontmatter, 전체 pytest **479개**, `docs-indexes`·`distribution-routes`, mise Doctor, Rulesync config 및 configured projection 검증 성공. 루트 Rulesync 입력이 변경되지 않아 dependency install 단계는 조건부로 생략됐습니다.
- [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/44287216374)는 head `fa0ec41`에서 성공했습니다.
- 실제 모델의 Skill 선택 성공률, tokenizer 기준 토큰량, 호출량·지연 시간은 측정하지 않았습니다. 정적 설명 보존과 CI 통과는 runtime routing 품질의 실측 근거가 아닙니다.

## 다음 작업

1. PR의 독립 검토와 사람 승인을 완료합니다. Agent 제어·하네스 표면 변경이므로 이 브리프나 CI 통과는 승인이나 merge 권한을 대신하지 않습니다.
