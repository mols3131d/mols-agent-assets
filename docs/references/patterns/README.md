# Patterns

이 디렉터리는 여러 repository와 harness에서 참고·선택·조합·변형할 수 있는 **reusable pattern capsule**을 보관합니다.

Pattern은 특정 project의 operational policy가 아니라, 반복해서 사용할 수 있는 설계 아이디어의 **본질과 적용 선택지**를 설명합니다.

## Capsule

하나의 pattern은 하나의 **self-contained capsule**입니다.

- 다른 capsule 없이도 pattern의 목적, core, 주요 선택지와 경계를 이해할 수 있어야 합니다.
- Self-contained는 isolated를 뜻하지 않습니다. 다른 capsule이 소유하는 인접 책임은 필요에 따라 reference해 함께 조합할 수 있습니다.
- Cross-link는 core 설명을 대신하는 의존성이 아니라, 관련 pattern을 다시 복제하지 않고 확장·적용할 수 있게 연결하는 수단입니다.

## Shape

Pattern은 보통 하나의 `*.md`로 시작하고, 커지면 **directory bundle**로 확장할 수 있습니다.

```text
patterns/
├─ simple-pattern.md
└─ large-pattern/
   ├─ README.md
   └─ ...
```

Bundle은 여러 파일로 나뉘어도 하나의 pattern capsule입니다. `README.md` 같은 entrypoint에서 bundle의 의미와 내부 탐색 경로를 파악할 수 있게 합니다.

단순히 문서가 길거나 section이 많다는 이유로 분할하지 않습니다. 독립적인 책임이나 유지보수 필요가 생길 때 bundle을 고려합니다.

## Writing

Pattern은 **본질은 분명하게, 적용은 유연하게** 작성합니다.

- Pattern을 성립시키는 core와 invariant는 명확하게 둡니다.
- 본질이 아닌 layout, filename, format, tool, workflow는 고정 규칙으로 만들지 않습니다.
- Directory나 filename은 명시적으로 contract라고 정의하지 않는 한 예시로 해석합니다. 강한 표현이 필요해도 보통 recommendation 또는 default 수준으로 둡니다.
- 대표 구현은 recommendation, typical form, example, option처럼 성격을 구분해 제시합니다.
- 의미 있는 대안과 규모·환경에 따른 extension을 열어둡니다.
- 작은 repository에서는 단순화하고, 필요한 경우 더 복잡한 구성으로 확장할 수 있어야 합니다.

문서 구조는 고정 schema가 아닙니다. 필요하면 `Purpose`, `Core`, `Typical Forms`, `Options`, `Extensions`, `Considerations`, `Boundary` 같은 책임을 사용할 수 있으며, 필요 없는 section은 형식 때문에 추가하지 않습니다.

## Ownership

각 capsule은 자기 pattern을 충분히 설명하되 그 경계를 넘지 않습니다.

- 다른 capsule과 내용이 겹치는 것은 self-containment와 재사용성에 도움이 되면 허용합니다.
- 중복 자체보다 **각 capsule이 어떤 책임을 소유하는지**를 우선 봅니다.
- 다른 pattern의 핵심 책임을 자기 규칙처럼 소유하지 않습니다. 인접 pattern의 책임이 적용에 유용하면 해당 capsule을 reference할 수 있습니다.
- Project-local convention과 mandatory workflow는 해당 project의 operational documentation이 소유합니다.
- 외부 standard나 tool behavior가 authority라면 필요에 따라 reference하고 pattern이 이를 재정의하지 않습니다.
- 같은 capsule이나 bundle 내부의 의미 없는 반복은 피합니다.

## Review

Pattern을 작성하거나 수정할 때 다음을 확인합니다.

1. 이 capsule만으로 pattern의 목적과 본질을 이해할 수 있는가?
1. Core와 recommendation / option / example이 구분되어 있는가?
1. 특정 repository나 tool에 불필요하게 고정되어 있지 않은가?
1. 다른 pattern이나 project policy가 소유해야 할 책임을 가져오지 않았는가?
1. 다른 capsule이 소유하는 인접 책임을 복제하기보다 필요에 따라 연결했는가?
1. 필요한 대안과 확장 가능성을 닫아버리지 않았는가?
1. Bundle이라면 entrypoint에서 전체 의미와 내부 구조를 탐색할 수 있는가?

이 README는 pattern 목록이나 index를 소유하지 않습니다. **이 디렉터리의 공통 작성·검토 contract만 소유합니다.**
