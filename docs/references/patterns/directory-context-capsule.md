# Directory Context Capsule

하나의 directory를 **agent가 사용하는 context boundary**로 보고, 가까운 entrypoint와 해당 scope의 rules, Skills, references, guidelines 등 agent-facing context를 함께 두는 패턴입니다.

Agent Skill에서 `SKILL.md`가 entrypoint가 되고 주변 파일이 필요한 context를 제공하는 것처럼, 일반 repository directory도 비슷한 구조를 가질 수 있습니다.

이 directory는 source code 영역일 필요가 없습니다. Filesystem 자체가 작업 상태나 운영 surface를 표현하는 FS Kanban 같은 구조에도 적용할 수 있습니다.

## Purpose

특정 directory에서만 필요한 behavior와 knowledge를 repository 전체 지침에 섞지 않고 해당 scope 가까이에 둡니다.

Entrypoint에는 항상 필요한 핵심 guidance와 추가 context로 가는 route를 두고, 세부 자료와 task-specific asset은 필요할 때 선택적으로 읽거나 적용할 수 있게 분리합니다.

## Core

```text
directory scope
      ↓
local entrypoint
      ↓
core guidance + context routing
      ↓
task-relevant local assets/context
```

- Directory가 하나의 책임 또는 context scope를 나타냅니다.
- Entrypoint가 해당 scope의 핵심 guidance와 추가 asset/context 탐색 경로를 제공합니다.
- 세부 context는 entrypoint에 모두 복제하지 않고 필요한 파일로 분리할 수 있습니다.
- Agent는 현재 task와 관련된 local rule, Skill, reference 또는 guidance만 선택적으로 사용할 수 있습니다.

## Entrypoint

Entrypoint mechanism은 repository와 harness에 맞게 선택할 수 있습니다. 문서 파일일 수도 있고, scope에 직접 적용되는 instruction/rule asset일 수도 있습니다.

대표적인 형태:

- nested `AGENTS.md` 같은 directory-scoped instruction asset
- `README.md` 같은 repository-local entry document
- glob/path scoped Rule 자체 또는 Rule이 가리키는 local entry file
- framework 또는 vendor가 제공하는 scoped instruction asset
- routing/index asset이 가리키는 custom entry document

`AGENTS.md`, `README.md` 또는 특정 filename은 필수 규격이 아닙니다. 핵심은 **directory scope에서 안정적으로 발견되거나 route될 수 있는 local entrypoint**입니다.

Entrypoint는 보통 다음에 집중합니다.

- directory의 목적과 책임
- 항상 필요한 핵심 guidance
- 중요한 authority 또는 constraint
- 어떤 상황에서 어떤 local asset이나 context를 더 사용할지에 대한 routing

## Skill-like Shape

대표 예시는 **entrypoint 하나와 context directory 하나**만 두는 단순한 형태입니다.

```text
Agent Skill                       Directory Context Capsule

<skill>/                          <dir>/
├─ SKILL.md                       ├─ AGENTS.md      # example entrypoint
└─ references/                    └─ .configs/      # example context surface
                                     ├─ workflow.md
                                     ├─ conventions.md
                                     └─ examples.md
```

두 구조 모두 entrypoint가 핵심 guidance를 제공하고 주변 context가 task-specific behavior와 knowledge를 보완할 수 있습니다.

`.configs/`는 대표 예시일 뿐입니다. `configs/`, `.agents/`, `agents/`, `context/` 또는 repository에 더 자연스러운 다른 이름을 사용할 수 있습니다. Context 종류마다 별도 directory를 만들 필요도 없습니다.

차이는 activation과 contract입니다. Skill은 Skill runtime의 discovery/activation semantics를 따르지만, Directory Context Capsule은 directory scope, path rule, explicit routing 또는 harness의 native mechanism을 통해 적용될 수 있습니다. Directory에 파일을 두었다는 사실만으로 Skill semantics나 automatic discovery가 생긴다고 가정하지 않습니다.

Context surface 안에는 필요에 따라 scope-local rules, Skill 또는 task-specific instruction, architecture/domain knowledge, guidelines, examples, schemas, templates, 다른 canonical owner로 가는 routing guidance 등을 함께 둘 수 있습니다.

