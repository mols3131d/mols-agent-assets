# 저장소 문서 (`docs/`)

프로젝트 정책, 자산 설명서 및 가이드 문서 보관 공간입니다.

---

## 디렉터리 구조

| 디렉터리 / 파일 | 설명 |
| :--- | :--- |
| `agentsmesh-migration-plan.md` | AgentsMesh 기반 Agent Asset 대이주 아키텍처 및 단계별 migration 계획 |
| `development.ko.md` | 자산 개발 파이프라인 및 승격 가이드 |
| `testing.ko.md` | 자동화 테스트 및 코드 품질 검증 가이드 |
| `skills/<skill-name>/` | 개별 자산별 사람용 가이드 및 문서 |
| `references/common/` | 자산 유형에 공통인 standard, principle, authoring, concept, tooling reference |
| `references/<asset-type>/` | Rule, Skill 등 특정 자산 유형만의 reference |

Reference 파일명은 `README.md` 같은 디렉터리 index를 제외하고 lowercase kebab-case의 `<domain>[-<subdomain>...]-<topic>.md`를 사용합니다.
