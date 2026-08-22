# Asset Configuration Surface

재사용 가능한 asset의 core와 project, repository 또는 scope별 customization을 분리해 관리하는 패턴입니다.

`.configs/`, `.configs/<asset-name>.md`, `.configs/<asset-name>/*`, `**/.configs/` 같은 이름과 경로는 모두 **representative examples**입니다. 핵심은 특정 filesystem convention이 아니라 **reusable core와 customization delta의 분리**입니다.

## Purpose

Base asset을 직접 복제하거나 수정하지 않고 환경별 변형을 작은 delta로 관리하면 reusable core를 유지하면서 local tuning을 적용하기 쉽습니다.

여기서 configuration은 option file만 뜻하지 않습니다. Asset의 extension point를 표현한다면 추가 instruction, template, schema, metadata, path mapping 같은 customization material도 포함할 수 있습니다.

## Core

- Reusable core와 환경별 customization을 분리합니다.
- 가능한 한 base asset 전체보다 필요한 delta만 표현합니다.
- 적용 대상과 scope를 식별할 수 있게 두면 여러 asset과 scope를 함께 관리하기 쉽습니다.
- 여러 source가 겹칠 때는 필요에 따라 precedence나 merge semantics를 설명합니다.
- Asset이 기대하는 configuration과 extension point가 드러나면 재사용과 이동이 쉬워집니다.

## Typical Forms

아래 layout은 예시이며 서로 배타적이지 않습니다. Repository나 tool에 맞는 이름, 위치, format 또는 manifest를 사용할 수 있습니다.

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

Asset이나 특정 scope와 customization의 결합이 강할 때 가까이 둘 수 있습니다.

### Scoped

```text
**/
└─ .configs/
   └─ ...
```

Directory, package, domain 등 scope별 customization이 필요할 때 nested surface를 사용할 수 있습니다.

## Typical Content

- runtime 또는 generation options
- 추가 instruction이나 constraint
- custom template
- schema와 validation information
- path, routing 또는 source mapping
- metadata와 defaults
- tool-specific adapter configuration

필요한 extension point만 선택합니다.

## Recommended Default

특별한 이유가 없다면 다음처럼 단순하게 시작할 수 있습니다.

- Base asset에는 reusable core와 extension point를 둡니다.
- Configuration surface에는 project-local 또는 scope-local delta를 집중시킵니다.
- 작은 customization은 단일 파일로 시작하고, 독립적인 책임이 생기면 bundle로 확장합니다.
- 여러 layer가 실제로 겹칠 때만 precedence나 merge rule을 추가합니다.

Asset이나 harness가 더 자연스러운 extension mechanism을 제공한다면 그 방식을 사용할 수 있습니다.

## Resolution

여러 configuration source가 겹치면 다음과 같은 계층을 둘 수 있습니다.

```text
asset defaults
    ↓
repository config
    ↓
scoped config
    ↓
explicit invocation config
```

이 순서는 예시일 뿐이며 특정 precedence를 뜻하지 않습니다. Override, merge, append 같은 의미도 configuration 종류에 따라 달라질 수 있습니다.

## Considerations

- Configuration surface가 miscellaneous storage가 되면 asset boundary와 ownership이 흐려질 수 있습니다.
- 큰 instruction이나 template을 반복하기보다 reusable owner와 필요한 delta를 분리하는 편이 관리하기 쉬운 경우가 많습니다.
- Structured configuration이 중요하면 schema나 validation을 함께 둘 수 있습니다.
- 필요한 configuration만 resolve하거나 load하면 context 효율을 높일 수 있습니다.
- Zero-config asset도, project-specific parameter가 필요한 asset도 가능합니다. Configuration requirement가 숨겨진 관행보다 이해 가능한 extension point로 드러나는 것이 중요합니다.

## Boundary

이 패턴은 **asset의 reusable core와 customization surface를 분리하는 설계**를 설명합니다.

Template/schema 설계, context injection mechanism, configuration format이나 directory 이름은 정의하지 않습니다. Configuration이 routing behavior를 조정할 수는 있지만 routing/index architecture 자체는 별도의 관심사로 볼 수 있습니다.

`.configs/`와 관련 예시는 filesystem convention의 한 형태일 뿐이며 필수 규격이나 경로가 아닙니다.
