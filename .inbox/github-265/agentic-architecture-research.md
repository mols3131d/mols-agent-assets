---
description: PR #265의 에이전틱 병렬 개발 아키텍처 패턴을 심층 조사하고 시나리오 적용·다관점 리뷰·보강 판단의 근거를 추적할 때 참고하는 작업 기록입니다.
---

# PR #265 — Agentic Architecture Research and Review

상태: 과거 설계 조사 기록 및 2026-11-02 개편 근거(실제 모델 행동 평가 미실시). 정본 패턴은 [Software Architecture for Multi-Agent Development](../../catalog/patterns/software-engineering/multi-agent-development-architecture.md)입니다. 아래 이전 Iteration 기록은 당시 설계에 대한 평가이며 현재 개편본의 검증으로 해석하지 않습니다.

## Goal / Scope

- **Goal:** 이 문서를 읽은 agent가 신규 아키텍처와 리팩터링 계획에서 실제 책임·데이터·의존성 경계를 선택하고, 안전한 개선 순서를 제안하도록 돕기.
- **In:** 연구와 반례 비교, 설계 패턴 보강, 가상 변경 시나리오의 건식 적용, 과설계 검토, PR 갱신.
- **Out:** 실제 애플리케이션 구조 변경, 신규 lint/CI/agent orchestration 구현, 머지, 모델 행동 평가를 했다는 주장.
- **Acceptance:** (1) 신규 설계와 레거시 리팩터링 모두에 쓸 수 있는 분할/접점/전환 패턴, (2) 작업 사이와 작업 내부 협업, (3) 복잡성·불변식·운영 위험의 반례, (4) GPPC의 GPP 중심, (5) 문서 내 링크·frontmatter 확인과 검사 한계 기록.

## Research — 직접 활용할 근거

