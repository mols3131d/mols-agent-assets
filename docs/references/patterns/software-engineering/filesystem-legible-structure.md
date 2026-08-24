---
description: repository의 file·directory 이름, 배치, 계층으로 탐색성을 높일지 판단할 때 참고하며, filesystem legibility와 구조·convention·operability 사이의 경계를 다루는 패턴입니다.
---

# Filesystem-Legible Structure

Filesystem이 **구조를 빠르게 이해하고 탐색하기 위한 정보 표면으로도 활용될 수 있는 상태**를 추구합니다.

Directory와 file의 이름, 배치, 계층, entrypoint만 보아도 무엇이 어디에 있고 어디부터 살펴볼지에 대한 큰 윤곽을 잡을 수 있으면 좋습니다.

다만 **FS가 구조를 결정하지 않습니다.** FS legibility는 구조 선택의 보조 기준입니다. 구조의 적합성, 유효한 convention, 유지보수성과 operability를 희생하면서까지 filesystem을 설명적으로 만들 필요는 없습니다.

이 패턴의 목표는 FS만으로 system을 정확히 복원하는 것이 아니라 **orientation과 navigation 비용을 낮추는 것**입니다.

## Boundary

이 원칙은 source code, 문서, configuration, scripts, tests처럼 repository에서 file과 directory로 드러나는 구조 전반에 적용할 수 있습니다.

적용 강도는 대상, ecosystem과 **실제 navigation environment**에 따라 달라집니다. Tree, CLI, browser가 주요 탐색 수단이면 FS legibility의 가치가 커질 수 있습니다. 반대로 IDE symbol navigation, search, dependency view처럼 더 좋은 탐색 경로가 있다면 filesystem에 모든 의미를 담을 필요가 없습니다. Framework, generator, package manager처럼 layout owner가 따로 있는 영역은 그 convention을 우선합니다.

이 패턴은 **어떤 축으로 구조를 나눌지 정하지 않습니다.**

- domain-first, feature-first, layer-first, component-first 같은 구조 전략을 선택하지 않습니다.
- 특정 architecture style이나 dependency direction을 요구하지 않습니다.
- filesystem hierarchy와 conceptual model을 1:1로 대응시키지 않습니다.
- runtime flow, dependency, ownership, lifecycle 같은 관계를 모두 FS에 표현하려 하지 않습니다.
- README, diagram, code navigation, search, dependency analysis 같은 다른 이해 수단을 대체하지 않습니다.

FS에서 보이는 경계와 이름은 **탐색 단서이지 그 자체로 architecture나 dependency contract의 증거는 아닙니다.** 실제 계약이나 제약의 enforcement는 그 계약을 소유한 별도 mechanism의 책임입니다.

## Application

Legibility를 개선할 때는 **탐색 문제와 구조 문제를 먼저 구분하고, 가장 싼 수단부터** 봅니다.

탐색이 어렵다고 바로 filesystem을 재구성하지 않습니다. 먼저 문제가 실제 responsibility나 structure의 배치에서 오는지, search·symbol navigation·dependency view·index 같은 탐색 수단의 한계에서 오는지 구분합니다. 후자라면 source structure를 바꾸기보다 더 싼 navigation aid를 우선합니다.

그다음에는 다음 순서로 봅니다.

- 이미 필요한 directory와 file에 이해하기 쉬운 naming을 사용합니다.
- 같은 구조를 유지하면서 placement나 entrypoint를 더 찾기 쉽게 만들 수 있는지 봅니다.
- 구조적으로 동등한 선택지가 있다면 orientation 비용이 낮은 쪽을 선호할 수 있습니다.
- tree만으로 부족하다면 작은 README나 index가 충분한지 봅니다.
- hierarchy, file split, placement처럼 filesystem organization 자체를 바꾼다면 줄어드는 탐색·이해 비용이 변경·운영 비용보다 충분히 큰지, 그리고 자연스러운 구조와 convention을 왜곡하지 않는지 봅니다.

핵심은 이 패턴 때문에 새로운 구조를 만드는 것이 아니라 **기존 구조가 가능하면 탐색에도 도움을 주게 하는 것**입니다. 정보량이나 directory 수를 늘리는 것 자체는 legibility가 아닙니다. Tree에서 큰 윤곽과 다음 탐색 지점을 얻을 수 있으면 충분합니다.

## Guardrails

**FS legibility보다 correctness, 적절한 구조, 유효한 ecosystem convention, 유지보수성과 operability가 우선합니다.**

FS를 더 설명적으로 만들기 위해 다음을 악화시키지 않습니다.

- behavioral compatibility와 correctness
- DRY, SRP, cohesion 등 설계 품질
- 책임과 ownership의 명확성
- framework, language, tooling과 generated/vendor 영역의 자연스러운 convention
- build, test, packaging, deployment와 운영 편의성
- 변경 비용과 불필요한 abstraction

Wrapper, abstraction, duplication처럼 software design에 별도 비용을 만드는 장치를 **FS를 설명적으로 보이게 하기 위한 수단으로 추가하지 않습니다.**

FS가 실제 구조를 완전히 설명하지 못하는 것은 허용합니다. 다만 반복적으로 잘못된 탐색을 유도한다면 naming, placement, entrypoint, 작은 안내 문서처럼 구조를 덜 흔드는 수단부터 검토합니다.

## Grounding

이 원칙은 특정 architecture pattern을 채택한 것이 아니라 program comprehension과 information representation에서 관찰된 공통점을 참고합니다.

- **Navigation cue** — [An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks](https://doi.org/10.1109/TSE.2006.116)는 개발자가 unfamiliar code를 탐색할 때 code와 environment의 cue에 의존하고 navigation 자체에 상당한 비용을 쓸 수 있음을 보여줍니다. 이 패턴은 filesystem의 naming과 hierarchy도 그런 탐색 cue로 활용될 수 있다고 봅니다.
- **Trade-off** — [Cognitive Dimensions of Information Artefacts](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDtutorial.pdf)는 visibility와 secondary notation 같은 표현상의 이점도 environment와 다른 특성의 trade-off 속에서 평가해야 한다고 봅니다. FS legibility 하나를 절대적으로 최적화하지 않는 근거입니다.
- **Limit** — [CodeSkyline](https://www.athene-center.de/en/research/publications/codeskyline-a-code-map-visualization-with-juxtapos-5582)은 folder hierarchy를 coupling·centrality와 함께 사용하고, 2025년 [RepoSummary preprint](https://arxiv.org/abs/2510.11039)은 directory-tree 중심 요약만으로 high-level feature traceability가 부족할 수 있음을 지적합니다. FS는 유용한 관점이지만 전체 모델은 아닙니다.

## Short Form

> **FS가 구조를 빠르게 이해하고 탐색하는 데에도 활용될 수 있는 상태를 추구하되, 이를 위해 구조를 왜곡하지 않습니다.**
