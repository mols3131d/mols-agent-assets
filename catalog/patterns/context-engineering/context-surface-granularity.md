---
description: instruction·Skill·Rule·router·index·configuration 같은 context surface를 얼마나 분리할지 판단할 때 참고하는 pattern으로, 분리의 이점과 관리·discovery·routing·resolution 비용 사이의 granularity를 다룹니다.
---

# Context Surface Granularity

Agent가 발견하거나 로드하는 context surface는 **독립적인 책임과 선택 가치가 있을 만큼만 분리하고, 분리로 생기는 관리·routing 비용이 이점을 넘지 않게 유지**합니다.

여기서 context surface는 instruction, Skill, Rule, router, index, configuration, reference처럼 agent의 작업 context를 구성하거나 그 context로 연결하는 자산을 넓게 뜻합니다.

## Purpose

Context를 적절히 나누면 scope locality, selective loading, reuse와 ownership을 개선할 수 있습니다. 반대로 surface를 지나치게 잘게 나누면 각 파일은 작아져도 무엇을 찾아야 하는지, 어떤 조합이 적용되는지, 무엇을 함께 갱신해야 하는지 판단하는 비용이 커질 수 있습니다.

이 패턴의 목표는 파일 수를 줄이는 것이 아니라 **각 surface의 분리가 실제 독립성을 표현하도록 granularity를 맞추는 것**입니다.

## Core

새 context surface에는 보통 다음과 같은 고정 비용이 따라옵니다.

- 누가 무엇을 소유하는지 이해하고 관리하는 비용
- candidate를 발견하고 서로 구분하는 discovery / routing 비용
- 여러 layer나 source가 겹칠 때 최종 적용 context를 해석하는 resolution 비용
- source, metadata, index, reference 사이의 drift 가능성

따라서 단순히 내용이 길거나 주제가 다르다는 이유만으로 분리하지 않습니다. 다음 중 하나 이상이 실제로 독립적일 때 분리가 더 자연스러울 수 있습니다.

- **Applicability** — 서로 다른 상황에서 적용되는가?
- **Loading** — 필요한 시점이나 context가 다른가?
- **Reuse** — 다른 workflow나 scope에서 독립적으로 재사용되는가?
- **Ownership / change** — 변경 이유나 관리 owner가 실질적으로 다른가?
- **Lifecycle** — 생성·갱신·폐기 주기가 다른가?

반대로 거의 항상 함께 적용되고, 같은 이유로 바뀌며, 독립적으로 선택하거나 재사용할 필요가 없다면 같은 surface에 두는 편이 더 단순할 수 있습니다.

## Trade-offs

위험과 대응을 따로 분리하기보다 같은 판단 안에서 함께 봅니다.

| 상황 | 위험과 대응 |
| --- | --- |
| Surface를 지나치게 세분화함 | 관리 지점과 dependency가 늘고 작은 변경에도 여러 owner를 따라가야 할 수 있습니다. **독립적인 applicability, loading, reuse, ownership 또는 lifecycle이 없다면 합치거나 분리하지 않습니다.** |
| 비슷한 candidate가 많아짐 | Routing signal이 겹치면서 잘못 선택하거나 필요한 context를 놓칠 가능성이 커질 수 있습니다. **책임과 적용 범위를 구분할 수 있게 하고, 실제 차이가 약한 candidate는 통합합니다.** |
| Router, index, layer가 연쇄적으로 늘어남 | Context를 읽기 전에 discovery와 resolution 자체가 새로운 비용과 failure point가 될 수 있습니다. **더 직접적인 route로 충분하면 중간 surface를 만들지 않거나 줄입니다.** |
| 오래되거나 가치가 불명확한 surface가 남음 | Stale metadata, route와 assumptions가 현재 source보다 오래 살아남을 수 있습니다. **사용 빈도만으로 제거하지 않고 독립적인 가치와 중요도를 확인하되, 중복·obsolete하거나 별도 owner로 남을 이유가 없으면 합치거나 제거합니다.** |
| 너무 많은 책임을 하나에 모음 | 항상 불필요한 context가 함께 로드되거나 독립적인 책임의 변경이 서로 결합될 수 있습니다. **선택적 loading, 재사용 또는 독립 변경의 실질적 이점이 생기면 그때 분리합니다.** |

즉 작은 surface가 항상 좋은 것도, 큰 surface가 항상 나쁜 것도 아닙니다. **분리로 얻는 locality와 선택성이 분리 후 필요한 discovery·coordination 비용을 정당화하는지**를 봅니다.

## Recommended Default

특별한 이유가 없다면 단순한 surface에서 시작하고 실제 독립성이 드러날 때 분리합니다.

- 거의 항상 함께 읽고 적용한다면 먼저 함께 둡니다.
- 별도 routing signal이 필요할 만큼 applicability가 달라지면 분리를 고려합니다.
- 큰 context 때문에 반복적으로 불필요한 loading이 생기면 필요한 부분을 독립 surface로 분리할 수 있습니다.
- 새로운 router나 layer를 추가하기 전에 기존 entrypoint, metadata 또는 가까운 owner로 충분한지 확인합니다.
- Surface를 추가하는 것만큼 합치고 제거하는 것도 정상적인 maintenance로 봅니다.

정량적인 파일 수나 최대 단계 수를 규칙으로 만들 필요는 없습니다. 적절한 granularity는 repository 규모, model과 harness capability, retrieval cost, 변경 빈도와 운영 방식에 따라 달라질 수 있습니다.

## Related Patterns

| Pattern | Relationship |
| --- | --- |
| [Progressive Context Routing](progressive-context-routing.md) | 선택된 context를 어떤 순서와 깊이로 점진적으로 로드할지 다룹니다. 이 패턴은 그런 candidate와 loading surface를 얼마나 나눌지 판단합니다. |
| [Layered Context Instructions](layered-context-instructions.md) | Structural / semantic scope에 어떤 mechanism을 사용할지 다룹니다. 이 패턴은 그 layer와 context surface의 분리 정도를 조절합니다. |
| [Routing & Index Assets](routing-index-assets.md) | 별도 discovery/routing surface의 역할과 authority를 다룹니다. 이 패턴은 그런 surface를 추가하거나 통합할 때의 공통 비용을 다룹니다. |
| [Asset Configuration Surface](asset-configuration-surface.md) | Reusable core와 customization delta의 분리를 다룹니다. 이 패턴은 configuration source와 layer를 얼마나 세분화할지 판단할 때 함께 사용할 수 있습니다. |
| [Semantic Asset Roles](semantic-asset-roles.md) | 무엇을 독립 책임으로 볼지 판단하는 관점을 제공합니다. 역할이 다르다는 사실만으로 반드시 파일이나 surface를 분리해야 하는 것은 아닙니다. |

## Boundary

이 패턴은 특정 file size, document count, directory depth, routing hop 수 또는 context token budget을 표준으로 정하지 않습니다. 또한 각 Skill, Rule, index, configuration의 고유한 activation, precedence, schema나 lifecycle을 대신 정의하지 않습니다.

핵심은 **surface 수를 최소화하는 것이 아니라, 분리와 통합이 실제 책임·선택·재사용 경계를 반영하도록 유지하는 것**입니다.