실제 Skill, Rule 또는 vendor-native asset은 해당 asset type과 harness의 contract를 그대로 따릅니다. Capsule은 이들을 함께 배치하고 route하는 boundary이지 새로운 공통 schema가 아닙니다.

## FS Kanban Example

Filesystem directory를 Kanban board처럼 사용하는 경우에도 같은 패턴을 적용할 수 있습니다.

```text
kanban/
├─ AGENTS.md
├─ .configs/
│  ├─ workflow.md
│  ├─ card-conventions.md
│  └─ review.md
└─ ...            # actual Kanban state and work items
```

`AGENTS.md`는 board의 목적, 상태 변경 원칙과 필요한 local context로 가는 route를 제공하고, `.configs/`는 workflow나 card convention처럼 세부 운영 context를 보관할 수 있습니다. 실제 Kanban state와 work item은 같은 directory의 본래 filesystem structure가 소유합니다.

이 예시의 핵심은 Kanban 자체가 아니라 **실제 작업 surface와 그 surface를 다루는 agent context를 같은 directory boundary에 붙이는 것**입니다.

## Discovery and Loading

이 패턴은 특정 discovery mechanism을 전제하지 않습니다.

```text
structural scope / path rule / explicit route
                  ↓
            local entrypoint
                  ↓
      relevant local assets/context
```

Harness가 nested instruction이나 scoped asset discovery를 지원하면 그 native mechanism을 사용할 수 있습니다. 자동 discovery가 없다면 repository entrypoint, routing asset, bootstrap instruction 또는 다른 explicit route가 capsule을 가리킬 수 있습니다.

## Options and Considerations

- 작은 scope는 entrypoint 하나만으로 충분할 수 있습니다.
- 세부 context나 task-specific asset이 늘어날 때 context directory 하나를 추가하는 정도로 시작할 수 있습니다.
- Context 종류가 실제로 독립된 책임과 관리 필요를 가질 때만 더 세분화합니다.
- Entrypoint가 Rule이고 사람이 읽는 설명은 별도 `README.md`가 맡을 수 있습니다.
- `README.md` 하나가 human guide와 agent entrypoint를 함께 맡을 수도 있습니다. 다만 agent-only operational guidance가 커지면 별도 instruction/Rule asset으로 분리하는 편이 더 명확할 수 있습니다.
- 여러 nested capsule은 실제 scope나 책임이 다를 때만 나누는 편이 좋습니다.
- 같은 rule, Skill behavior 또는 knowledge를 root guidance와 local capsule에 중복 소유하지 않습니다.
- 단순 filesystem grouping에 독립적인 context 책임이 없다면 capsule을 만들 필요가 없습니다.
- Local asset이나 context가 여러 scope에서 반복 사용되면 더 적절한 reusable owner로 옮기거나 route할 수 있습니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Layered Context Instructions](layered-context-instructions.md) | Scope에 따라 어떤 instruction mechanism을 사용할지 다룹니다. 이 패턴은 선택된 directory scope 안의 entrypoint와 context bundle을 다룹니다. |
| [Progressive Context Routing](progressive-context-routing.md) | 필요한 context를 점진적으로 로드하는 shape를 다룹니다. Directory Context Capsule은 그 local destination이 될 수 있습니다. |
| [Nonstandard Directory Guide](nonstandard-directory-guide.md) | 비표준 directory를 설명 가능한 상태로 유지하는 human-facing guide를 다룹니다. 이 패턴은 agent가 실제 작업에 사용할 guidance와 context bundle까지 다룹니다. |
| [Skill Source Workspace](skill-source-workspace.md) | 실제 Agent Skill package를 다룹니다. 이 패턴은 일반 repository directory에 Skill-like entrypoint/context structure를 적용합니다. |

## Boundary

이 패턴은 **directory-local entrypoint와 주변 agent-facing assets/context를 하나의 scope-local capsule로 구성하는 방식**을 설명합니다.

특정 directory 이름, entrypoint filename, subdirectory layout, discovery mechanism 또는 Agent Skill packaging을 강제하지 않습니다. 또한 local entrypoint가 harness의 instruction precedence, permission, Skill discovery 또는 scope semantics를 새로 정의한다고 가정하지 않습니다.
