# Documentation Ownership

문서는 실제 책임을 소유할 때만 둡니다. 파일이나 디렉터리가 존재한다는 이유만으로 문서를 만들지 않습니다.

## Scope Placement

문서 규칙은 **실제로 적용되는 가장 좁은 owner**가 소유합니다.

- repository 전체의 documentation principle이나 convention → `docs/document/`
- top-level documentation layout과 주요 surface routing → `docs/README.md`
- 특정 directory나 surface에만 적용되는 contract, navigation, maintenance 또는 recovery rule → 해당 directory의 `README.md` 또는 그 directory 안의 local document
- 개별 asset 또는 family에만 적용되는 maintainer knowledge → 해당 asset documentation capsule

`docs/document/`를 directory별 local contract의 registry로 사용하지 않습니다. 같은 local rule이 여러 directory에서 반복되기 시작하면 실제로 repository-wide 원칙인지 먼저 판단하고, 그렇다면 공통 owner로 승격합니다.

## Repository Entrypoints

| Surface | Responsibility |
| --- | --- |
| `README.md` | 사람에게 repository의 목적과 주요 시작점을 제공 |
| `AGENTS.md` | repository-local agent behavior와 작업 boundary 제공 |

## Directory Documentation

Directory-level README는 해당 directory의 contract 또는 navigation responsibility를 실제로 소유할 때 entrypoint로 둡니다.

다음은 local documentation의 근거가 됩니다.

- child source 이름만으로 복구하기 어려운 directory contract
- correctness나 recovery에 영향을 주는 진입 순서 또는 navigation decision
- 해당 directory만의 maintenance 또는 recovery knowledge

Sibling 파일 목록만 복제하는 index는 만들지 않습니다. 쉽게 재생성되는 inventory는 filesystem과 search에 맡깁니다.

문서의 공통 중복 원칙은 [DRY Boundaries](dry.md)가 소유하고, directory-local 중복 경계는 해당 local owner가 소유합니다.
