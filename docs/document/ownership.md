# Documentation Ownership

문서는 실제 책임을 소유할 때만 둡니다. 파일이나 디렉터리가 존재한다는 이유만으로 문서를 만들지 않습니다.

## Repository Entrypoints

| Surface | Responsibility |
| --- | --- |
| `README.md` | 사람에게 repository의 목적과 주요 시작점을 제공 |
| `AGENTS.md` | repository-local agent behavior와 작업 boundary 제공 |

## Directory Documentation

Directory-level README는 해당 directory의 contract 또는 navigation responsibility를 실제로 소유할 때 entrypoint로 둡니다.

다음은 독립 문서의 근거가 됩니다.

- child source 이름만으로 복구하기 어려운 directory contract
- correctness나 recovery에 영향을 주는 진입 순서 또는 navigation decision
- 해당 directory만의 maintenance 또는 recovery knowledge

Sibling 파일 목록만 복제하는 index는 만들지 않습니다. 쉽게 재생성되는 inventory는 filesystem과 search에 맡깁니다.

문서의 중복 허용 범위는 [DRY Boundaries](dry.md)가 소유합니다.
