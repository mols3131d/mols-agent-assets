# 저장소 문서 (`docs/`)

프로젝트 정책, 자산 설명서 및 가이드 문서 보관 공간입니다.

---

## 디렉터리 구조

| 디렉터리 / 파일 | 설명 |
| :--- | :--- |
| `agentsmesh-migration-plan.md` | Project EXODUS의 AgentsMesh 대이주 아키텍처와 cutover 계획 |
| `agentsmesh-migration-census.md` | EXODUS Phase 0 자산·권위·target capability·검증 baseline census |
| `agentsmesh-migration-report.md` | EXODUS 완료 상태, 실제 이주 범위, 예외, 검증 evidence와 RPWR 작업 기록 |
| `development.md` | 자산 개발 파이프라인 및 승격 가이드 |
| `testing.md` | 자동화 테스트, AgentsMesh와 코드 품질 검증 가이드 |
| `skills/<skill-name>/` | AgentsMesh-managed portable Skill의 maintainer-only guide, baseline, decision 및 recovery 문서 |
| `references/common/` | 자산 유형에 공통인 standard, principle, authoring, concept, tooling reference |
| `references/<asset-type>/` | Rule, Skill 등 특정 자산 유형만의 reference |

`docs/skills/<skill-name>/`은 target에 배포되는 Skill package가 아니다. `.agentsmesh/skills/<skill-name>/`이 deployable canonical source이며, 사람·maintainer용 비런타임 문서는 이곳에서 분리해 관리합니다.

Reference 파일명은 `README.md` 같은 디렉터리 index를 제외하고 lowercase kebab-case의 `<domain>[-<subdomain>...]-<topic>.md`를 사용합니다.
