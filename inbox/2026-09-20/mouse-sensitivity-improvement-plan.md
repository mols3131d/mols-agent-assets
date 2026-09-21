# `mouse-sensitivity` 개선 Run — Plan

이 Plan은 [`mouse-sensitivity-improvement-research.md`](mouse-sensitivity-improvement-research.md)의 결론을 구현 대상으로 좁힌다.

## Work 1 — Entrypoint / activation

대상: `src/rulesync/.rulesync/skills/mouse-sensitivity/SKILL.md`

- description에 desktop, pointer/cursor game, first-/third-person game, requested conversion 범위를 명확히 표현한다.
- Route가 profile / desktop / generic gaming / first-person / third-person / conversion의 조건부 loading을 소유하게 한다.
- Core는 universal optimum 부정, input pipeline 분리, decision-changing input만 사용, game-native value 보존 정도만 남긴다.
- `cm/360`, eDPI, mousepad 세부 판단, pro setting, profile persistence 세부 규칙은 references로 내린다.
- Workflow는 `context 확인 → reference load → 작은 조정/필요 시 조사 → 실제 사용 검증`의 최소 흐름으로 줄인다.

Acceptance: 사무/코딩 요청에서 게임 변환 detail이 항상 로드되지 않으며, pointer game 요청도 metadata와 Route에서 자연스럽게 수용된다.

## Work 2 — Generic gaming scope

대상: `references/gaming.md`

- 먼저 `camera/aiming`, `pointer/cursor`, mixed input context를 구분한다.
- native sensitivity는 게임별 값으로 보존하고 게임 간 숫자를 직접 비교하지 않는다.
- pointer/cursor game은 target acquisition, repeated travel, edge/map navigation 같은 pointer behavior를 기준으로 판단한다.
- camera-specific `cm/360`, turn, mousepad constraint는 해당 context에서만 사용한다.
- FPS/TPS 세부 동작은 각 reference로 넘긴다.

Acceptance: FPS/TPS 이외의 게임에서도 generic gaming reference가 유효하며 불필요한 camera 가정을 하지 않는다.

## Work 3 — FPS / TPS / desktop refinement

대상: `references/first-person.md`, `references/third-person.md`, `references/desktop.md`

- generic gaming과 중복되는 문장을 제거한다.
- first-person은 acquisition, correction, tracking, turn, ADS/zoom의 특수 판단만 남긴다.
- third-person은 camera/reticle/character coupling과 state별 sensitivity의 특수 판단만 남긴다.
- desktop은 logical workspace, precision/travel, acceleration의 workflow 영향만 유지한다.

Acceptance: 각 reference가 독립 loading 가치가 있고 generic rule을 불필요하게 반복하지 않는다.

## Work 4 — Profile contract / example

대상: `references/profile.md`, `assets/profile.example.json`

- config top-level order를 `version → mouse → mousepad → os → displays → games`로 통일한다.
- display order를 `name → primary → resolution → scale`로 통일한다.
- `games.<id>.type`을 optional `games.<id>.input_context`로 변경한다.
- `input_context`는 descriptive routing hint이며 closed enum이 아니라고 명시한다.
- unknown/optional OS pointer setting과 game sensitivity는 example에서 생략한다.
- default game list는 Counter-Strike 2, Overwatch 2, Valorant를 유지한다.
- concrete sample 값은 사용자 실제 환경과 겹치지 않는 neutral example을 사용한다.

Acceptance: example이 user state처럼 보이지 않고, 실제 profile은 확인된 값만 추가하도록 contract가 읽힌다.

## Work 5 — Conversion simplification

대상: `references/conversion.md`

- exact conversion은 user request 또는 결과에 필요한 경우만 수행한다.
- source priority를 `official/current game info → maintained tool/converter → measured in-game comparison` 정도로 유지한다.
- 고정 converter URL 목록과 internal formula reconstruction 권고를 제거한다.
- 결과는 적용 조건과 함께 시작값으로 제시하고 target game에서 검증한다.

Acceptance: external research behavior는 유지하면서 stale source maintenance와 계산 중심 context가 줄어든다.

## Work 6 — Text optimization

대상: 위 모든 runtime text

`mols-text-optimizer` 제약을 보조적으로 적용한다.

- technical token, routing target, 강도, 조건, boundary를 보존한다.
- 같은 의미를 metadata / entrypoint / reference에 중복한 부분을 줄인다.
- 구조 변경이 필요한 개선은 Agent Asset owner가 먼저 수행하고, wording pass는 그 뒤에 한다.

Acceptance: 의미 손실 없이 instruction/context 비용이 감소한다.

## Work 7 — Generated projection / validation

대상: `route/skills.jsonl`, PR #239

- 최종 `SKILL.md` frontmatter 기준으로 repository 공식 generator를 실행해 route를 동기화한다.
- changed files formatting, source/frontmatter validation, deterministic tests, projection validation, Rulesync validation을 가능한 범위에서 실행한다.
- semantic review는 responsibility, activation, routing, context, granularity, package, regression 축으로 다시 수행한다.
- runtime behavioral eval을 실행하지 않으면 그 사실을 명시한다.

Acceptance: PR Gate deterministic blocker가 해소되고, remaining limitation이 실제 evidence 수준으로 기록된다.
