---
description: PR #265의 다중 코딩 에이전트 소프트웨어 아키텍처 패턴에 대한 최종 셀프 리뷰 발견 사항과 후속 조사·개편 방향을 검토할 때 참고합니다.
---

# PR #265 — Multi-Agent Architecture Follow-up Research

상태: 최종 셀프 리뷰 기록 완료 / 추가 근거 조사 중. 대상: [Software Architecture for Multi-Agent Development](../../catalog/patterns/software-engineering/multi-agent-development-architecture.md) (검토 기준 `8dfd8f94bc2370f1fe85844a05db58eb10f43cd0`).

## Review findings (2026-11-02)

**판정: 보완 후 머지 권장.** 문서명은 다중 에이전트 개발용 소프트웨어 아키텍처를 약속하지만, 현재 다섯 패턴 중 네 항목의 초점은 주로 단일 에이전트의 탐색·검증·맥락 복원·리팩터링 후보 선택이다. 다중 에이전트 협업은 세 번째 패턴에 집중되어 있다.

| Priority | 위치 | Finding | 보완 목표 |
| --- | --- | --- | --- |
| High | 원문 53–67행 | 독립/생산자–소비자/공유 불변식을 분류하나, **한 기능을 여러 에이전트가 함께 개발하도록 하는 소프트웨어 책임·모듈·통합 경계**를 구체적으로 선택하게 만들지 못한다 | 다중 에이전트 변경 단위와 공유 의미의 소유 구조를 설계 후보로 제시 |
| High | 원문 98–143행 | 데이터 파이프라인 예시는 주로 agent 하나의 입력원 추가를 설명한다. 여러 agent가 **동시에 하나의 기능을 구현하는 before/after 반례**가 없다 | 동일 요구에 대한 구조 대안과 병렬 의존성, 통합 검증의 차이를 보여주는 시나리오 |
| Medium | 원문 27–51행, 69–79행 | search/tooling, test/runtime feedback, handoff 같은 비아키텍처 문제와 구조적 문제의 경계가 느슨하다 | 아키텍처가 직접 소유하는 책임 경계·검증 seam만 핵심에 두고 외부 메커니즘을 명시적으로 구분 |
| Medium | Grounding 및 전체 | agent/multi-agent 생산성 향상은 구조적 휴리스틱이지 인과적으로 검증되지 않았다 | 증거 수준 구분과 대표 시나리오 기반 비교·향후 모델 평가 설계 |

**보존할 점:** GPPC의 GPP 구조, 작고 선택적인 패턴, '현 구조 유지' 선택, 불변식과 안전성 우선, microservice·interface·linter·문서 추가 강제 없음.

**검토 범위:** 아키텍처 패턴의 설계 유도력과 설명 정합성. 이 기록은 독립 에이전트의 실제 병렬 실행·비교 실험, 실제 저장소 리팩터링, CI 결과가 아니다.

## Research questions

1. 파일 충돌 감소와 **의미적 충돌·변경 의존성 감소**는 어떤 구조 선택에서 달라지는가?
2. 다중 agent의 작업 독립성이 실제로 생기는 코드·데이터·계약·검증의 '완결 단위'는 무엇인가?
3. API/schema 변경, DB transaction, end-to-end workflow 등 협업이 필요한 경우 어떤 설계 대안이 있으며 무엇을 병렬화하지 말아야 하는가?
4. 구조 변경이 아닌 orchestration, workspace isolation, search, tool/harness improvements를 어떻게 구분하는가?
5. 설계 전후를 실제로 비교할 때 단순 agent 수나 파일 수가 아닌 어떤 결과를 측정할 것인가?

## Additional research — research and review loops (2026-11-02)

### Loop 1 — 병렬 코딩의 문제를 정확히 분리하기

**관찰:**

