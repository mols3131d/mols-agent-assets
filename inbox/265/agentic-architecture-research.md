---
description: PR #265의 에이전틱 병렬 개발 아키텍처 패턴을 심층 조사하고 시나리오 적용·다관점 리뷰·보강 판단의 근거를 추적할 때 참고하는 작업 기록입니다.
---

# PR #265 — Agentic Architecture Research and Review

상태: 진행 중. 정본 패턴은 [Agentic Parallel Development Architecture](../../catalog/patterns/software-engineering/agentic-parallel-development-architecture.md)이며, 이 파일은 조사·검토 근거입니다.

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
