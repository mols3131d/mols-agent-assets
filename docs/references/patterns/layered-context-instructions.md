# Layered Context Instructions

지침과 context를 적용 범위에 따라 다른 mechanism으로 배치해 **자동 주입을 유지하면서 불필요한 context load를 줄이는** 패턴입니다.

## Layers

| Scope | Mechanism |
| --- | --- |
| repository 전체 기본 지침 | root `AGENTS.md` |
| 특정 directory subtree | nested `AGENTS.md` |
| 확장자, glob, 반복되는 path pattern | glob-scoped Rule |
| task 의미를 판단해야 선택 가능한 context, rule, knowledge | load-context Skill |

## Pattern

- Repository 전체에 항상 필요한 지침은 root `AGENTS.md`에 둡니다.
- 특정 subtree에만 필요한 지침은 nested `AGENTS.md`로 좁힙니다.
- 디렉터리 hierarchy와 맞지 않는 확장자별·반복 path별 지침은 glob Rule로 적용합니다.
- 현재 task의 intent를 모델이 판단해야 선택할 수 있는 context, rule, knowledge는 Skill로 구성합니다.
- 같은 지침을 여러 layer에 복제하기보다 가장 자연스럽고 좁은 scope가 소유하게 합니다.

## Principle

구조적으로 적용 대상을 결정할 수 있으면 path-based mechanism을 우선하고, **semantic relevance를 판단해야 할 때 Skill을 사용**합니다.

```text
structural scope
├─ repository      → AGENTS.md
├─ directory tree  → nested AGENTS.md
└─ path / glob     → Rule

semantic scope
└─ task intent     → Skill
```

## Boundary

- 모든 지침을 root `AGENTS.md`에 집중시키지 않습니다.
- 반대로 구조적으로 자동 적용할 수 있는 지침을 불필요하게 Skill로 만들지 않습니다.
- Layer는 context routing 책임을 나누기 위한 것이며 같은 규칙의 중복 소유를 위한 것이 아닙니다.
