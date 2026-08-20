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

## Knowledge and Artifact Lifecycle

정보의 현재성, authority와 보존 가치를 분리합니다.

| Kind | Destination | Meaning |
| --- | --- | --- |
| Current durable knowledge | canonical source 또는 `docs/` | 현재와 미래의 판단을 계속 바꾸는 decision, invariant, recovery knowledge와 non-obvious rationale |
| Working / handoff artifact | `inbox/YYYY-MM-DD/` | 작업 과정에서 생성되며 아직 canonical하지 않은 report, review, research, handoff와 generated output |
| Retained historical artifact | `inbox/archive/YYYY-MM-DD/` | 현재 정본은 아니지만 artifact 원문 자체를 다시 참고할 가치가 있는 기록 |
| Repository change history | Git history와 PR | 변경 과정, 완료된 migration, 이전 canonical state와 일반 작업 이력 |

`inbox/`와 archive의 상세 lifecycle은 [`inbox/README.md`](../../inbox/README.md)가 소유합니다.

Durable knowledge를 inbox나 archive에만 남겨 current authority를 숨기지 않습니다. 반대로 단순 과거 상태를 durable documentation으로 승격하거나 archive에 중복 보관하지 않습니다.

Git history는 **어떻게 변경되었는지**를 보존하고, archive는 **비정본 artifact 자체를 계속 찾아볼 가치가 있을 때**만 사용합니다.

## Boundary

이 문서는 각 Skill의 maintainer contract, testing policy, Rulesync integration detail 또는 Agent Skills specification을 소유하지 않습니다. 해당 내용은 각각의 canonical source나 좁은 reference가 소유합니다.
