# Catalog

이 디렉토리는 여러 프로젝트에서 다시 찾아 쓰기 좋은 reusable asset의 **curated discovery surface**입니다. 실제 작성 원본, 설치 상태와 dependency lock은 각 asset을 소유하는 canonical surface에 둡니다.

## Areas

- `skills.json` — 자주 재사용하는 외부 Agent Skill source와 설치 recipe
- `patterns/` — 이 repository의 reusable pattern library를 찾기 위한 entrypoint

## Skills

`skills.json`은 설치 상태나 dependency lock이 아니라 다시 찾고 설치하기 위한 catalog입니다. 각 entry의 `install`은 현재 source를 설치하기 위한 copy-paste recipe이며, 실제 target, scope, lock과 update 상태는 선택한 installer가 소유합니다.

각 항목은 필요한 최소 정보만 가집니다.

- `name` — catalog에서 식별할 이름
- `source` — upstream GitHub repository (`owner/repo`)
- `description` — 선택할 때 참고하는 짧은 설명
- `install.skills` — skills CLI로 직접 설치하는 명령
- `install.rulesync` — Rulesync declarative source로 추가하는 명령

예를 들어 같은 source를 다음 두 방식 중 하나로 설치할 수 있습니다.

```bash
npx skills add JuliusBrussee/caveman
rulesync add JuliusBrussee/caveman
```

`skills add`는 runtime의 project/global Skill 위치로 직접 설치할 때 사용합니다. `rulesync add`는 Rulesync workspace에서 source와 lock을 관리하고 이후 `rulesync generate` 흐름으로 배포할 때 사용합니다. 같은 dependency의 설치·update 상태를 두 installer에서 동시에 소유하지 않습니다.

고정 revision, 설치 경로, target별 상태와 computed hash 같은 lock 정보는 catalog에 두지 않습니다. 특정 repository가 실제 dependency로 사용하는 Skill의 상태는 해당 dependency 관리 surface가 소유합니다. CLI contract가 바뀌면 upstream을 확인하고 recipe를 갱신합니다.

## Patterns

Pattern 본문과 category 구조의 canonical source는 [`docs/references/patterns/`](../docs/references/patterns/)가 소유합니다. [`patterns/`](patterns/)는 이를 복제하지 않고 catalog에서 찾기 위한 entrypoint만 제공합니다.
