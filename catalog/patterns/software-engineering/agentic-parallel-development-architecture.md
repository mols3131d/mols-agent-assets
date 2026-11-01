---
description: 여러 agent와 병렬 작업이 독립적으로 변경·검증·통합할 수 있도록 도메인·모듈·계약·의존성 경계를 설계하고 구조 분할의 비용을 판단할 때 참고하는 패턴입니다.
---

# Agentic Parallel Development Architecture

**병렬 개발에 유리한 구조는 디렉터리 수가 많거나 agent마다 소유 폴더가 있는 구조가 아니라, 각 작업이 다른 작업의 내부 구현을 거의 몰라도 변경·검증·통합할 수 있는 구조**입니다.

여러 작업이 동시에 진행되고 각 작업 안에서도 구현·테스트·검토 agent가 협업한다면, 주요 비용은 코드 작성뿐 아니라 **공유 상태 충돌, 넓은 변경 맥락, 계약 조정, 반복적인 통합**에서 발생합니다. 이 패턴은 그 비용을 줄이기 위해 *소프트웨어의 변경 경계*를 어떻게 선택할지 다룹니다.

## Primary Decision

**함께 변경해야 하는 것은 가까이 두고, 독립적으로 바뀔 것은 안정적인 계약 뒤에 둡니다.**

- **변경 독립성**: 한 기능의 통상적인 수정이 무관한 여러 도메인의 내부 파일까지 건드리지 않는가?
- **추론 국소성**: 작업자가 해당 경계의 책임·공개 계약·관련 테스트만으로 대부분의 결정을 내릴 수 있는가?
- **계약 명확성**: 다른 경계가 사용해도 되는 API·데이터·이벤트와 보장해야 할 invariant가 구분되는가?
- **검증 가능성**: 해당 변경의 핵심 동작을 인접 테스트나 경계 계약으로 확인한 뒤 통합 검증으로 확장할 수 있는가?
- **통합 비용**: 별도 작업이 독립적으로 성공해도 합칠 때 충돌·순서 의존·호환성 문제가 반복되지 않는가?

이것은 **서로 다른 agent가 각각 다른 디렉터리를 점유하게 하자는 규칙이 아닙니다.** 파일 경계는 변경 경계의 표현일 뿐이며, 실제 독립성은 데이터 소유권, 의존성, 외부 효과, 실행·검증 계약에 달려 있습니다.

## Choosing a Decomposition

분할 축은 현재 개발 흐름에서 **반복해서 독립적으로 변경되는 책임**을 기준으로 선택합니다. 처음부터 완벽한 도메인 지도를 확정하려 하지 않습니다.

| Axis | Useful when | Failure mode |
| --- | --- | --- |
| **Domain / capability first** | 비즈니스 규칙·데이터·변경 사유가 서로 다른 기능군 | 도메인 간 공통 규칙을 무분별하게 복제하거나 경계를 넘어 직접 DB에 접근 |
| **Feature / vertical slice first** | 사용자 가치 단위로 UI부터 데이터까지 함께 변경 | 공통 invariant가 기능별로 갈라지고 같은 정책을 여러 번 수정 |
| **Layer / technical concern first** | 작고 단순한 프로그램, framework 관행, 실제로 독립적인 기술 구성 요소 | 기능 하나에도 controller·service·repository 등 여러 팀/agent의 공동 수정 필요 |
| **Component / package first** | 재사용 계약이나 독립 릴리스·배포·운영 경계가 분명 | 사용처보다 작은 패키지가 늘고 interface·version 관리가 작업을 압도 |

선택은 배타적이지 않습니다. **도메인·기능 단위로 큰 경계를 정하고, 그 안에서 필요한 경우에만 layer를 나누는** 방식도 가능합니다. 여러 서비스로 쪼개지 않고 한 프로세스 안에서 경계를 유지하는 *modular monolith*도 유효한 시작점입니다.

### Boundary Selection

1. 최근 또는 예상되는 **서로 다른 두세 가지 변경 시나리오**를 적습니다. 예: 요금 계산 변경, 배송 상태 변경, 공통 인증 정책 변경.
2. 각 시나리오에서 함께 변경될 **동작, 데이터 invariant, 통합 지점, 테스트**를 찾습니다. 같은 이유로 자주 바뀌면 하나의 응집된 경계를 우선 검토합니다.
3. 경계마다 **책임과 데이터 소유자, 허용된 의존성, 공개 계약, 실패·오류 의미**를 정합니다. 다른 경계가 private implementation을 직접 읽거나 수정할 필요가 있다면 분할을 재검토합니다.
4. 변경을 다른 경계와 **병렬로 실행했을 때** 공통 파일·스키마·전역 설정·생성물이 어디에서 충돌하는지 확인합니다. 충돌이 불가피하면 소유자와 통합 순서를 명시합니다.
5. 해당 시나리오를 **하나의 경계에서 구현하고 국소적으로 검증할 수 있는지** 시험합니다. 개선 이득이 없다면 새 패키지나 계층을 추가하지 않습니다.

