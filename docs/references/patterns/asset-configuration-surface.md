# Asset Configuration Surface

재사용 가능한 asset의 core와 project, repository 또는 scope별 customization을 분리해 관리하는 패턴입니다.

`.configs/`, `.configs/<asset-name>.md`, `.configs/<asset-name>/*`, `**/.configs/` 같은 이름과 경로는 모두 **representative examples**입니다. 이 패턴의 핵심은 특정 filesystem convention이 아니라 **reusable core와 customization delta의 분리**입니다.

## Purpose

Asset의 기본 source와 환경별 customization을 분리하면 reusable core를 유지하면서도 project-local tuning, 추가 지침, 경로 조정, template 교체 같은 변형을 비교적 작은 delta로 관리할 수 있습니다.

Configuration surface는 단순한 option file에 한정되지 않습니다. Asset의 extension point를 표현하는 별도 surface라면 instruction, template, schema, metadata, path mapping 등도 함께 둘 수 있습니다.

## Core

- Reusable core와 환경별 customization을 분리합니다.
- Configuration은 가능한 한 base asset 전체를 복제하기보다 필요한 delta를 표현합니다.
- Configuration의 적용 대상과 scope를 식별할 수 있게 두면 여러 asset이나 여러 scope를 함께 관리하기 쉽습니다.
- 여러 configuration source가 겹치는 환경에서는 precedence나 merge semantics를 명확히 해두는 편이 좋습니다.
- Asset 자체는 어떤 configuration을 기대하는지, 어떤 extension point를 제공하는지 이해할 수 있게 두는 것이 일반적으로 재사용에 유리합니다.

## Typical Forms

아래 layout은 대표적인 예시이며 필수 구조가 아닙니다. Repository나 tool의 convention에 따라 다른 이름, 위치, format 또는 manifest를 사용할 수 있습니다.

### Centralized

```text
.configs/
├─ <asset-name>/
│  ├─ config.yaml
│  ├─ instructions.md
│  ├─ template.md
│  └─ schema.json
└─ <asset-name>.md
```

여러 asset의 customization을 repository-level surface에서 관리할 수 있습니다.

### Co-located

```text
<asset>/
├─ ...
└─ .configs/
   ├─ instructions.md
   ├─ template.md
   └─ schema.json
```

Asset 또는 특정 scope와 configuration의 결합이 강할 때 가까이 둘 수 있습니다.

### Scoped

```text
**/
└─ .configs/
   └─ ...
```

같은 asset이라도 directory, package, domain 등 scope별 customization이 필요할 때 nested configuration surface를 사용할 수 있습니다.

## Configuration Content

Configuration surface는 필요에 따라 다음과 같은 내용을 포함할 수 있습니다.

- runtime 또는 generation options
- 추가 instruction이나 constraint
- custom template
- schema와 validation information
- path, routing 또는 source mapping
- metadata와 defaults
- tool-specific adapter configuration

모든 종류를 지원할 필요는 없습니다. Asset이 실제로 제공하는 extension point와 유지보수 필요에 맞춰 선택합니다.

## Recommended Default

특별한 이유가 없다면 다음처럼 시작하는 구성이 단순합니다.

- Base asset에는 reusable core와 extension point를 둡니다.
- Configuration surface에는 project-local 또는 scope-local delta를 집중시킵니다.
- 작은 customization은 단일 파일로 시작하고, 독립적인 책임이 늘어나면 directory bundle로 확장합니다.
- 여러 layer가 겹치기 시작할 때만 precedence나 merge rule을 추가합니다.

이 방식은 대표적인 시작점일 뿐이며 asset의 성격이나 harness가 더 적합한 구성을 제공하면 그 방식을 따를 수 있습니다.

## Resolution

Configuration source가 하나뿐이라면 별도 resolution model이 필요하지 않을 수 있습니다.

여러 source가 겹친다면 적용 순서와 merge semantics를 명확히 할 수 있습니다. 예를 들면 다음과 같은 계층을 사용할 수 있습니다.

```text
asset defaults
    ↓
repository config
    ↓
scoped config
    ↓
explicit invocation config
```

이 순서는 예시일 뿐이며 pattern 자체가 특정 precedence를 강제하지 않습니다. Override, merge, append 같은 의미도 configuration 종류에 따라 달라질 수 있습니다.

## Considerations

- Configuration surface가 miscellaneous storage가 되면 asset boundary와 ownership이 흐려질 수 있습니다.
- 큰 instruction이나 template을 여러 configuration에 복제하기보다 reusable owner를 두고 필요한 delta만 표현하는 편이 관리하기 쉬운 경우가 많습니다.
- Structured configuration이 중요하면 schema나 validation을 함께 두는 선택지가 있습니다.
- 모든 configuration을 항상 context에 주입할 필요는 없습니다. 적용 대상과 현재 task에 필요한 configuration만 resolve하거나 load하는 구성이 context 효율에 도움이 될 수 있습니다.
- 일부 asset은 zero-config default를 제공할 수 있고, 일부는 project-specific parameter를 필수로 요구할 수 있습니다. 중요한 것은 configuration requirement가 숨겨진 관행이 아니라 이해 가능한 extension point로 드러나는 것입니다.

## Boundary

이 패턴은 **asset의 reusable core와 customization surface를 분리하는 설계**를 설명합니다.

Asset 자체의 template/schema 설계 방법, context injection mechanism, configuration file format이나 특정 directory 이름은 정의하지 않습니다. Configuration에서 routing behavior를 조정할 수는 있지만 routing/index architecture 자체는 별도의 관심사로 볼 수 있습니다.

`.configs/`와 관련 예시는 filesystem convention의 한 형태일 뿐이며 이 패턴의 normative contract가 아닙니다.
