# 로컬 에이전트 인계 — PR #256 Skill 모델 Eval

최신 후속 작업은 [Eval 개선 인계](bootstrap-eval-improvement-handoff-2026-10-25.md)를 따른다. 아래는 기존 11-case 실행 계획과 그 당시의 인계 기록이다.

> 대상: `mols3131d/mols-agent-assets` · 브랜치: `mols/feat/dev-environment-bootstrap` · [PR #256](https://github.com/mols3131d/mols-agent-assets/pull/256) (Draft)
>
> **인계 실행 완료 / 행동 품질 미달.** 최신 11건을 두 로컬 모델로 실행하고 [결과·개별 기준 판정](bootstrap-eval-results-2026-10-25.md)을 남겼다. 자동 채점 위양성과 provider 오류를 구분했으며 Draft를 유지한다. 다음 과제는 grader 보정과 제한된 행동 개선이다. 아래 절차는 재평가 시 참고한다. 환경 부트스트랩 구현은 [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258)의 별도 작업.

## 작업

1. 저장소 지침(`AGENTS.md`, 관련 개발·Eval 정책)을 따르고, **현재 PR HEAD와 working tree**를 확인한다. 기존 사용자 변경은 보존한다.
1. 평가 대상은 [Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md), [11건 fixture](../../evals/skills/mols-dev-env-bootstrap-design/cases.json), [Promptfoo 설정](../../evals/promptfoo/mols-dev-env-bootstrap-design.yaml)이다. 기존 `package.json` 진입점과 `scripts/agent_assets/{skills_promptfoo.py,promptfoo_run.py}`을 **그대로 재사용**한다.
1. **읽기 전용 사전 점검:** Node(>=22.22.0), npx, uv, Ollama 서비스 및 이미 설치된 실행·채점 모델을 확인한다. `OLLAMA_BASE_URL`, `PROMPTFOO_GRADER_PROVIDER`, 기존 Promptfoo 경로 설정이 로컬 전송·캐시·쓰기 대상을 바꾸는지 확인한다.
1. `uv run`의 프로젝트 환경 동기화, `npx --yes`의 Promptfoo 다운로드, 모델 pull·공유 캐시 쓰기가 필요하면 **영향과 위치를 설명하고 사전 승인**을 받는다. 승인이나 안전한 로컬 전송 경로가 없으면 실행하지 않고 차단 사항을 보고한다. 전역 설정·HOME·훅 수정과 무단 설치 금지.
1. 사용할 모델과 grader가 준비되면 기존 기본 설정을 활용하고, 필요한 경우에만 **해당 명령 실행 범위**에서 기존 `PROMPTFOO_RUNTIME_MODEL`·`PROMPTFOO_GRADER_PROVIDER`를 지정한다. 실행 조건·정확한 모델 ID를 기록한다.

```bash
npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=trigger
npm run eval:promptfoo:mols-dev-env-bootstrap-design -- --filter-metadata suite=behavior
```

## 평가·기록

- **Trigger 6건:** 적용 3건/비적용 3건의 예상 선택과 실제 JSON을 비교한다. 이 실험은 **단일 Skill 후보의 metadata 선택**으로, 실제 다중 Skill 라우팅을 증명하지 않는다.
- **Behavior 5건:** 실제 답변을 읽고 각 사례의 assertion 3개씩 **총 15개**를 충족/미충족/불명으로 판정한다. grader의 점수·사유와 대조하며, 안전 조건 누락을 총점으로 덮지 않는다.
- 오류는 **모델 행동 / provider·schema / fixture·runner / grader**로 구분한다. 의심되는 사례만 조건을 고정해 제한적으로 재실행한다. 과거 영문 10건 결과와 최신 한국어 11건을 혼합하지 않는다.
- 결과를 `inbox/github-256/`의 **평가 결과 문서 1개**로 정리하고, 사용 모델·grader·버전·HEAD·실행 명령, 사례별 판정 및 미검증 사항을 기록한다. 민감한 raw 로그는 GitHub에 올리지 않는다. PR 설명은 관찰된 결과만 갱신하고 Draft를 임의로 해제하거나 병합하지 않는다.

**완료 기준:** 최신 11건에 대한 실행 결과와 오류·채점 차이를 재현 가능한 수준으로 보고하거나, 실행 불가 사유와 필요한 승인·선행조건을 명확히 인계한다. 실행하지 못한 검사를 통과로 기록하지 않는다.

세부 근거와 반례가 필요할 때만 [평가 계획](bootstrap-eval-plan-2026-10-25.md), [채점 검토](bootstrap-eval-plan-child-grader-2026-10-25.md), [환경 영향 검토](bootstrap-eval-plan-child-runtime-2026-10-25.md)를 읽는다.
