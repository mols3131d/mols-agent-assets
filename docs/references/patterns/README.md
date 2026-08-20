# Patterns

이 디렉터리는 여러 repository와 harness에서 참고·선택·조합·변형할 수 있는 **reusable pattern capsule**을 보관합니다.

각 pattern 문서는 특정 project의 operational policy가 아니라, 반복해서 사용할 수 있는 설계 아이디어의 본질과 적용 선택지를 독립적으로 설명합니다.

## Capsule Contract

Pattern은 기본적으로 하나의 `*.md` 문서로 시작할 수 있으며, 내용이나 책임이 커지면 **directory bundle**로 구성할 수 있습니다.

```text
patterns/
├─ simple-pattern.md
└─ large-pattern/
   ├─ README.md
   └─ ...
```

파일이든 bundle이든 하나의 pattern은 **독립적으로 읽고 재사용할 수 있는 self-contained capsule**입니다.

- 각 capsule은 자기 pattern의 목적, 본질, 적용 방식, 선택지와 경계를 충분히 설명합니다.
- Bundle은 하나의 pattern capsule을 여러 파일로 나눈 형태이며, `README.md` 같은 entrypoint에서 전체 의미와 내부 읽기 경로를 복원할 수 있게 합니다.
- 다른 capsule을 반드시 읽어야만 핵심 의미를 이해할 수 있는 hidden dependency를 만들지 않습니다.
- 다른 pattern과 내용이 겹치는 것은 self-containment와 재사용성에 도움이 되면 허용합니다.
- 중복 자체보다 **어떤 capsule이 그 책임을 소유하는가**를 우선 봅니다.
- 다른 pattern의 책임이나 특정 project의 operational policy를 대신 소유하지 않습니다.

관련 pattern을 링크하거나 함께 설명할 수 있지만, 링크가 capsule의 독립성을 대체하지는 않습니다.

## Flexibility

Pattern은 **본질은 분명하게, 적용은 유연하게** 작성합니다.

- Pattern으로 성립하기 위한 최소 core와 invariant는 명확하게 둡니다.
- 파일명, directory layout, format, tool, workflow 같은 구현 방식은 본질이 아닌 한 고정하지 않습니다.
- 대표적인 구현은 recommendation, typical form, example 또는 option으로 제시합니다.
- 대안이 의미 있으면 함께 제시하고, 규모나 환경에 따른 extension도 열어둡니다.
- 작은 repository에서는 단순화하고, 복잡한 repository에서는 확장할 수 있어야 합니다.
- 특정 harness나 tool의 지원 차이가 있으면 같은 목적을 만족하는 다른 mechanism으로 조정할 수 있습니다.

예시는 pattern을 이해하기 위한 reference이지 모든 repository에 적용되는 universal requirement가 아닙니다.

## Structure

문서 구조는 고정 schema가 아닙니다. 필요에 따라 다음 책임을 사용할 수 있습니다.

- `Purpose` — 해결하려는 문제와 존재 이유
- `Core` — pattern을 성립시키는 최소 본질
- `Typical Forms` / `Typical Options` — 자주 쓰는 구현과 권장 선택지
- `Options` — 대안이나 조합 가능한 선택지
- `Extensions` — 규모·자동화·도구에 따른 확장 방법
- `Considerations` — trade-off와 적용 시 판단할 점
- `Boundary` — 이 pattern이 소유하지 않는 책임

Pattern에 필요하지 않은 section을 형식 때문에 추가하지 않습니다.

Bundle로 확장할 때도 section을 기계적으로 파일로 분리하지 않습니다. 독립적인 책임이나 유지보수 이유가 생길 때만 파일을 나누고, bundle 전체는 하나의 pattern capsule로 유지합니다.

## Ownership

각 capsule은 자기 책임을 충분히 소유하되 그 경계를 넘지 않습니다.

- 다른 capsule과 같은 내용을 설명해도 괜찮습니다.
- 다른 capsule의 핵심 책임을 자기 규칙처럼 정의하면 ownership 문제입니다.
- Project-local convention이나 mandatory workflow는 해당 project의 operational documentation이 소유합니다.
- 외부 standard나 tool behavior가 authority라면 필요에 따라 reference하고 local pattern이 이를 재정의하지 않습니다.
- 같은 capsule 또는 bundle 내부에서는 의미 없는 반복을 피합니다.

## Review

Pattern을 작성하거나 수정할 때 다음을 우선 확인합니다.

1. 이 capsule 하나만으로 pattern의 목적과 본질을 이해할 수 있는가?
2. Core와 example/recommendation/option이 구분되어 있는가?
3. 특정 repository에 불필요하게 맞춰져 있지 않은가?
4. 다른 pattern이나 project policy가 소유해야 할 책임을 가져오지 않았는가?
5. 필요한 대안과 확장 가능성을 닫아버리지 않았는가?
6. 다른 capsule과의 overlap을 없애려다 self-containment를 훼손하지 않았는가?
7. Bundle이라면 파일 분할이 실제 책임 경계를 반영하고, entrypoint만으로 전체 구조를 탐색할 수 있는가?

이 README는 pattern 목록이나 index를 소유하지 않습니다. 이 디렉터리의 공통 contract만 소유합니다.

이 디렉터리의 목표는 완전한 규격집을 만드는 것이 아니라, **독립적으로 재사용할 수 있고 필요에 따라 변형 가능한 pattern vocabulary**를 축적하는 것입니다.