- [CooperBench (2026)](https://arxiv.org/abs/2601.13295): 오픈소스 12개 라이브러리에서 협업 가능하지만 충돌할 수 있는 두 기능을 agent 둘에게 맡겼을 때, 함께 개발한 성공률이 하나가 두 기능을 처리할 때보다 평균 약 30% 낮았다고 보고. *협업 실패가 기술적으로 중요하다*는 근거이지 '모듈 경계 변경이 30% 개선한다'는 근거는 아님.
- [AsynCodeBench (2026)](https://arxiv.org/abs/2609.32662): 19개 실제 저장소 작업의 52개 방향성 의존성을 별도로 검증. task pass와 cross-agent dependency pass를 구분해 평가할 필요.
- [Passes Alone, Fails Together (2026)](https://arxiv.org/abs/2609.25396): 텍스트 충돌이 없어도 서로 다른 변경이 의미적으로 충돌할 수 있음. 단, **실제 merged Django PR 417쌍의 834회 실행에서 간섭 1회**와 인위적으로 의존성을 만든 Django 시나리오의 높은 간섭률을 구분해야 함. 인위적으로 만든 사례의 실패율을 일반 프로젝트의 실제 발생률로 옮기지 말 것.
- [AgenticFlict (2026)](https://arxiv.org/abs/2604.03551): 병합 시뮬레이션이 가능한 agent PR 표본에서 텍스트 충돌을 관찰. 연구의 표본·시뮬레이션 정의를 벗어나 '대부분의 병렬 agent 작업이 충돌한다'고 단정할 수 없음.

**판단:** agent 수·폴더 수·PR 수·텍스트 충돌률로 구조의 성공을 정의하지 않는다. 목표는 **개별 변경이 통합 후에도 의미와 불변식을 보존하도록 하는 구조**다. 파일 격리만으로 해결되지 않는 API·data·policy·상태 전이 의존성을 핵심 비교 축으로 삼아야 한다.

### Loop 2 — 협업 가능한 소프트웨어 구조로 연결하기

**설계 가설:** 다중 에이전트 개발에 유리한 기본 단위는 *대표 변경을 스스로 찾고, 자체 구현 범위 안에서 끝내고, 가까운 동작을 검증할 수 있는 단위*이다. 단위 사이 의존 관계는 쉽게 확인할 수 있는 **공개 접점과 한 곳의 의미상 소유권**으로 드러나야 한다. 이것을 물리적 agent별 folder로 고정하지 않는다.

아키텍처 후보를 고르는 방법:

| 반복 변경 유형 | 구조적으로 고려할 선택 | 피할 과설계 / 반례 |
| --- | --- | --- |
| 같은 계약을 사용하는 독립 구현이 여러 개 필요 | 의미 있는 확장점 아래 각각의 구현·인접 테스트를 묶고, 소비자는 공개 동작만 호출 | 단순히 agent 수만큼 모듈을 복제하거나 모든 helper에 interface 추가 |
| 단일 기능이 여러 정책·통합을 조합 | 조합의 의미와 통합 검증을 책임지는 상위 use case / application entrypoint를 하나 둠 | 조합 코드를 각 기능에 중복해 쓰거나 상호 호출 cycle을 새 wrapper로 감춤 |
| 모든 구현이 한 schema 또는 정책을 공유 | 실제 변경 책임을 가진 영역 하나가 authoritative model·rule을 소유; 소비자는 public representation이나 변환을 사용 | `shared/`에 모든 모델을 몰아넣어 모든 agent가 동시에 수정 |
| provider–consumer 계약이 변함 | 이미 존재하는 호환 접점을 유지하거나 필요할 때 expand → migrate → contract로 소비자 전환을 분리 | 계약이 바뀌기 전 동시 개발을 '독립 작업'이라고 선언; 호환성을 영구적으로 유지 |
| 강한 정합성·원자적 상태 변경 | 한 소유 경계에서 state transition을 유지하고, 공급자 플러그인 등 주변부만 독립화 | 병렬 개발만 위해 트랜잭션을 분산 서비스/이벤트로 쪼갬 |

근거와 해석: [Microsoft DDD context mapping](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis)은 공급자/소비자 관계, published language, anti-corruption layer 등 관계 선택지를 제시한다. [Fowler, Microservice Trade-Offs](https://www.martinfowler.com/articles/microservice-trade-offs.html)는 좋은 modular monolith도 경계를 가질 수 있고 microservice에는 배포·데이터·운영 비용이 있음을 강조한다. [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html)는 불일치 API를 단계적으로 전환하는 기존 기법이다. 이것들은 인간 개발에서도 통용되며, **agent-specific한 차이는 변경 단위와 cross-agent dependency 충족을 설계 후보의 직접적인 평가 대상으로 삼는 것**이다.

**특히 구분할 것:**
- 코드 모듈의 *조합 책임(owner)*은 런타임 동작의 소프트웨어 아키텍처다. 어떤 agent에게 조합 작업을 위임하는가는 orchestration이다.
- 타입·스키마·입출력의 *공개 의미(owner)*는 소프트웨어 아키텍처다. agent 간 메신저·handoff·작업 순서 프로토콜은 orchestration이다.
- 테스트 가능한 접점을 설계하는 일은 아키텍처다. 특정 runner, worktree, CI, context injection 구축은 harness/개발환경 책임이다.

### Loop 3 — 여러 agent가 한 기능을 개발하는 구조 비교

**가상 요구:** checkout에 카드와 계좌이체 결제 방식을 추가하고, 할인 정책을 수정하며, 결제 결과를 주문 상태에 반영한다. 세 변경이 동시에 진행될 수 있지만 **주문 상태 전이, 결제 오류 의미, idempotency**는 공유된다. 아래는 정해진 정답이 아니라 구조 후보의 비교용 시나리오다.

**A. 횡단 수정이 필요한 현 구조(예시)**

```text
src/
  checkout.py      # 결제 방식 분기 + 주문 상태 갱신 + 할인
  payments.py      # 여러 provider 구현과 반환 형태
  models.py        # 공유 주문/결제 모델
  utils.py
tests/test_checkout.py
```

독립 agent 3명이 각기 카드, 계좌이체, 할인을 수정하면 `checkout.py`와 `payments.py`의 동일 조건 분기와 반환 의미를 반복해서 만질 위험이 있다. 다른 파일에서 수정되더라도 공유 모델의 변화가 소비자까지 전파될 수 있다.

**B. 반복 변경을 가정한 선택적 구조(모듈식 모놀리스의 한 예)**

```text
src/
  ordering/
    checkout.py          # 실제 checkout 조합 책임
    order_state.py       # 주문 상태 전이의 쓰기 소유
  payments/
    result.py            # 결제 결과/오류의 공개 의미 소유
    service.py           # 기존 소비자에게 노출한 결제 동작
    providers/
      card.py
      bank_transfer.py
  pricing/
    discount.py
tests/
  payments/providers/...
  pricing/...
  ordering/test_checkout.py
```

- 카드 구현과 계좌이체 구현은 `payments`의 동일 공개 의미를 **소비**하고 각자의 구현·테스트를 수정하므로 병렬로 진행할 후보가 된다. 할인 정책은 `pricing`에서 별도로 진화할 수 있다.
- `ordering/checkout.py`는 요금·결제 결과를 조합하지만 `payments`가 주문 상태를 직접 기록하지 않는다. `ordering/order_state.py`가 authoritative owner라고 **가정했을 때만** 이 구조가 적절하다. 실제 결제·주문의 원자성이 다른 경계에 있다면 구조를 조정한다.
- `payments/result.py`의 오류/재시도/idempotency 의미가 불안정하면 provider 작업은 아직 진정한 독립 작업이 아니다. 먼저 계약 의미를 명확하게 하거나 **순차 변경**을 선택한다.
- provider가 둘뿐이고 변경 빈도가 낮다면 provider별 파일·패키지·테스트를 새로 분리하는 비용이 이득보다 클 수 있다. 기존 코드 + 명시된 작은 seam이 더 좋은 C안이 된다.
- local provider 테스트는 card·bank 구현의 오류를 검출하지만, 주문 상태/취소/중복 청구 등을 포함한 checkout 통합 검증을 대체하지 않는다.

**C. 반례—schema를 두 agent가 동시에 바꿈:** 한 agent가 `PaymentResult.status`의 값을 변경하고 다른 agent가 해당 값을 해석하는 checkout을 작성하면 코드가 다른 디렉터리에 있어도 의존한다. 선택은 (1) 의미를 기존 상태로 고정해 소비자 작업을 먼저 유지, (2) 호환 가능한 확장 후 소비자 전환, (3) 하나의 결합 변경으로 함께 구현 중 실제 의존성과 맞는 것. 모든 경우에 소비자 계약과 통합 동작을 검증해야 한다.

**비교의 질문:** 각 선택지에서 card, bank, 할인, 주문 상태를 변경하는 agent가 무엇을 읽고, 어느 파일/의미를 공동 수정하며, 언제 각각의 테스트가 유효하고, 어떤 테스트가 전체 결과를 보증하는가? `B`는 특정 조건에서 유리한 후보일 뿐 자동 승자가 아니다.

### Loop 4 — 도구·운영과 구조를 분리하고 반례로 압축

- [GitHub의 agent 병렬 위임 가이드](https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/delegating-and-parallelizing-work-with-agents)는 독립 작업 분해, 의존성 확인, 별도 컨텍스트와 결과 결합을 설명한다. 이것은 **오케스트레이션 역량**의 근거이지 기능 모듈의 파일 배치에 관한 실증은 아니다.
- [OpenAI Harness Engineering (2026)](https://openai.com/index/harness-engineering/)의 고정된 레이어와 dependency lint, 격리 실행·관찰 가능성은 특정 프로젝트의 사례다. 공개 계약과 불변식 검증의 가치만 구조적 선택에 참고하고 **고정된 layer·custom lint·인덱싱 문서**를 모든 저장소에 강요하지 않는다.
- [Anthropic Effective Harnesses (2025)](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)는 세션 간 작업 정보 복구의 실무 사례다. **agent handoff 방법**은 software architecture 정본이 아니다.
- [Pact contract testing](https://docs.pact.io/)은 소비자 기대와 provider 구현을 독립적으로 검사할 수 있는 방법 중 하나다. 그러나 contract testing은 내부 기능 테스트나 전체 비즈니스 invariant 검증을 대체하지 않는다. 작은 단일 프로세스 프로젝트에는 기존 단위·통합 테스트면 충분할 수 있다.
- [ESEM 2026 shared Git workspace coordination](https://doi.org/10.4230/LIPIcs.ESEM.2026.18)은 peer action observation의 효과를 보여주지만, 이를 이유로 저장소의 worktree 격리 정책을 바꾸거나 아키텍처 패턴 안에 shared workspace 운영을 넣지 않는다.

**반증 1 / 높은 일관성:** 주문·결제 원자성이 핵심이면 독립 작업을 위한 서비스 분할이 오히려 correctness와 운영을 악화시킨다. 한 소유 경계를 유지하고 주변 adapter만 병렬화할 수 있다.

**반증 2 / 작은 CRUD:** 변경·테스트 경로가 짧고 협업 의존성이 거의 없다면 현재 framework layout을 유지한다. agent별 패키지, 계약 테스트, 설계 문서를 새로 만들 이유가 없다.

**반증 3 / ETL schema 변동:** source adapter 간 독립성이 있어도 모든 입력원이 공통 정규화 schema 변경에 따라 수정된다면 그 작업은 병렬 독립이 아니다. owner 1곳과 변환 접점을 명시하거나 schema 호환 전환을 먼저 고려한다.

**검토 결론:** '모든 에이전트를 항상 병렬화 가능하게 만들기'는 목표가 아니다. **독립 가능한 범위를 높이고, 독립 불가능한 공유 의미를 숨기지 않으며, 전체 검증 책임을 잃지 않는 구조**가 목표다.

## Document revision proposal (not applied)

다음 패턴 개정은 새 'multi-agent architecture' 방법론을 과하게 발명하기보다 현재 본문의 비중을 수정하는 방식이 적합하다.

1. Goal/Principles에서 작업 하나의 `locate → understand → edit → verify → integrate`를 유지하되, **여러 동시 변경이 안전하게 결합되는 비용**을 주목적으로 명시한다.
2. Patterns의 중심을 **(a) 병렬 변경의 완결 단위, (b) 공유 schema·불변식의 단일 의미 소유권, (c) 상위 조합/통합 경계, (d) 변화 중인 계약의 호환 경계**로 이동한다. 고정 개수·레이어·용어는 강제하지 않는다.
3. 기존 탐색·컨텍스트 복원·리팩터링 후보 선택은 아키텍처 판단에 직접 기여하는 내용만 남겨 축약하거나 관련 pattern/도구 owner로 연결한다.
4. 본문 예시의 주역을 **동시에 한 기능을 만드는 카드/이체/할인/checkout 시나리오**로 바꾼다. 기존 ETL 예시는 필요하면 한 문단의 반례로 남긴다.
5. '이 구조를 택해야 할 신호'와 '이 구조를 택하면 안 되는 신호'를 같이 보여준다. 추가 package, event bus, shared-contract repository, linter, workflow step은 요구하지 않는다.

## Evidence/evaluation plan

**가설:** 같은 작업 집합을 같은 모델·하네스·자원에서 실행할 때, 다중 에이전트 변경 경계가 더 명확한 소프트웨어 구조는 특정 결합 패턴에서 통합 후 성공률을 높이거나 재작업 비용을 줄일 수 있다. 아직 입증되지 않았다.

- 비교군: (A) 현재 횡단 구조, (B) 변경/정본/조합 경계를 분리한 구조, (C) 현 구조 + 최소 seam·계약 설명만 보완. 각각 **동일 기능 요구**에 대해 여러 agent 실행과 단일 agent 기준선을 둔다.
- 케이스: 독립 provider 2개+할인 동시 개발, producer/consumer의 breaking schema 동시 변경, 강한 상태 정합성 checkout, 소형 CRUD negative control, schema 진화 중 ETL.
- 결과: 통합 후 요구사항/기존 동작 테스트, cross-agent dependency pass(AsynCodeBench 개념), merge 전후 semantic regression, 수동 수정/통합 재시도, 완료까지의 wall-clock, model/tool 비용, 새 추상화와 구조 유지비.
- 통제: 동일 base commit·model·prompt·agent 수·tool access·검증 조건·작업 공간 격리 및 반복 실행. 아키텍처 변경 자체가 요구 구현과 충돌하면 안 된다. 단순 PR 수나 generated LOC로 성공 판정하지 않는다.
- 단순한 문서 dry-run은 개념적 검토만 증명한다. 실제 agent 실험, 유의미한 통계, 장기 유지보수 비용은 모두 **미검증**이다.

## Research closure

**이번 추가 조사 결과:** 구조적 선택지는 확인했지만, 최종 pattern 본문에는 아직 반영하지 않았다. 심층 근거는 다중 agent 협업 문제의 존재를 지지하고, 특정 고정된 코드 레이아웃을 일반적 정답으로 증명하지 않는다. 다음 행동은 이 연구안에 따라 **표준 패턴을 간결하게 개편하고 실제 사례 평가를 분리**하는 것.

**Scope/verification:** public sources and live PR/file content checked; dry-run scenario reasoning performed. No actual multi-agent runtime experiment or CI; no architectural source code modified; PR stays Draft/unmerged.
