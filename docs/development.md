# 자산 개발 가이드

## Directory Roles

- `src/agentsmesh/rules/`: AgentsMesh-compatible Rule canonical source.
- `src/agentsmesh/skills/`: AgentsMesh-compatible Skill canonical source.
- `src/agentsmesh/agents/`: AgentsMesh-compatible Agent canonical source.
- `src/agentsmesh/agentsmesh.yaml`: temporary AgentsMesh workspace에 stage할 projection configuration.
- `src/`의 다른 경로: AgentsMesh contract로 표현할 수 없는 실제 custom/non-standard Agent Asset만 유지.
- `tests/`: 자산 및 도구의 deterministic verification.
- `evals/`: behavioral/model eval과 cross-asset regression contract.
- `docs/<asset-type>/<asset-name>/`: 특정 자산에 필요할 때만 두는 maintainer-only 문서.
- `docs/references/`: 여러 자산이 공유하는 공통·유형별 reference.

Repository root의 `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`는 canonical 또는 generated distribution surface로 commit하지 않습니다. 이 저장소가 보관한 자산을 자기 runtime configuration으로 오인하지 않게 하는 의도적인 trust boundary입니다.

현재 target이 canonical asset의 semantics를 완전히 지원하지 않더라도 canonical authority와 target capability를 구분합니다. 지원되지 않는 semantics를 portability 명목으로 삭제하거나 수동 projection으로 위조하지 않습니다.

## Skill Package Convention

Skill은 chatbot/agent 또는 flat/runtime으로 분류하지 않습니다.

모든 canonical Skill은 다음 경로에서 시작합니다.

```text
src/agentsmesh/skills/<skill-name>/SKILL.md
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

## Workflow

1. `<owner>/<type>/<topic>` 브랜치를 생성합니다.
1. AgentsMesh가 표현할 수 있는 Rule, Skill, Agent는 `src/agentsmesh/`에서 작성하거나 수정합니다.
1. 필요한 경우에만 자산별 maintainer docs를 함께 갱신합니다.
1. Markdown 변경은 repository rumdl policy에 맞춰 format합니다.
1. AgentsMesh-native 검증이 필요하면 `src/agentsmesh/`를 temporary workspace의 `.agentsmesh/`로 stage합니다.
1. `agentsmesh lint`, generation, drift check 같은 native command는 그 temporary workspace에서만 수행합니다.
1. 필요한 repository test/eval을 실행합니다.
1. canonical source를 검토합니다. temporary `.agentsmesh/`와 harness-native generated projection은 commit하지 않습니다.
