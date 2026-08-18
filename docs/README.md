# 저장소 문서 (`docs/`)

프로젝트 정책, 자산별 maintainer 문서 및 공통 reference를 보관합니다.

---

## 디렉터리 구조

| 디렉터리 / 파일 | 설명 |
| :--- | :--- |
| `agentsmesh-migration-plan.md` | Project EXODUS의 AgentsMesh 대이주 아키텍처와 cutover 계획 |
| `agentsmesh-migration-census.md` | EXODUS Phase 0 자산·권위·target capability·검증 baseline census |
| `agentsmesh-migration-report.md` | EXODUS 완료 상태, 실제 이주 범위, 예외, 검증 evidence와 RPWR 작업 기록 |
| `development.md` | 자산 개발 파이프라인 및 승격 가이드 |
| `testing.md` | 자동화 테스트, AgentsMesh와 코드 품질 검증 가이드 |
| `<asset-type>/<asset-name>/` | 특정 자산에 필요할 때만 두는 maintainer-only 문서 |
| `references/common/` | 자산 유형에 공통인 standard, principle, authoring, concept, tooling reference |
| `references/<asset-type>/` | Rule, Skill 등 특정 자산 유형 전체가 공유하는 reference |

## 자산별 Maintainer 문서

`docs/<asset-type>/<asset-name>/`은 **선택적 surface**다. 모든 자산에 만들지 않고,
canonical 자산만으로 안전하게 유지보수하기 어려울 때만 둔다.

다음과 같은 경우에 검토한다.

- 자산이 복잡해 purpose나 architecture를 source만으로 재구성하기 어렵다.
- 단순화·refactor 과정에서 중요한 intent, invariant 또는 non-goal이 훼손될 위험이 크다.
- durable decision이나 trade-off를 잃으면 잘못된 재설계 가능성이 높다.
- maintenance, recovery, migration 또는 compatibility 절차가 비자명하다.
- baseline을 별도로 보존하는 것이 향후 회귀·복구 비용을 실질적으로 낮춘다.

단순하고 self-explanatory한 자산에는 만들지 않는다. 임시 조사·작업 로그, canonical
source에서 쉽게 재생성되는 정보, runtime이 반드시 읽어야 하는 지식도 이곳에 두지 않는다.
Runtime-required resource는 해당 자산의 deployable/runtime surface가 소유한다.

자산 유형 directory는 필요할 때만 생긴다. 예를 들어 Skill 문서가 필요하면
`docs/skills/<skill-name>/`을 사용하고, Agent·Prompt·Rule도 같은 원칙으로
`docs/agents/`, `docs/prompts/`, `docs/rules/` 아래에 둘 수 있다. 비어 있는 유형
directory를 미리 만들지 않는다.

`docs/references/<asset-type>/`은 **유형 전체가 공유하는 지식**, `docs/<asset-type>/<asset-name>/`은
**특정 자산 하나의 보존·유지보수 지식**을 소유한다.

Reference 파일명은 `README.md` 같은 디렉터리 index를 제외하고 lowercase kebab-case의
`<domain>[-<subdomain>...]-<topic>.md`를 사용한다.
