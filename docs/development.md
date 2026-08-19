# 자산 개발 가이드

## Directory Roles

- `.agentsmesh/rules/`: AgentsMesh-managed Rule canonical source.
- `.agentsmesh/skills/`: AgentsMesh-managed Skill canonical source.
- `.agentsmesh/agents/`: AgentsMesh-managed Agent canonical source.
- `src/`: AgentsMesh contract 밖에 의도적으로 남기는 custom/non-standard Agent Asset exception만 유지.
- `tests/`: 자산 및 도구의 deterministic verification.
- `evals/`: behavioral/model eval과 cross-asset regression contract.
- `docs/<asset-type>/<asset-name>/`: 특정 자산에 필요할 때만 두는 maintainer-only 문서.
- `docs/references/`: 여러 자산이 공유하는 공통·유형별 reference.

AgentsMesh가 생성한 `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`는 derived target artifacts입니다. 직접 수정하지 않습니다.

현재 target이 canonical asset의 semantics를 완전히 지원하지 않더라도 canonical authority와 target capability를 구분합니다. 지원되지 않는 semantics를 portability 명목으로 삭제하거나 수동 projection으로 위조하지 않습니다.

현재 `src/` 아래에 필수 custom Agent Asset은 없습니다. 실제 target 또는 format 요구를 AgentsMesh로 표현할 수 없을 때만 예외를 추가하며, 빈 구조나 parallel source를 미리 만들지 않습니다.

## Skill Package Convention

Skill은 chatbot/agent 또는 flat/runtime으로 분류하지 않습니다.

모든 canonical Skill은 다음 경로에서 시작합니다.

```text
.agentsmesh/skills/<skill-name>/SKILL.md
```

`SKILL.md` 하나로 capability가 완결되면 **single-file Skill**로 유지합니다. 파일 길이나 runtime 존재만으로 분리하지 않습니다.

실행에 실제로 필요할 때만 같은 package에 `references/`, `scripts/`, `assets/`, `templates/` 같은 supporting resource를 추가합니다.

Single-file Skill에서는 top-level `#` heading을 여러 Markdown 문서의 responsibility boundary처럼 사용할 수 있습니다. 모든 heading은 하나의 명확한 책임을 가져야 하며, 불필요한 미세 분할은 하지 않습니다.

## Asset Documentation

자산별 maintainer 문서는 기본 산출물이 아닙니다. canonical source만으로 안전하게 유지보수하기 어렵거나 복잡성·훼손 위험·durable decision·recovery 지식이 별도로 보존될 가치가 있을 때만 `docs/<asset-type>/<asset-name>/`을 만듭니다.

- runtime이 읽어야 하는 정보는 deployable asset package에 둡니다.
- 임시 작업 로그와 쉽게 재생성되는 상태는 durable maintainer docs로 승격하지 않습니다.
- 완료된 migration 계획·보고서는 current guidance로 유지하지 않고 Git history에 맡깁니다.
- 유형 전체가 공유하는 지식은 `docs/references/<asset-type>/`이 소유합니다.
- 필요 없는 자산 유형 directory나 빈 placeholder 문서를 미리 만들지 않습니다.

## Workflow

1. `<owner>/<type>/<topic>` 브랜치를 생성합니다.
1. AgentsMesh가 표현할 수 있는 Rule, Skill, Agent는 `.agentsmesh/`에서 작성하거나 수정합니다. `src/`는 intentional custom/non-standard exception만 소유합니다.
1. 필요한 경우에만 자산별 maintainer docs를 함께 갱신합니다. 의도·불변조건·복구 기준이 바뀌지 않았다면 baseline을 기계적으로 수정하지 않습니다.
1. Markdown 변경은 repository rumdl policy에 맞춰 format합니다.
1. `npm ci`로 pinned AgentsMesh toolchain을 준비합니다.
1. AgentsMesh-managed 변경은 `npm run agentsmesh:lint` 후 `npx agentsmesh generate`로 active target projection을 갱신합니다.
1. `npm run agentsmesh:check`와 `npm run agentsmesh:generate:check`로 drift와 regeneration을 검증합니다.
1. 필요한 repository test/eval을 실행합니다.
1. canonical source와 generated artifacts를 같은 PR에서 검토한 뒤 배포 브랜치에 병합합니다.
