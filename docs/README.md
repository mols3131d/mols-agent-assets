# 저장소 문서 (`docs/`)

현재 운용에 필요한 repository guidance, 자산별 maintainer 문서 및 공통 reference를 보관합니다.

## 디렉터리 구조

| 디렉터리 / 파일 | 설명 |
| --- | --- |
| `development.md` | canonical/derived surface와 자산 개발·검증 workflow |
| `testing.md` | 자동화 테스트, AgentsMesh와 코드 품질 검증 가이드 |
| `<asset-type>/<asset-name>/` | 특정 자산에 실제로 필요할 때만 두는 maintainer-only 문서 |
| `references/common/` | 여러 자산 유형이 공유하는 standard, principle, authoring, concept, tooling reference |
| `references/<asset-type>/` | 특정 자산 유형 전체가 공유하는 reference |

완료된 migration 계획·census·작업 보고서는 current guidance로 유지하지 않습니다. 필요하면 Git history에서 복구합니다.

## 자산별 Maintainer 문서

`docs/<asset-type>/<asset-name>/`은 **선택적 surface**입니다. 모든 자산에 만들지 않고 canonical 자산만으로 안전하게 유지보수하기 어려울 때만 둡니다.

다음과 같은 경우에 검토합니다.

- 자산이 복잡해 purpose나 architecture를 source만으로 재구성하기 어렵다.
- 단순화·refactor 과정에서 중요한 intent, invariant 또는 non-goal이 훼손될 위험이 크다.
- durable decision이나 trade-off를 잃으면 잘못된 재설계 가능성이 높다.
- maintenance, recovery, migration 또는 compatibility 절차가 비자명하다.
- baseline을 별도로 보존하는 것이 향후 회귀·복구 비용을 실질적으로 낮춘다.

단순하고 self-explanatory한 자산에는 만들지 않습니다. 임시 조사·작업 로그, canonical source에서 쉽게 재생성되는 정보, runtime이 반드시 읽어야 하는 지식도 이곳에 두지 않습니다. Runtime-required resource는 해당 자산의 deployable/runtime surface가 소유합니다.

자산 유형 directory는 필요할 때만 생깁니다. 예를 들어 Skill 문서가 필요하면 `docs/skills/<skill-name>/`을 사용합니다. 비어 있는 유형 directory나 placeholder 문서를 미리 만들지 않습니다.

`docs/references/<asset-type>/`은 **유형 전체가 공유하는 지식**, `docs/<asset-type>/<asset-name>/`은 **특정 자산 하나의 보존·유지보수 지식**을 소유합니다.

Reference 파일명은 `README.md` 같은 directory index를 제외하고 lowercase kebab-case의 `<domain>[-<subdomain>...]-<topic>.md`를 사용합니다.
