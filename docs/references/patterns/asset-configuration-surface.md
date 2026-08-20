# Asset Configuration Surface

재사용 가능한 asset의 core를 직접 수정하지 않고 project, repository 또는 scope별 customization을 별도 surface에서 제공하는 패턴입니다.

`.configs/`, `.configs/<asset-name>.md`, `.configs/<asset-name>/*`, `**/.configs/` 같은 이름과 경로는 모두 **representative examples**입니다. 이 패턴의 핵심은 특정 filesystem convention이 아니라 **reusable core와 customization delta의 분리**입니다.

## Purpose

Asset의 기본 source와 환경별 customization을 분리해 재사용성과 local tuning을 함께 유지합니다.

Base asset은 독립적으로 유효한 기본 동작을 제공하고, configuration surface는 필요한 환경에서 이를 보완하거나 조정합니다.

## Core

- Asset의 reusable core와 local customization을 분리합니다.
- Configuration은 base asset을 복제하지 않고 필요한 delta를 표현합니다.
- Configuration surface에는 설정뿐 아니라 asset customization에 필요한 instruction, template, schema, metadata, path mapping 등을 둘 수 있습니다.
- Configuration의 적용 대상과 scope는 식별 가능해야 합니다.
- 여러 configuration layer가 동시에 적용될 수 있다면 resolution과 precedence가 모호하지 않아야 합니다.

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

Configuration surface는 필요에 따라 다음을 포함할 수 있습니다.

- runtime 또는 generation options
- 추가 instruction이나 constraint
- custom template
- schema와 validation contract
- path, routing 또는 source mapping
- metadata와 defaults
- tool-specific adapter configuration

모든 종류를 지원할 필요는 없습니다. Asset이 실제로 제공하는 extension point만 사용합니다.

## Resolution

Configuration source가 하나뿐이라면 별도 resolution model이 필요하지 않을 수 있습니다.

여러 source가 겹친다면 적용 순서와 merge semantics를 명확히 합니다. 예를 들면 다음과 같은 계층을 사용할 수 있습니다.

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

- Configuration surface가 asset 본체의 필수 정보를 빼내는 장소가 되어서는 안 됩니다. Configuration 없이도 base asset의 기본 의미와 동작을 이해할 수 있어야 합니다.
- Configuration directory를 miscellaneous storage처럼 사용하지 않습니다. 들어가는 내용은 특정 asset의 customization과 직접 관련되어야 합니다.
- 큰 instruction이나 template을 여러 configuration에 복제하기보다 reusable owner를 두고 필요한 delta만 표현하는 편이 좋습니다.
- Structured configuration이 중요하면 schema나 validation을 함께 둘 수 있습니다.
- 모든 configuration을 항상 context에 주입할 필요는 없습니다. 적용 대상과 task에 필요한 configuration만 resolve하거나 load할 수 있습니다.

## Boundary

이 패턴은 **asset에 customization extension point를 제공하고 그 customization을 별도 surface에 배치하는 방식**을 다룹니다.

Asset 자체의 template/schema 설계 방법, context injection mechanism, configuration file format이나 특정 directory 이름은 정의하지 않습니다.

`.configs/`와 관련 예시는 filesystem convention의 한 형태일 뿐이며 이 패턴의 normative contract가 아닙니다.