특정 규모의 파일 수, 폴더 깊이, agent 수를 분할 임계값으로 삼지 않습니다.

## Repository Layout Is a Projection

`src/`, `tests/`, `docs/`, `scripts/` 같은 최상위 디렉터리는 **artifact의 성격**을 나타낼 수 있습니다. 반면 그 안에서 `billing/`, `shipping/` 같은 경계는 **제품·도메인의 책임**을 나타낼 수 있습니다. 두 축은 서로 대체하지 않습니다.

다음은 하나의 예이지 필수 템플릿이 아닙니다.

```text
src/
  billing/
    pricing.py
    public.py
  shipping/
    fulfillment.py
    public.py
tests/
  billing/
    test_pricing.py
  shipping/
    test_fulfillment.py
  contracts/
    test_billing_shipping.py
```

- 각 도메인은 자신의 규칙과 private implementation을 소유합니다. 타 도메인은 합의된 공개 표면을 통해 상호작용합니다.
- `tests/` 분리, source 옆 테스트, contract/integration test 배치는 언어·framework의 자연스러운 관행과 실제 검증 경계에 따라 선택합니다. 소스 경로를 문자 그대로 복제하지 않습니다.
- 공유 `common/`·`utils/`는 **모든 도메인의 변경이 집중되는 병목**이 되기 쉽습니다. 실제 공통 invariant나 안정된 재사용 계약이 확인될 때만 공통화합니다. 반대로 중요한 invariant를 편의상 중복하는 것도 피합니다.
- `docs/`, `scripts/`, 생성 코드, schema·migration·root 설정의 물리적 위치는 각 tool과 repository의 owner가 정할 수 있습니다. 위치가 다르더라도 변경 소유권과 영향을 받는 소비자를 찾을 수 있어야 합니다.

파일 탐색성 자체의 원칙은 [Filesystem-Legible Structure](filesystem-legible-structure.md), source와 test의 배치는 [Source-Mirrored Test Structure](source-mirrored-test-structure.md)를 참고합니다.

## Two Levels of Parallelism

**수평 병렬성 — 여러 작업 사이.** 서로 다른 도메인·기능의 작업은 공개 계약에 의존하고, 가능한 한 독립된 파일·데이터·테스트 경계를 변경합니다. 경계를 가로지르는 API 변경은 소비자까지 영향 범위를 확인하고 호환 가능한 전환 경로를 먼저 검토합니다.

**수직 협업 — 한 작업 안의 여러 agent.** 설계·구현·테스트·검토가 같은 변경 경계에 기여할 수 있습니다. 역할이 다르다고 항상 동시에 쓰는 것은 아닙니다. 구현과 별도의 read-only 분석·검토는 병렬화할 수 있지만, 같은 코드·테스트·스키마를 바꾸는 작업은 **명시적으로 나뉜 변경 소유권**이나 **순차적 인계**가 필요합니다.

각 변경 경계가 병렬 협업에 적합한지 확인할 때는 다음 정보를 짧고 명확하게 전달할 수 있어야 합니다.

| Contract | What collaborators need |
| --- | --- |
| **Goal and boundary** | 기대 동작, 바꿀 수 있는 영역, 바꾸지 않을 영역 |
| **Public interface** | 입력·출력·데이터 schema·오류·호환성 약속 |
| **Ownership** | 도메인 책임자, 변경을 통합할 주체, 공유 자산 변경의 결정권 |
| **Verification** | 국소 테스트, 경계 테스트, 필요한 통합 검증과 미검증 위험 |

이 정보가 이미 코드·타입·테스트·작은 문서에서 분명하면 새로운 handoff 양식을 강제하지 않습니다. 여러 agent를 쓰는 오케스트레이션 자체는 작업 workflow의 책임이고, 이 패턴은 **그 오케스트레이션을 가능하게 하는 architecture**에 집중합니다.

### Shared-State Changes

DB migration, root configuration, public schema, generated output, shared lockfile은 도메인 폴더가 달라도 같은 상태를 바꿀 수 있습니다. 이런 변경을 무조건 병렬화하지 않습니다.

- **호환성 있는 계약 변경**은 가능하면 새 계약 제공 → 소비자 전환 → 구 계약 제거의 단계로 나눕니다.
- **동시에 바꾸면 충돌하는 자산**은 한 변경 작업에 소유권을 모으거나, 조정된 순서로 처리합니다.
- **분리 불가능한 invariant**는 한 책임 경계에서 유지합니다. 가짜 독립성을 만들기 위해 critical business rule을 복제하지 않습니다.
- 작업 공간·branch 격리와 Git integration 규칙은 각 repository의 VCS 정책에 맡깁니다. 코드 모듈 분리만으로 concurrent write safety가 보장되지는 않습니다.

