# Progressive Context Routing

후보를 한 번에 확정하거나 모든 context를 처음부터 읽기보다, **얕은 discovery에서 더 구체적인 context로 점진적으로 이동하며 applicability와 다음 route를 좁혀 가는** 패턴입니다.

Agent Skill에서 frontmatter나 index로 후보를 찾은 뒤 `SKILL.md` 본문에서 다시 적용 가능성을 확인하는 구성이 대표적인 예지만, 이 패턴은 Skill에 한정되지 않습니다.

## Purpose

큰 context surface에서는 처음부터 모든 source를 읽는 것보다 작은 routing signal로 후보를 좁힌 뒤 필요한 context만 단계적으로 로드하는 편이 효율적일 수 있습니다.

이 방식은 다음과 같은 상황에서 특히 유용합니다.

- 많은 asset 중 일부만 현재 task와 관련될 때
- candidate source 자체가 길거나 instruction-rich해서 불필요한 load 비용이 클 때
- 잘못 선택된 context가 terminology, assumptions, workflow 같은 noise를 추가할 수 있을 때
- 상위 metadata만으로는 대략적인 후보를 고를 수 있지만 최종 applicability는 더 풍부한 local context가 필요할 때
- 선택된 asset이 다시 더 구체적인 source, reference, workflow 또는 다른 asset으로 routing해야 할 때

목적은 단순히 약한 모델의 정확도를 보정하는 데 있지 않습니다. 최신 고성능 모델에서도 **relevant context density, context economy, locality, progressive disclosure**를 높이는 구조적 선택으로 사용할 수 있습니다.

## Core

대표적인 흐름은 다음과 같습니다.

```text
coarse discovery
      ↓
candidate
      ↓
load candidate-local context
      ↓
applicability / routing decision
      ↓
apply or route deeper
```

처음 단계는 비교적 작고 넓은 signal로 후보를 찾고, 다음 단계에서는 candidate에 더 가까운 context를 사용해 적용 여부나 다음 route를 판단합니다.

이 과정은 정확히 두 단계일 필요가 없습니다. 정보 구조와 비용에 따라 한 번의 gate로 끝날 수도 있고 여러 단계의 routing으로 이어질 수도 있습니다.

## Skill Example

Agent Skill에서는 다음과 같은 구성이 자연스럽습니다.

```text
index / frontmatter
→ 이 Skill을 읽어볼 후보인가?

SKILL.md entry
→ 현재 task에 실제로 적용할 가치가 있는가?

SKILL.md body / references / related assets
→ 어떻게 적용하거나 어디로 더 routing할 것인가?
```

`SKILL.md` 본문 초반에 applicability를 다시 확인하는 짧은 gate를 둘 수도 있습니다. 특히 Skill 본문이 크거나 강한 procedural instruction을 포함한다면, 본문 전체를 깊게 소비하기 전에 현재 task와의 관련성을 한 번 더 판단하는 방식이 context cost와 불필요한 context contamination을 줄이는 데 도움이 될 수 있습니다.

이 gate는 대표적인 technique이지 Skill format의 필수 요소는 아닙니다.

## Other Forms

같은 아이디어는 다양한 information surface에 적용할 수 있습니다.

```text
INDEX.jsonl
→ candidate document
→ document-local entry guidance
→ detailed reference

agent catalog
→ candidate agent
→ agent-local suitability guidance
→ tools / context / workflow

glob or path routing
→ candidate rule/context
→ local applicability check
→ specialized instruction

command or workflow router
→ candidate workflow
→ entry guidance
→ concrete procedure
```

Routing layer의 표현 방식은 frontmatter, manifest, index, rule, directory entrypoint, metadata 등 환경에 따라 달라질 수 있습니다.

## Recommended Default

특별한 이유가 없다면 다음과 같은 구성이 단순한 출발점이 될 수 있습니다.

- 초기 discovery에는 작고 비교적 안정적인 metadata를 사용합니다.
- 후보 수가 충분히 줄어든 뒤 candidate-local context를 로드합니다.
- Candidate-local entrypoint에서는 현재 task에 대한 applicability와 필요한 다음 context를 짧게 판단할 수 있게 합니다.
- 더 깊은 routing은 실제로 추가 context가 필요할 때만 진행합니다.
- 단계가 늘어날수록 더 구체적이고 관련성 높은 context로 좁혀지는 구성을 선호합니다.

작은 repository나 context cost가 중요하지 않은 환경에서는 이런 계층을 만들지 않고 source를 바로 읽는 편이 더 단순할 수 있습니다.

## Context Contamination

여기서 context contamination은 반드시 instruction hierarchy 실패를 의미하지 않습니다.

관련 없는 source를 읽는 것만으로도 다음과 같은 정보가 active context에 추가될 수 있습니다.

- 현재 task와 관계없는 terminology
- 다른 workflow의 assumptions와 procedures
- 사용하지 않을 schema나 examples
- 비슷하지만 다른 domain의 constraints
- 추가적인 tokens와 attention burden

최신 모델이 이런 정보를 잘 구분하더라도, 필요 없는 context를 줄이고 relevant context density를 높이는 것 자체가 유용할 수 있습니다.

따라서 progressive routing은 "틀린 candidate를 절대 읽지 않는다"보다 **필요성이 높아질수록 더 많은 context를 읽는다**는 방향으로 이해하는 편이 적절합니다.

## Options

- Metadata가 충분히 정확하고 candidate body가 작다면 별도 local gate를 생략할 수 있습니다.
- Candidate entrypoint를 yes/no gate 대신 적용 방식, 관련 reference, 대안 candidate를 안내하는 router로 사용할 수 있습니다.
- 여러 asset을 함께 적용하는 환경에서는 하나를 배제하기보다 관련 candidate 여러 개를 선택한 뒤 각각 필요한 정도만 로드할 수 있습니다.
- Routing metadata를 자동 생성하거나 static index로 유지하는 방식 모두 가능합니다.
- Candidate-local routing이 다시 다른 candidate로 이어지는 계층형 구조도 사용할 수 있습니다.

## Considerations

- Routing layer가 너무 세밀하면 context 절약보다 관리 복잡도가 커질 수 있습니다.
- Metadata와 underlying source가 따로 관리되면 stale routing 가능성을 고려해야 합니다.
- Candidate-local gate 자체가 장문의 두 번째 instruction body가 되면 progressive loading의 이점이 줄어듭니다.
- 어떤 단계에서 얼마만큼의 context를 로드할지는 model capability, context window, asset 크기, retrieval cost, task 중요도에 따라 달라질 수 있습니다.
- 이 패턴은 routing 단계를 늘리는 것이 목표가 아니라 **필요한 context를 필요한 시점에 더 정확한 범위로 가져오는 것**이 목표입니다.

## Boundary

이 패턴은 **discovery 이후 context를 점진적으로 좁히고 로드하는 routing shape**를 설명합니다.

어떤 index format을 사용할지, Skill activation semantics를 어떻게 정의할지, 어떤 instruction mechanism이 authority를 가지는지, 또는 특정 단계 수를 강제하지 않습니다.

Routing/index asset 자체의 구조와 자동화는 별도의 routing/index pattern으로 다룰 수 있고, scope별 instruction injection은 별도의 context-layering pattern으로 다룰 수 있습니다.
