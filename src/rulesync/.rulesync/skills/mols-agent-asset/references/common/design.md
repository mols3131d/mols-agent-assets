# Common Design

Skill, Rule, Subagent에 공통으로 적용되는 설계 판단을 다룬다. 자산 유형 고유의 판단은 각 유형의 `design.md`가 소유한다.

## Responsibility

파일이나 형식보다 먼저 책임을 정한다. Representation과 semantic responsibility를 같은 것으로 취급하지 않는다.

- Skill, Rule, Subagent라는 형식은 책임을 자동으로 결정하지 않는다. 자산이 주로 무엇을 소유하고 어떤 이유로 변경되는지로 책임을 본다.
- 이미 책임을 소유한 자산이 있으면 경쟁 owner를 만들기보다 기존 owner 확장을 우선한다.
- 새 책임이나 큰 변경은 실제 사용 사례로 추상화가 맞는지 확인한다.
- 인접 자산과 혼동하기 쉬우면 대표적인 non-use 또는 near-miss도 함께 본다.
- 관련 권한과 주변 자산을 확인한 뒤에도 owner나 자산 유형이 모호하면 추측으로 새 owner를 만들지 않는다.

## Scope and placement

적용 여부를 가장 자연스럽게 결정할 수 있는 mechanism을 선택한다.

- repository, directory, path, glob처럼 구조만으로 적용 대상을 결정할 수 있으면 structural scope를 우선한다.
- task intent나 의미적 관련성을 봐야 적용할 수 있으면 semantic routing이 가능한 자산을 사용한다.
- 별도 실행 단위의 specialization, isolation, capability, coordination이 필요할 때만 agent delegation을 고려한다.
- 이미 존재하는 native scope, entrypoint, configuration 또는 routing mechanism으로 충분하면 새 layer를 만들지 않는다.

항상 적용되어야 하는 authority나 safety boundary를 optional routing 뒤에 숨기지 않는다.

## Granularity

새 파일이나 context surface에는 ownership, discovery, routing, resolution, synchronization 비용이 생긴다. 내용이 길거나 주제가 다르다는 이유만으로 분리하지 않는다.

다음 중 하나 이상이 실질적으로 독립적일 때 분리를 고려한다.

- applicability가 다르다.
- 필요한 loading 시점이나 context가 다르다.
- 다른 owner나 workflow에서 독립적으로 재사용된다.
- 변경 이유와 관리 owner가 다르다.

거의 항상 함께 적용되고 같은 이유로 바뀌며 독립적인 선택 가치가 없다면 함께 두는 편을 우선한다. 반대로 불필요한 context가 반복적으로 같이 로드되거나 독립적인 reuse가 명확하면 그때 분리한다.

Filesystem의 이름과 배치는 orientation과 navigation을 도울 수 있게 하되, 구조를 설명적으로 보이게 만들기 위해 framework convention, cohesion, operability 또는 올바른 ownership을 왜곡하지 않는다.

## Reusable core and delta

공통 behavior와 project, repository, scope 또는 target별 customization을 구분한다.

- reusable core 전체를 복제하기보다 필요한 local delta만 표현한다.
- customization이 적용되는 scope와 owner를 식별할 수 있게 한다.
- 여러 customization source가 실제로 겹칠 때만 precedence나 merge semantics를 추가한다.
- target별 차이가 작은데 전체 자산을 fork하지 않는다.
- customization surface를 miscellaneous storage로 만들지 않는다.

Caller가 실제로 제어할 가치가 있는 변형만 argument나 option으로 노출한다. `default`, `auto`, explicit value가 있다면 각 의미와 omission behavior를 구분하고, argument 하나가 사실상 별도 capability나 permission boundary를 만든다면 parameterization보다 책임 분리를 우선한다.

## Authority

결정별 권한을 구분한다.

1. 사용자와 프로젝트 지침은 요청 결과와 허용 범위를 소유한다.
1. source framework는 canonical representation을 소유한다.
1. target runtime은 target-specific behavior를 소유한다.
1. repository convention은 local delta를 소유한다.
1. 개별 자산은 위 권한보다 좁은 자체 요구사항을 소유할 수 있다.

빠르게 변하는 vendor field, path, discovery, packaging, permission, runtime semantics를 범용 규칙으로 복제하지 않는다. 결과에 영향을 주는 경우 현재 authoritative source를 확인한다.

## Precision

실패 비용과 변동성에 비례해 제약의 강도를 정한다.

- 여러 접근이 유효하면 outcome, constraint, heuristic 중심으로 둔다.
- 일관성이 중요하면 선호 구조를 명시한다.
- 순서, 재현성, 안전성이 취약하면 deterministic mechanics나 좁은 절차를 사용한다.
- 일반적인 모델 지식을 포괄성을 위해 반복하지 않는다.
- 서로 다른 자산을 겉으로 통일하기 위한 추상화 계층을 만들지 않는다.

## Boundary

변경 전에 write boundary를 정한다. 권한, dependency, 예시를 읽었다고 쓰기 권한까지 생기지 않는다.

- unrelated asset을 함께 정규화하지 않는다.
- generated/projection은 해당 계약이 명시적으로 다르게 정하지 않는 한 파생 결과로 취급한다.
- 외부 자산을 재사용하면 필요한 attribution, license, upstream revision을 보존한다.
