# Documentation Ownership

이 문서는 repository documentation을 줄이거나 추가할 때 적용하는 **entrypoint와 ownership 결정의 durable rationale**을 기록합니다.

## Decision

문서는 파일이나 디렉터리가 존재한다는 이유만으로 만들지 않습니다. 각 문서는 child source만으로 복구하기 어려운 contract, durable decision, recovery knowledge 또는 실제 navigation responsibility를 소유해야 합니다.

Repository root의 일반 entrypoint는 다음 책임으로 구분합니다.

| Surface | Responsibility |
| --- | --- |
| `README.md` | 사람에게 저장소의 목적과 주요 시작점을 제공 |
| `AGENTS.md` | repository-local agent behavior와 작업 boundary 제공 |

서로 다른 entrypoint가 같은 policy body를 복제하지 않습니다. Linked source가 자기 의미의 authority를 유지합니다.

## Directory Documentation

Directory-level README 또는 index는 기본 산출물이 아닙니다.

다음 중 하나를 실제로 소유할 때만 둡니다.

- child files의 이름만으로 복구할 수 없는 directory contract
- 진입 순서가 correctness나 recovery에 영향을 주는 navigation decision
- 해당 directory만의 maintenance 또는 recovery knowledge

Sibling 문서를 단순 열거하기 위한 index-only README는 만들지 않습니다. 파일 목록과 쉽게 재생성되는 상태는 filesystem, search와 Git history에 맡깁니다.

## Durable vs Historical Knowledge

Repository에 남길 것은 현재와 미래의 판단을 바꾸는 지식입니다.

- 유지: durable decision, invariant, recovery knowledge, non-obvious rationale
- 유지하지 않음: 완료된 migration log, 일회성 작업 상태, 쉽게 재생성되는 inventory, PR별 진행 기록

역사적 맥락만 필요한 경우 Git history와 PR을 사용합니다. 현재 behavior를 이해하거나 안전하게 변경하기 위해 rationale이 계속 필요하면 development documentation으로 승격합니다.

## Boundary

이 문서는 각 Skill의 maintainer contract, testing policy, Rulesync integration detail 또는 Agent Skills specification을 소유하지 않습니다. 해당 내용은 각각의 canonical source나 좁은 reference가 소유합니다.