| 근거 | 이 PR에 채택할 시사점 | 주의할 일반화 |
| --- | --- | --- |
| [Microsoft — Domain analysis](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) / [Boundary identification](https://learn.microsoft.com/en-us/dotnet/standard/microservices-architecture/architect-microservice-container-applications/identify-microservice-domain-model-boundaries) | 기능 맵, bounded context, context map, 소유자가 다른 모델과 번역 접점을 이용해 책임 경계 찾기 | DDD의 bounded context는 서비스·폴더와 1:1 필수 관계가 아님 |
| [Parnas — Decomposition](https://doi.org/10.1145/361598.361623) / [Fowler — Microservices](https://martinfowler.com/articles/microservices.html) | 변경 이유에 따른 응집/결합, 반복적인 공동 변경은 경계 재검토 신호 | 공동 커밋 자체만으로 아키텍처 결함 확정 불가 |
| [Fowler — Legacy seam](https://martinfowler.com/bliki/LegacySeam.html) / [Branch by abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) / [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) | 레거시 진입점·소비자를 가로채는 seam, 점진적인 교체·소비자 이전·구 경로 제거 | 모든 변경에 wrapper·feature flag·새 인터페이스를 넣는 방식은 과설계 |
| [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) | 저장소 내 가시적 책임/지식, 빠른 피드백과 적용 가능한 경계가 agent 생산성에 도움 | 특정 실험 팀의 고정 layer·custom lint가 일반 필수는 아님 |
| [Anthropic — Multi-agent research](https://www.anthropic.com/research/multi-agent-research-system) / [ESEM 2026 coordination](https://doi.org/10.4230/LIPIcs.ESEM.2026.18) | 병렬성보다 실제 독립성·작업 상태의 가시성·협업 비용이 중요 | shared worktree 실험은 특정 모델·Python 버그 수정 조건; 저장소의 격리 정책을 변경할 근거 아님 |
| [AsynCodeBench 2026](https://arxiv.org/abs/2609.32662) | 개별 task pass와 cross-agent dependency 충족은 구별해야 함 | 19개 task, 52개 의존성의 연구 결과를 보편 정량 규칙으로 사용하지 않음 |
| [CodeThread — EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2528/) | 최초 수정 성공뿐 아니라 후속 에이전트 변경 시 검증/에러 의미의 보존도 중요 | agent 코드의 일반적인 열등성이라고 확대 해석 금지 |

## Plan

1. **Loop 1 — 구조 설계 렌즈:** 기능 경계, 모델 소유권, 의존성 방향·검증 경계를 실제 구조 예제로 표현하도록 패턴을 보강한다.
2. **Loop 2 — 리팩터링 렌즈:** 레거시 layered 구조에서 소비자·데이터 경계에 seam을 만들고 단계적으로 전환하는 방법을 가상 시나리오에 적용한다.
3. **Loop 3 — 다중-agent 렌즈:** 독립 기능과 하나의 작업 내부 협업을 구분하고, 공유 schema/상태 때문에 실패하는 반례를 다룬다.
4. **Loop 4 — 최소화·반증 렌즈:** 과도한 계약과 체크리스트·추상화·문서 중복을 제거하고, 소형/데이터 집약/이벤트 기반 프로젝트의 반례로 선택성을 검토한다.
5. **Finalize:** 대상 PR source/metadata, Markdown 구성·상대 링크 검사, 미검증 경계, PR 설명을 확인한다.

## Review trajectory

- **Baseline:** 기존 문서는 응집도·국소성의 방향을 제시했지만, 분할된 모델 사이의 읽기/쓰기 소유권, 구조 대안의 선택, 레거시 이행의 단계가 충분하지 않다.
- **Counterexample A:** `controllers/services/repositories`로 분리된 주문 시스템. 단지 `orders/`, `billing/`로 파일을 이동하면 기존 shared `Order`·DB 쓰기와 root 테스트 병목이 그대로 남는다.
- **Counterexample B:** 신규 ETL 파이프라인에서는 billing/shipping 같은 비즈니스 도메인보다 ingestion/normalization/quality의 안정적 데이터 계약과 배치/스트리밍 경계가 더 적절할 수 있다. 기술 layer인지 독립 capability인지 변경 이유로 판정해야 한다.
- **Counterexample C:** 한 기능의 API·스키마를 세 agent가 동시에 바꾸면 파일이 분리되어도 계약 불일치로 통합 실패할 수 있다. 먼저 경계가 안정된 부분을 식별하는 방법이 필요하다.

마지막 단계에서 실제 문서 개정·검토 결과, 잔여 리스크를 갱신합니다.


## Iteration 1 — Research → Plan → Work → Review

- **Implemented:** change-scenario mapping; vertical capability/feature packaging comparison; public surface and data-authority decisions; legacy seam / expand-migrate-contract options; ETL counterexample; representative-change evaluation.
- **Structural review (architecture):** improves ability to propose architecture candidates, but the Before/After example does not yet make `ordering`'s authoritative data and dependency directions explicit. A directory reshuffle could still be mistaken for domain decoupling.
- **Review (refactor safety):** migration strategy mentions regression and compat but does not yet exemplify the *first low-risk change* and the exact point where consumers can work independently.
- **Review (agent collaboration):** distinguishes distinct tasks and same-task agents, but no explicit producer-consumer case shows which work can proceed concurrently after contract stabilization.
- **Review (minimality):** GPP and optional seam choices maintained. No mandatory linter/microservice/large checklist.
- **Disposition:** absorb architecture example and producer-consumer decisions in next loop; reject adding a mandatory plan template or directory schema.

## Iteration 2 — Dry-run assumptions (not runtime agent eval)

**Scenario A — existing layered shop:** `controllers/`, `services/`, `repositories/`, shared `Order` table; jobs: change pricing, change shipping provider, and change order status. A credible plan should compare (A) keeping layout with local seam, (B) packaging pricing/shipping/ordering boundaries in modular monolith, (C) early service split. With no independent deployment requirement, (B) is a reasonable provisional candidate, but shared order-state writes must remain with their authoritative owner. Plan migration should first expose order-state read/command seam and verify regression, then move pricing, then shipping, with versioned/compatible consumers where needed.
**Scenario B — new ETL:** repeated tasks are connector-specific and schema mapping changes. `ingestion/`-`normalization/`-`quality/` by technical stages can cause every connector addition to touch all three. A connector-centered slice with stable normalized record/quality contract is a more promising candidate if each connector owns all three; if normalization is shared policy, centralize its invariant and test consumer adapters.
**Scenario C — two agents one feature:** one agent changing the public error schema while another writes a consumer, a third writes integration tests. Passing local tests is insufficient. Freeze an interface baseline or coordinate a compatible transition; consumer work is parallel only if acceptance/error semantics are already stable.

**Decision:** enrich the pattern with one compact alternative-comparison and *dependency-focused* example instead of producing a large step-by-step plan template.


## Iteration 2 — Scenario dry-run and review

- **Work:** architecture candidates A/B/C compared explicitly; example reshaped around `ordering` as state authority and `billing`/`shipping` as invoked capabilities. Migration now uses one pricing-function extraction and checkout behavior preservation before later consumer conversion. ETL scenario evaluates connector slices versus shared normalization.
- **Review / planning usefulness:** For shop example, an agent can now identify current structure, target boundary, dependency shape, initial low-risk change, consumer migration, and integration feedback. For ETL, the agent can choose a different axis instead of blindly applying business domain packages.
- **Review / adverse conditions:** Shared order state cannot be solved by directory moves; a strong transaction requirement may invalidate separation. A consumer contract change remains an ordered/compatible update even when code paths are disjoint. Avoid presenting implementation details as an enforceable schema.
- **Remaining:** narrow semantic guidance for error/validation contracts during migration, clearer within-one-task agent scenario, and evidence-supported notes against over-aggressive extraction. Resolve in next review/work.
- **Evidence limit:** these are role-separated *reasoned dry runs*, not separate subagent executions, multi-model evals, or empirical productivity measurements.

## Iteration 3 — Adversarial perspectives

1. **Domain designer:** Failure mode is identifying domain packages from nouns rather than invariants and information authority; response: put data/command owner and context-specific model explicitly before folder names. Good in current draft.
2. **Legacy maintainer:** Failure mode is changing error semantics, input validation, security, or transaction order while moving modules; response: add these as examples of behavioral equivalence, not a new mandatory gate.
3. **Agent collaboration designer:** Failure mode is a producer agent changing the schema under a consumer agent and reviewers thinking separate files imply independence; response: add a compact scenario of stable interface versus breaking interface.
4. **Minimalist / operations:** Failure mode is introducing new event infrastructure, wrapper or microservice merely for parallelism; response: prefer in-process module calls and existing seam where sufficient, use one extra abstraction only for actual replacement.
5. **Evaluation skeptic:** Correlation in co-change and published agent benchmarks cannot certify an optimal structure; response: distinguish heuristic, synthetic scenario exercise, and real measurement.

**Disposition:** absorb (2)(3) with small targeted additions. Do not add procedural checklist, module-size metrics, mandatory lints, or model evaluation claims.


## Iteration 4 — Final architecture challenge and disposition

| Planning case (reasoned dry-run) | Expected structural decision | Outcome / residual |
| --- | --- | --- |
| Layer-first shop with shared Order writes | Compare seam-only, modular monolith, service split; keep order-state authority, move pricing first, migrate consumer calls with unchanged behavior | **Adequate for plan drafting.** True transaction atomicity or real code dependency analysis still needed before applying it. |
| New connector-heavy data pipeline | Compare stage-first with source-specific vertical slices; centralize genuinely shared normalized-record invariants, not every helper | **Adequate for choosing candidate axis.** Relative cost depends on measured change patterns. |
| Two agents implementing one changing checkout API | Reject false independence; choose stable producer-consumer baseline or compatible migration; keep integration and error semantics visible | **Adequate for expressing dependencies.** No actual parallel-run test conducted. |
| Tiny CRUD tool with one developer and shallow code | Keep native framework layout and direct tests; extra domain packages/interfaces would add navigation cost | **Adequate anti-overdesign behavior.** |
| Payment/order transaction with strong consistency | Keep invariant and state transition ownership cohesive; do not propose event-driven split just to add parallelism | **Adequate caution.** Concrete transactional design still application-specific. |

**Multi-perspective reconciliation:** Architecture design (pass), brownfield safety (pass), multi-agent integration logic (pass), small-project minimalism (pass), model-behavior evidence (not verified). One material gap remained after Iteration 3: cyclic inter-module dependencies were only identified, not resolved. The final small correction compares a higher-level orchestration owner with extraction of a genuinely shared policy, while warning against an interface that hides a cycle rather than removing it.

**Scope fidelity:** Only pattern guidance and this durable research/review record were changed. GPP without a compulsory Contracts layer, no CI/tooling instructions, no fixed artifact schema, and no microservice-by-default.

## Validation and limits

- **Verified via live GitHub source reads:** The pattern has YAML `description`, GPP headings, a scenario-driven Patterns section, paired fences, no mandatory `Contracts` heading, and links to existing local patterns. The research document has its own frontmatter and relative link.
- **Semantic review:** Three distinct planning cases and two counterexamples were compared against the proposed guidance, with separate failure lenses; these are *simulated reasoning exercises*, not actual independent agent results.
- **Not verified:** Repository-native `rumdl` formatting, generated index/route synchronization where relevant, full CI, implementation tests, controlled multi-agent performance improvement, or applicability to every stack.
- **Further evidence if needed:** Use a real representative codebase and identical planning prompts with/without the pattern. Compare target boundary accuracy, dependency ownership, first safe migration step, integration risk handling, and unintended abstractions; score blind and verify on concrete changes rather than treating prose similarity as success.

**Finalization intent:** Keep PR #265 Draft and unmerged. The durable output is the catalog pattern; this file records sources, scenarios, iteration findings, and unresolved empirical verification.


## 2026-11-02 — Agent-native architecture reframing

**Research question:** 기존 DDD·모듈화·점진적 리팩터링에 agent라는 단어를 추가한 것이 아니라, agent의 작업 특성 때문에 다른 아키텍처 선택이 나오는가?

- **발견 1 / 위치 탐색:** [CORE-Bench](https://aclanthology.org/2026.emnlp-main.1604/)와 [RepoNav](https://aclanthology.org/2026.emnlp-main.1474/)는 코딩 에이전트가 저장소 전체에서 올바른 수정 위치와 주변 맥락을 찾는 일이 독자적인 문제임을 보여준다. 대응은 고정 폴더 구조가 아니라 검색→실제 변경 지점→검증 경로가 서로 연결되도록 하는 것.
- **발견 2 / 국소 피드백:** [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)은 환경 및 관측 가능성이 실제 agent 작업 완료와 연결되는 사례다. 구조 차원의 선택은 의미 있는 동작을 국소 재현·검증할 경계를 제공하는 것이며 특정 lint나 test runner를 강제하는 것은 별도 문제.
- **발견 3 / 협업:** [AsynCodeBench](https://arxiv.org/abs/2609.32662)는 개별 코딩 성공과 agent 간 의존성 충족이 다를 수 있음을 보여준다. [ESEM 2026](https://doi.org/10.4230/LIPIcs.ESEM.2026.18)는 제한된 환경에서 실행 상태 관찰이 유의미함을 보고하지만, 공유 worktree 사용을 일반적으로 권고하지는 않는다. 구조는 의미적 의존성 유형을 드러내고 실행·격리 정책은 별도 owner에 맡긴다.
- **발견 4 / 설계 후보 선택:** [CodeTaste](https://proceedings.mlr.press/v306/thillen26a.html)는 리팩터링을 구현하는 일과 적절한 후보를 발견하는 일의 차이를 뒷받침한다. '변경하지 않음'과 '탐색·검증만 보강'을 구조 재편의 실질적 대안에 포함한다.

**디자인 결정:** 패턴의 중심 평가 단위를 `locate → understand → edit → verify → integrate`의 *agent change episode*로 바꾼다. 기능/도메인 구조 자체는 가능한 수단일 뿐이다. 사람에게 유리한 구조와 같은 선택이 나올 수도 있지만, 이미 모듈화된 코드에서는 재분할이 아니라 국소 피드백을 강화하는 다른 결론을 내릴 수 있어야 한다.

**건식 검토:** 입력원 추가가 잦은 ETL에서 올바른 adapter 검색과 shared schema 소유를 구분하는 계획을 유도하는지, 이미 모듈화된 결제 시스템에서 무의미한 재구조화 대신 관찰·검증 문제를 찾아내는지, 상호의존적 API 변경을 병렬 독립 작업으로 착각하지 않는지 점검했다. 결과는 문서의 추론 가능성에 대한 검토이지 독립 모델 실행 결과가 아니다.

**잔여 한계:** 실제 저장소에서 동일 모델/조건으로 개편 전후의 목표 위치 적중률, 맥락 탐색 비용, 첫 유효 검증까지의 시간, 통합 재작업을 측정하지 못했다. 특정 디렉터리 레이아웃의 agent 생산성 우월성을 주장하지 않는다.
