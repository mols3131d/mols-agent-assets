# Catalog

이 디렉토리는 여러 프로젝트에서 다시 찾아 쓰기 좋은 reusable asset의 **curated discovery surface**입니다. 실제 작성 원본, 설치 상태와 dependency lock은 각 asset을 소유하는 canonical surface에 둡니다.

## Areas

- `skills.json` — 자주 재사용하는 외부 Agent Skill source와 사용할 수 있는 installer 목록
- `patterns/` — 이 repository의 reusable pattern library를 찾기 위한 entrypoint

## Skills

`skills.json`은 설치 상태나 dependency lock이 아니라 다시 찾고 설치하기 위한 catalog입니다. Catalog는 **무엇을 설치할지**만 기록하고, installer의 CLI syntax와 설치·update 동작은 각 installer가 소유합니다.

각 항목은 필요한 최소 정보만 가집니다.

- `name` — catalog에서 식별할 이름
- `source` — asset의 canonical upstream URL. GitHub에 한정하지 않습니다.
- `description` — 선택할 때 참고하는 짧은 설명
- `installers` — 이 source를 사용할 수 있는 installer 이름

현재 installer 식별자는 `skills cli`와 `rulesync`를 사용합니다. Installer는 `source` URL을 자신의 source contract에 맞게 처리하며, CLI syntax, target, scope, revision, lock과 update 옵션은 해당 installer가 소유합니다.

같은 dependency의 설치·update 상태를 여러 installer가 동시에 소유하지 않습니다. 특정 source가 한 installer와 호환되지 않으면 그 installer를 `installers`에 넣지 않습니다.

고정 revision, 설치 경로, target별 상태와 computed hash 같은 lock 정보도 catalog에 두지 않습니다. 특정 repository가 실제 dependency로 사용하는 Skill의 상태는 해당 dependency 관리 surface가 소유합니다.

## Patterns

Pattern 본문과 category 구조의 canonical source는 [`docs/references/patterns/`](../docs/references/patterns/)가 소유합니다. [`patterns/`](patterns/)는 이를 복제하지 않고 catalog에서 찾기 위한 entrypoint만 제공합니다.
