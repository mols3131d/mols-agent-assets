# Coding Context 변경 리뷰

2026-11-25 기준 [PR #320](https://github.com/mols3131d/mols-agent-assets/pull/320)의 변경된 지침을 리뷰에 적용하지 않고 기존 정책과 원본을 기준으로 정적 검토했다.

- Base: `e839deafd3f1678f9ed50a8c8fcfe2bbdddc8e45`
- Head: `73cd2aeba5fb4474783d089ecfb23f563ea70f99`
- 판정: 설계 방향 수용, 머지 준비 미완료. Blocker/High/Medium 0건, Low 1건.
- 범위: [변경 파일 6개](https://github.com/mols3131d/mols-agent-assets/pull/320/files), 기존 Core·레거시·Python 원본, 공개 route, 유지보수 문서, 관련 평가 fixture와 runner.

## Finding

### R1 — LOW / CONFIRMED: 평가 후보의 이전 description

[evals/skills/mols-test-design/cases.json:15–20](https://github.com/mols3131d/mols-agent-assets/blob/73cd2aeba5fb4474783d089ecfb23f563ea70f99/evals/skills/mols-test-design/cases.json#L15-L20) 등 6개 후보 정의가 변경 전 mols-coding-context description을 사용한다. [평가 runner](https://github.com/mols3131d/mols-agent-assets/blob/73cd2aeba5fb4474783d089ecfb23f563ea70f99/scripts/agent_assets/skills_promptfoo.py#L682-L697)는 주입된 discovery metadata로 라우팅을 평가한다.

기존 fixture의 성공은 변경된 Core metadata와 mols-test-design의 실제 조합 선택 근거가 되지 않는다. 평가 실패나 실제 라우팅 회귀가 발생했다는 뜻은 아니다. 현행 조합 평가를 의도했다면 description을 갱신하고, 고정 비교 조건이라면 그 의도를 확인한다. 별도 자동 동기화 도구나 문자열 일치 gate의 필요성은 입증되지 않았다.

## 설계 판단

- Core: 범용 판단의 통합, 근거와 해결책의 독립 평가, 추측성 방어 억제와 정당한 실패 처리의 균형, 관찰 가능한 계약의 보존이 적절하다. 추가적인 실행 절차나 일괄 압축은 권장하지 않는다.
- Python: Core 중복을 걷어내고 예외·typing·import·asyncio·interpreter/build 판단에 집중한 방향이 타당하다. 신규 판단은 실제 실패 근거 없이 추가하지 않는다.
- 유지보수 문서: 실행 계약과 변경 판단의 분리, Python의 Core 참조, route description의 일치가 적절하다. 새로운 문서 계층은 필요하지 않다.
- 비용: 정적 압축은 확인했으나 토큰 사용량, 추론 비용, 품질 향상과 행동 동등성은 실측하지 않았다.

## 검증과 한계

| 항목 | 결과 |
| --- | --- |
| PR Gate | [성공](https://github.com/mols3131d/mols-agent-assets/actions/runs/45584007104), 검토 당시 HEAD |
| Branch Check | [성공](https://github.com/mols3131d/mols-agent-assets/actions/runs/45583998092), 검토 당시 HEAD |
| 원본·diff·route 비교 | 정적 검토 수행 |
| 외부 소비자 | 일부 검색 결과에서 새 이름 사용 확인; 레거시 의존성 전수 확인 및 이관 미완료 |
| 모델 행동·선택·재사용 | 미실행 |
| 격리된 독립 Subagent | 실행 환경 부재로 미수행; 이번 정적 리뷰를 격리된 독립 리뷰로 승격하지 않음 |

PR 자체의 명시적 완료 조건은 아직 충족되지 않았다. 이후 작업은 [로컬 작업 제안](01-handoff-coding-context.md)을 참고한다. 새 base/head에서는 검증 결과를 다시 확인한다.