## Evaluating the Structure

구조 개선 여부는 *폴더 개수나 agent throughput만*으로 판단하지 않습니다. 서로 다른 변경 두 가지를 가정하거나 실제 작업 기록을 보고 다음을 비교합니다.

| Signal | What to inspect |
| --- | --- |
| 반복적인 cross-boundary touch | 단순 기능 수정마다 무관한 모듈 내부 파일까지 수정하는가? |
| Shared-file contention | 여러 독립 변경이 동일 helper·schema·설정·생성물에 몰리는가? |
| Context and coordination cost | 공개 계약 대신 다른 경계의 내부 구현을 다시 읽고 묻는가? |
| Independent verification | 인접 테스트만으로 의미 있는 신뢰를 얻고 필요한 통합 테스트로 보완할 수 있는가? |
| Integration rework | 병합 뒤 계약 불일치, 순서 의존, 큰 재작업이 반복되는가? |

이 신호가 반복되면 **책임 재배치 → 계약 단순화 → 의존성 방향 정리 → 필요한 검증 보강** 순서로 비용 대비 효과를 비교합니다. 구조를 바꾼 뒤에도 같은 시나리오를 다시 실행해 개선 여부를 확인합니다. 병렬 agent를 더 늘리는 것은 구조적 충돌의 해결책이 아닙니다.

## Guardrails

- **병렬 작업 수와 모듈 수를 일치시키지 않습니다.** 일시적인 작업 계획에 맞춰 영구적인 소프트웨어 경계를 만들지 않습니다.
- **작은 repository에 복잡한 계층·interface·microservice·package를 미리 강제하지 않습니다.** 독립성 증가보다 추상화·운영 비용이 더 크면 단순 구조를 유지합니다.
- **독립 개발과 독립 배포는 다릅니다.** 별도 배포가 필요한지 여부는 운영 요구와 시스템 제약으로 결정합니다.
- **모든 작업이 병렬화 가능한 것은 아닙니다.** 보안 경계, 공통 데이터 모델, 대규모 schema migration과 cross-cutting invariant는 의도된 조정이 필요할 수 있습니다.
- **테스트와 정적 분석은 필요한 계약만 검증합니다.** architecture enforcement는 위반이 실제로 중요하고 재발할 때 도입을 검토하며, framework가 이미 보장하는 규칙을 중복 구현하지 않습니다.
- **Agent에게 읽기 쉬운 구조가 사람과 런타임에 나쁜 구조가 되어서는 안 됩니다.** correctness, 응집도, ecosystem convention, 성능, 운영과 유지보수를 우선합니다.

## Grounding

이 패턴은 새로운 보편적 아키텍처의 실증적 정답이 아니라, 기존의 modularity·loosely coupled delivery 원칙을 **agent의 맥락 비용과 다중 변경 충돌**에 적용한 설계 가설입니다.

- [Parnas, *On the Criteria to Be Used in Decomposing Systems into Modules*](https://doi.org/10.1145/361598.361623) — 모듈을 어떤 기준으로 나누느냐가 변경 용이성과 이해 가능성에 영향을 준다는 고전적 근거.
- [DORA, *Loosely Coupled Teams*](https://dora.dev/capabilities/loosely-coupled-teams/) — 독립적으로 변경·검증·배포할 수 있는 경계가 조정 비용을 줄인다는 인간 개발 조직의 근거. 이를 agent 성능의 직접 측정치로 해석하지 않습니다.
- [OpenAI, *Harness Engineering*](https://openai.com/index/harness-engineering/) — agent-first repository에서 legible architecture와 검증 가능한 불변식을 강조하는 **특정 팀의 사례**. 사례의 고정된 계층 모델을 일반적인 의무 규칙으로 복제하지 않습니다.
- [Anthropic, *Building Effective Agents*](https://www.anthropic.com/research/building-effective-agents) — 병렬 분할과 orchestrator–worker 패턴의 조건. 이 자료는 작업 분할 메커니즘에 관한 것이며, 특정 directory layout의 우월성을 입증하지는 않습니다.

## Short Form

> **변경 이유와 데이터·동작의 책임을 기준으로 경계를 설계하고, 경계 밖에는 작은 공개 계약만 노출합니다.** 여러 작업이 서로의 내부 구현을 몰라도 변경·검증할 수 있게 하되, 한 작업 안의 여러 agent가 공유 자산을 동시에 수정해야 하는 경우에는 소유권과 인계·통합을 명시합니다. 구조 분할의 비용이 협업 이익보다 크면 더 단순한 구조가 낫습니다.
