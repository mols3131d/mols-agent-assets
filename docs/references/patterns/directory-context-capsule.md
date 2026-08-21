# Directory Context Capsule

하나의 directory를 **agent가 사용하는 context boundary**로 보고, 가까운 entrypoint와 해당 scope의 agent-facing context를 함께 두는 패턴입니다.

Agent Skill에서 `SKILL.md`가 entrypoint가 되고 주변 context가 필요한 정보와 동작을 보완하는 것처럼, 일반 repository directory도 비슷한 구조를 가질 수 있습니다. 다만 이 패턴이 directory에 Skill discovery나 packaging semantics를 부여하지는 않습니다.

이 directory는 source code 영역일 필요가 없습니다. Filesystem 자체가 작업 상태나 운영 surface를 표현하는 FS Kanban 같은 구조에도 적용할 수 있습니다.

## Purpose

특정 directory에서만 필요한 behavior와 knowledge를 repository 전체 지침에 섞지 않고 해당 scope 가까이에 둡니다.

Entrypoint에는 항상 필요한 핵심 guidance와 추가 context로 가는 route를 두고, 세부 문서와 task-specific asset은 필요할 때 선택적으로 읽거나 적용할 수 있게 분리합니다.

## Core

```text
directory scope
      ↓
local entrypoint
      ↓
core guidance + routing
      ↓
task-relevant local context
```

- Directory가 하나의 책임 또는 context scope를 나타냅니다.
- Entrypoint가 해당 scope의 핵심 guidance와 추가 context 탐색 경로를 제공합니다.
- 세부 context는 entrypoint에 모두 복제하지 않고 가까운 context surface에 둘 수 있습니다.
- Agent는 현재 task와 관련된 local rule, Skill, reference, guideline 같은 context만 선택적으로 사용할 수 있습니다.

## Entrypoint

Entrypoint mechanism은 repository와 harness에 맞게 선택할 수 있습니다. 문서 파일일 수도 있고 scope에 직접 적용되는 instruction/rule asset일 수도 있습니다.

대표적인 형태:

- nested `AGENTS.md` 같은 directory-scoped instruction asset
- `README.md` 같은 repository-local entry document
- glob/path scoped Rule 자체 또는 Rule이 가리키는 local entry file
- framework 또는 vendor가 제공하는 scoped instruction asset
- routing/index asset이 가리키는 custom entry document

Entrypoint는 보통 directory의 목적과 책임, 항상 필요한 guidance, 중요한 authority/constraint, 추가 context로 가는 routing에 집중합니다.

`AGENTS.md`, `README.md` 또는 특정 filename은 필수 규격이 아닙니다. 핵심은 **directory scope에서 안정적으로 발견되거나 route될 수 있는 local entrypoint**입니다.

## Representative Shape

대표 예시는 **entrypoint 하나와 context directory 하나**만 두는 단순한 형태입니다.

```text
<dir>/
├─ AGENTS.md
└─ .configs/
   ├─ lifecycle.md
   ├─ review.skill.md
   └─ references/
      └─ terminology.md
```

`.configs/`는 대표 예시일 뿐입니다. `configs/`, `.agents/`, `agents/`, `context/` 또는 repository에 더 자연스러운 다른 이름을 사용할 수 있습니다. Context 종류마다 별도 directory를 만들 필요는 없고, 실제 책임이 나뉠 때는 context surface 아래에 하위 directory를 둘 수도 있습니다.

파일명도 예시 convention을 둘 수 있습니다.

```text
<name>.md                 # ordinary context/document
<name>.<asset-type>.md    # agent asset
```

예를 들어 `lifecycle.md`, `terminology.md`는 일반 context 문서로, `review.skill.md`, `routing.rule.md`는 agent-facing asset으로 구분할 수 있습니다. 이 suffix convention은 사람이 빠르게 구분하기 위한 대표 예시이며 실제 filename이나 asset type contract를 정의하지 않습니다.

Context surface에는 scope-local rules, Skill 또는 task-specific instruction, architecture/domain knowledge, guidelines, examples, schemas, templates, 다른 canonical owner로 가는 routing guidance 등을 필요에 따라 함께 둘 수 있습니다.

실제 Skill, Rule 또는 vendor-native asset은 해당 asset type과 harness의 contract를 그대로 따릅니다. Capsule은 이들을 함께 배치하고 route하는 boundary이지 새로운 공통 schema가 아닙니다.

## FS Kanban Example

Filesystem directory를 Kanban board처럼 사용하는 경우에도 같은 패턴을 적용할 수 있습니다.

```text
kanban/
├─ AGENTS.md
├─ backlog/
├─ archive/
└─ .configs/
   ├─ lifecycle.md
   ├─ card-conventions.md
   ├─ move-card.skill.md
   ├─ review.rule.md
   └─ references/
      └─ status-model.md
```

`backlog/`, `archive/` 같은 directory는 Kanban 자체의 filesystem state를 표현합니다. `AGENTS.md`는 board의 목적과 상태 변경 원칙, 필요한 local context로 가는 route를 제공하고, `.configs/`는 그 board를 다루기 위한 문서와 agent-facing asset을 함께 보관합니다.

이 예시의 `AGENTS.md`, `.configs/`, `*.skill.md`, `*.rule.md`, `references/`와 내부 layout은 모두 대표 예시입니다. 핵심은 **실제 작업 surface와 그 surface를 다루는 local agent context를 같은 directory boundary에 붙이는 것**입니다.

## Discovery and Loading

이 패턴은 특정 discovery mechanism을 전제하지 않습니다.

```text
structural scope / path rule / explicit route
                  ↓
            local entrypoint
                  ↓
           relevant context
```

Harness가 nested instruction이나 scoped asset discovery를 지원하면 그 native mechanism을 사용할 수 있습니다. 자동 discovery가 없다면 repository entrypoint, routing asset, bootstrap instruction 또는 다른 explicit route가 capsule을 가리킬 수 있습니다.

Directory에 asset이 존재한다는 사실만으로 automatic discovery, Skill activation 또는 instruction precedence가 생긴다고 가정하지 않습니다.

## Options and Considerations

- 작은 scope는 entrypoint 하나만으로 충분할 수 있습니다.
- 세부 context나 task-specific asset이 늘어날 때 context directory 하나를 추가하는 정도로 시작할 수 있습니다.
- Context 종류가 실제로 독립된 책임과 관리 필요를 가질 때만 더 세분화합니다.
- Entrypoint가 Rule이고 사람이 읽는 설명은 별도 `README.md`가 맡을 수 있습니다.
- `README.md` 하나가 human guide와 agent entrypoint를 함께 맡을 수도 있습니다. Agent-only operational guidance가 커지면 별도 instruction/Rule asset으로 분리할 수 있습니다.
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
| [Artifact Inbox](artifact-inbox.md) | `inbox/` 같은 working surface가 자체 local agent guidance/context를 가질 때 함께 사용할 수 있습니다. |
| [Skill Source Workspace](skill-source-workspace.md) | 실제 Agent Skill package를 다룹니다. 이 패턴은 일반 repository directory에 Skill-like entrypoint/context structure를 적용합니다. |

## Boundary

이 패턴은 **directory-local entrypoint와 주변 agent-facing context를 하나의 scope-local capsule로 구성하는 방식**을 설명합니다.

특정 directory 이름, entrypoint filename, subdirectory layout, filename suffix, discovery mechanism 또는 Agent Skill packaging을 강제하지 않습니다. 또한 local entrypoint가 harness의 instruction precedence, permission, Skill discovery 또는 scope semantics를 새로 정의한다고 가정하지 않습니다.
