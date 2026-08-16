# Decisions

이 문서는 `rulesync-agent-assets`의 durable design rationale와 재검토 조건을 기록한다.
Normative behavior는 `requirements.md`가 소유하며, 여기서는 같은 요구사항을 다시 정의하지
않는다.

## D1. Rulesync is the translation backend

**Supports:** R9

**Decision:** Cross-harness format translation은 Rulesync에 위임한다.

**Rationale:** Harness별 schema, discovery path와 capability 변화 추적은 독립적인 유지보수
비용이 크다. 이미 이 문제를 소유하는 backend를 활용하는 것이 KISS와 DRY에 맞다.

**Revisit when:** Rulesync가 필요한 핵심 source model 또는 target을 지속적으로 지원하지
못하고 그 gap이 실제 사용에서 반복될 때.

## D2. Both source models are first-class

**Supports:** R3, R4

**Decision:** Canonical fan-out과 native bridge를 하나의 Skill에서 동등하게 지원한다.

**Rationale:** 어떤 repository는 공용 canonical source를 원하고, 다른 repository는 특정
harness의 native asset을 authoritative source로 유지해야 한다. 하나를 강제하면 불필요한
migration이 생긴다.

**Revisit when:** 제품 방향 자체가 단일 source model만 지원하도록 명시적으로 변경될 때.

## D3. Reuse is evidence-based and precedes conversion

**Supports:** R2, Q1

**Decision:** Direct reuse가 실제로 성립한다는 evidence가 있으면 변환보다 먼저 선택한다.

**Rationale:** 생성물이 늘수록 drift와 ownership ambiguity가 늘어난다. 반대로 evidence 없는
reuse는 compatibility loss를 숨길 수 있으므로 단순함과 검증 가능성을 함께 요구해야 한다.

**Revisit when:** 특정 asset category에서 direct reuse의 discovery 또는 semantics가 구조적으로
불안정하다는 반복 evidence가 생길 때.

## D4. Source authority stays outside the generic Skill

**Supports:** R1, R11

**Decision:** Generic Skill은 repository의 source-of-truth architecture를 선택하거나 ownership을
이전하지 않는다. Generated target은 ordinary conversion에서 derived artifact로 남는다.

**Rationale:** Portability Skill이 project architecture까지 결정하면 orchestration과 ownership
책임이 섞인다.

**Revisit when:** 없음. Ownership transfer는 별도 migration contract로 다룬다.

## D5. Conversion success is not semantic parity

**Supports:** R8, R10

**Decision:** File generation과 runtime semantic compatibility를 별개의 evidence로 취급한다.

**Rationale:** Harness는 같은 개념을 다르게 표현하거나 일부 기능을 지원하지 않을 수 있다.
Generation 성공만 보고하면 실제보다 강한 호환성을 주장하게 된다.

**Revisit when:** 특정 feature에서 backend가 runtime parity를 직접 검증할 수 있게 되더라도
그 검증 evidence를 결과에 명시하는 원칙은 유지한다.

## D6. Preview is the mutation gate

**Supports:** R6

**Decision:** Backend write는 가능한 dry-run/preview 결과를 먼저 확인한다.

**Rationale:** Cross-harness generation은 여러 파일과 config를 동시에 건드릴 수 있으므로
예상 범위 확인이 mutation보다 먼저 와야 한다.

**Revisit when:** Preview가 없는 operation을 지원해야 할 때. 이 경우 먼저 동등한
pre-mutation safety boundary를 정의한다.

## D7. No speculative wrapper or parallel schema

**Supports:** R9, Q1

**Decision:** Concrete하고 반복되는 Rulesync limitation이 확인되기 전에는 custom wrapper,
adapter 또는 parallel canonical schema를 만들지 않는다.

**Rationale:** Rulesync와 겹치는 abstraction은 upstream tracking과 format maintenance를 다시
우리 책임으로 가져온다.

**Revisit when:** 반복되는 backend gap이 작은 policy로 해결되지 않고 별도 automation이 실제
중복과 오류를 줄인다는 evidence가 생길 때.

## D8. Documentation has separate audiences

**Supports:** Q2, Q3, Q4

**Decision:** 문서 audience를 분리한다.

- `SKILL.md`: runtime agent execution contract
- `references/*`: 조건부 backend/project detail
- `README.md`: caller invocation contract
- `.docs/baseline/*`: maintainer product contract와 rationale

**Rationale:** 서로 다른 독자가 같은 문서를 공유하면 runtime context가 불어나고 같은 사실이
여러 위치에서 독립적으로 진화하기 쉽다.

**Revisit when:** 문서 소비 방식 자체가 바뀌더라도 audience ownership은 유지한다.

## D9. Frontmatter follows the common Skill contract

**Decision:** Frontmatter 역할은 다음과 같이 유지한다.

- `description`: activation context와 사용 조건
- `compatibility`: dependencies, runtime prerequisites와 호환 조건
- `metadata`: 식별용 부가 정보

현재 `metadata`에는 `author`만 둔다. 별도 release/version lifecycle이 정의되기 전에는
`version`을 넣지 않는다. 호환성이나 backend 전제도 metadata에 중복 기록하지 않는다.

**Rationale:** 공용 Agent Skills frontmatter의 semantic role을 따르고, stale metadata와 같은
사실의 중복 소유를 피하기 위해서다.

**Revisit when:** 공용 Skill spec, repository validator, 또는 이 Skill의 실제 version lifecycle이
변경될 때.

## Change Discipline

Baseline decision을 깨는 변경은 refactor로 취급하지 않는다. 같은 변경에서 관련
requirements, caller-facing 영향과 migration 여부를 함께 검토한다.
