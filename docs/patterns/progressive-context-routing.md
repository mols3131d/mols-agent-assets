# Progressive Context Routing

후보를 한 번에 확정하거나 모든 context를 처음부터 읽기보다, **얕은 discovery에서 더 구체적인 context로 점진적으로 이동하며 applicability와 다음 route를 좁혀 가는** 패턴입니다.

Agent Skill에서 frontmatter나 index로 후보를 찾은 뒤 `SKILL.md`에서 다시 적용 가능성과 다음 context를 판단하는 구성이 대표적인 예지만, 이 패턴은 Skill에 한정되지 않습니다.

## Purpose

큰 context surface에서는 작은 routing signal로 후보를 좁힌 뒤 필요한 context만 단계적으로 로드하는 편이 효율적일 수 있습니다.

특히 다음과 같은 경우에 유용합니다.

- 많은 asset 중 일부만 현재 task와 관련될 때
- candidate가 길거나 instruction-rich해서 불필요한 load 비용이 클 때
- 잘못 선택된 context가 terminology, assumptions, workflow 같은 noise를 추가할 수 있을 때
- metadata로 후보는 좁힐 수 있지만 실제 적용 판단에는 더 풍부한 local context가 필요할 때
- 선택된 asset이 다시 reference, workflow 또는 다른 asset으로 routing할 때

이는 약한 모델의 정확도 보정에 한정된 패턴이 아닙니다. 최신 고성능 모델에서도 **relevant context density, context economy, locality, progressive disclosure**를 높이는 데 사용할 수 있습니다.

## Core

```text
coarse discovery
      ↓
candidate
      ↓
load candidate-local context
      ↓
applicability / routing decision
      ↓
apply / refine / route onward
```

처음에는 작고 넓은 signal로 후보를 찾고, 필요성이 높아질수록 candidate에 가까운 context를 사용해 적용 방식이나 다음 route를 좁힙니다.

정확히 두 단계일 필요는 없습니다. 한 번의 local check로 끝날 수도 있고 여러 단계로 이어질 수도 있습니다.

## Skill Example

```text
index / frontmatter
→ 이 Skill을 읽어볼 후보인가?

SKILL.md entry
→ 현재 task에 실제로 적용할 가치가 있는가?
→ 어떤 부분이나 reference가 필요한가?

SKILL.md body / references / related assets
→ 필요한 context만 더 사용하거나 다른 route로 연결
```

`SKILL.md` 초반에 짧은 applicability guidance나 routing gate를 두는 방식이 대표적입니다. 본문이 크거나 procedural instruction이 강할수록 더 깊은 context를 사용하기 전에 관련성을 다시 판단하는 가치가 커질 수 있습니다.

실제 token 절감 정도는 harness가 metadata, entrypoint, body, reference를 얼마나 분리해 retrieve/load할 수 있는지에 따라 달라집니다. `SKILL.md` 전체가 이미 context에 들어왔다면 entry gate는 적용 범위와 추가 loading을 좁힐 수 있지만 이미 소비된 body token 자체를 줄이지는 못합니다.

큰 body의 load 비용까지 줄이고 싶다면 `metadata → small entry/gate → larger body/reference`처럼 retrieval surface 자체를 나누는 방법도 있습니다.

이런 gate와 layout은 대표적인 technique이지 Skill format의 필수 요소는 아닙니다.

## Other Forms

```text
INDEX / catalog
→ candidate
→ local entry guidance
→ detailed reference or source

path / glob routing
→ candidate rule/context
→ local applicability check
→ specialized instruction

workflow router
→ candidate workflow
→ entry guidance
→ concrete procedure
```

Routing signal은 frontmatter, manifest, index, rule, directory entrypoint, metadata 등 환경에 따라 달라질 수 있습니다.

## Recommended Default

특별한 이유가 없다면 다음처럼 시작할 수 있습니다.

- 초기 discovery에는 작고 비교적 안정적인 metadata를 사용합니다.
- 후보가 충분히 좁혀진 뒤 candidate-local context를 로드합니다.
- Local entrypoint에서는 applicability와 필요한 다음 context를 짧게 판단합니다.
- 추가 context는 실제로 필요할 때 로드합니다.
- 단계가 늘어날수록 더 구체적이고 관련성 높은 context로 좁혀지는 구성을 선호합니다.

작은 repository나 source가 짧은 환경에서는 바로 읽는 편이 더 단순할 수 있습니다.

## Context Contamination

여기서 context contamination은 instruction hierarchy 실패만을 뜻하지 않습니다. 관련 없는 source를 읽는 것만으로도 현재 task와 무관한 terminology, assumptions, procedures, schema, examples와 추가 token burden이 active context에 들어올 수 있습니다.

최신 모델이 이를 잘 구분하더라도 필요 없는 context를 줄이고 relevant context density를 높이는 것 자체가 유용할 수 있습니다. 따라서 핵심은 "틀린 candidate를 절대 읽지 않는다"보다 **필요성이 높아질수록 더 많은 context를 읽는다**는 데 있습니다.

## Options

- Metadata가 충분히 정확하고 candidate가 작다면 local gate를 생략할 수 있습니다.
- Local entrypoint를 yes/no gate 대신 적용 방식, reference, 대안 candidate를 안내하는 router로 사용할 수 있습니다.
- 여러 asset이 관련되면 candidate 여러 개를 선택하고 각각 필요한 정도만 로드할 수 있습니다.
- Routing metadata는 자동 생성하거나 static index로 유지할 수 있습니다.
- Routing은 더 구체적인 candidate뿐 아니라 다른 후보나 병렬 context로 이어질 수도 있습니다.

## Considerations

- Routing layer가 너무 세밀하면 context 절약보다 관리 복잡도가 커질 수 있습니다.
- Metadata와 underlying source가 따로 관리되면 stale routing 가능성을 고려합니다.
- Local gate 자체가 긴 두 번째 instruction body가 되면 progressive loading의 이점이 줄어듭니다.
- 적절한 loading granularity는 model capability, context window, asset 크기, retrieval cost, task 중요도에 따라 달라질 수 있습니다.
- 목표는 단계를 늘리는 것이 아니라 **필요한 context를 필요한 시점에 적절한 범위로 가져오는 것**입니다.

## Boundary

이 패턴은 **discovery 이후 context를 점진적으로 좁히고 로드하는 routing shape**를 설명합니다.

특정 index format, Skill activation semantics, instruction authority 또는 단계 수를 정의하지 않습니다. Routing/index 구조와 자동화, scope별 instruction injection, asset customization은 각각 별도의 관심사로 볼 수 있습니다.
