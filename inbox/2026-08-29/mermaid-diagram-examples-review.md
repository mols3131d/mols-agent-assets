# Mermaid Diagram Examples Review

`src/rulesync/.rulesync/skills/mols-mermaid-diagram/references/examples/`를 한 번에 전부 수정하지 않고, **최대 5개씩 batch로 진행하되 각 파일은 독립적으로 `리뷰 → 개선 → 재리뷰`**한다.

각 파일은 **깊은 추론**을 기본으로 `mols-rpi` Skill의 Research → Plan → Implementation → 재귀 Review 루프를 적용해 고도화한다. 단순 문법 확인이나 1회성 리뷰로 완료하지 않고, 내부 원칙과 upstream 근거를 교차 검토하며 새로운 근거가 판단을 실질적으로 바꾸지 않을 때까지 반복한다.

## 원칙

- 현재 진행 cursor를 따라 최대 5개를 한 batch로 묶는다. 끝에 도달하면 남은 미완료 파일을 `examples/README.md`의 질문별 인덱스 순서로 이어간다.
- Batch는 작업 단위일 뿐 판단 단위가 아니다. 각 파일의 Research → Plan → Implementation → Review를 독립적으로 순차 수행하고 여러 파일을 하나의 공통 결론으로 처리하지 않는다.
- 파일별 완료 여부는 개별 RPI 수렴으로 판단한다. 같은 batch의 다른 파일이 미완료여도 수렴한 파일만 체크할 수 있다.
- 최신 Mermaid 공식 문법과 target renderer 책임을 확인한다.
- `mols-rpi`에 따라 조사, 계획, 구현과 반례 중심 재리뷰를 재귀적으로 수행한다.
- syntax catalog를 복제하지 않고 local design judgment만 남긴다.
- semantic fidelity, layout ≠ semantics, portability, viewport composition을 공통 기준으로 적용한다.
- 완료는 깊은 RPI 루프가 수렴하고 `리뷰 → 개선 → 재리뷰`가 끝난 파일만 체크한다.

## TODO

### 절차·분기·ownership
- [x] `flowchart.md`
- [x] `swimlanes.md`

### message order
- [x] `sequence-diagram.md`
- [x] `zenuml.md`

### lifecycle
- [x] `state-diagram.md`

### domain model·schema
- [x] `class-diagram.md`
- [x] `er-diagram.md`

### architecture·boundary
- [x] `architecture-diagram.md`
- [x] `c4-diagrams.md` — `c4-context.md`에서 rename
- [x] `block-diagram.md`

### chronology·planning·work
- [x] `timeline.md`
- [x] `gantt.md`
- [x] `git-graph.md`
- [x] `kanban.md`

### hierarchy·experience·requirements
- [x] `mindmap.md`
- [x] `tree-view.md`
- [x] `user-journey.md`
- [x] `requirement-diagram.md`

### specialized relationship·sensemaking
- [x] `packet-diagram.md`
- [x] `event-modeling.md`
- [x] `venn.md`
- [x] `ishikawa.md`
- [x] `wardley.md`
- [x] `cynefin.md`

## Current

- 진행: **24/24 완료**, 파일별 심층 RPI 수렴 완료
- Batch 운영: 최대 5개씩 진행, 파일별 RPI는 독립·순차 수행
- 완료: `architecture-diagram.md`
- 완료: `c4-diagrams.md` — 리뷰 → 개선 → 재리뷰 완료
- 완료: `block-diagram.md` — 심층 RPI 완료; 공식 docs·11.17.2 parser/layout tests·release history·open layout issue·local design principles 교차 검토
- 완료: `timeline.md` — 추가 심층 RPI 완료; 공식 docs·11.17.2 DB/tests/LR·TD renderer·develop renderer·11.14/11.17 release·upstream issue를 교차 검토하고 temporal precision뿐 아니라 order uncertainty, visual connector semantics, repeated section, event-density coupling, long-title width와 TD actual-render gate까지 재검증
- 완료: `gantt.md` — 심층 RPI 완료; Mermaid 11.17.2 docs/parser/DB/tests, 11.16–11.17 release와 current Gantt issues/PRs를 교차 검토하고 implicit sequencing, reference resolution, working calendar, schedule uncertainty, milestone/status/criticality, renderer-sensitive acceptance를 재설계
- 완료: `git-graph.md` — 심층 RPI 완료; Mermaid 11.17.2 docs/AST/renderer/tests, Git merge·cherry-pick 공식 semantics와 current upstream issues를 교차 검토하고 synthetic history boundary, stable identity, branch point/declaration order, merge-mode fidelity, cherry-pick ancestry caveat, temporal/parallel layout과 current-ref boundary를 재설계
- 완료: `kanban.md` — 심층 RPI 완료; Mermaid 11.17.2 docs/parser/DB/renderer/tests, current Kanban styling/parser issues와 Kanban Guide를 교차 검토하고 snapshot completeness, Definition of Workflow boundary, flat column→card model, visual ordering, metadata honesty, styling safety와 viewport split을 재설계
- 완료: `mindmap.md` — 심층 RPI 완료; Mermaid 11.17.2 docs/parser/DB/tests, current layout-default issue와 local design principles를 교차 검토하고 decision/process 오용 제거, single-root/tree fidelity, multiple-root split, indentation safety, shared identity boundary, decomposition consistency와 layout-semantic separation을 재설계
- 완료: `tree-view.md` — 심층 RPI 완료; Mermaid 11.17.2 docs/parser/DB/renderer/e2e, box-drawing implementation, current root behavior·upstream issues와 local design principles를 교차 검토하고 literal-tree scope/completeness, virtual `/` root, file-directory identity, structural input, annotation semantics, order/layout와 viewport fallback을 재설계
- 완료: `user-journey.md` — 심층 RPI 완료; official docs·11.17.2 parser/DB/renderer를 교차 검토하고 1–5 score evidence, actor optionality·single-task score, activity-line semantics, phase/order honesty와 quantitative fallback을 재설계
- 완료: `requirement-diagram.md` — 심층 RPI 완료; official docs·11.17.2 Jison/DB/tests와 current renderer-direction issue를 교차 검토하고 declaration/display ID 분리, endpoint resolution, typed traceability, direction/render acceptance와 coverage completeness를 재설계
- 완료: `packet-diagram.md` — 심층 RPI 완료; official docs·11.17.2 parser/tests를 교차 검토하고 contiguous bit arithmetic, fixed/variable boundary, reserved-gap honesty, row-wrap semantics, bit numbering·byte order와 excerpt fallback을 재설계
- 완료: `event-modeling.md` — 심층 RPI 완료; official docs·11.17.2 grammar/validator/DB/tests와 current namespace/data-render issues를 교차 검토하고 timeframe identity, declaration-order inference, reset/source control, entity-type source validation, namespace·data renderer sensitivity를 재설계
- 완료: `venn.md` — 심층 RPI 완료; official docs·11.17.2 parser/DB/renderer와 current text/many-set issues를 교차 검토하고 `union`≠set union, set identity, size/population honesty, higher-arity synthetic pairwise layout, text/density와 quantitative fallback을 재설계
- 완료: `ishikawa.md` — 심층 RPI 완료; official docs·11.17.2 Jison/DB/tests를 교차 검토하고 effect/cause authority, raw indentation hierarchy, hypothesis/evidence, category discipline, one-effect boundary와 renderer layout semantics를 재설계
- 완료: `wardley.md` — 심층 RPI 완료; Wardley Mapping source와 Mermaid 11.17.2 parser/DB/builder/tests를 교차 검토하고 user/need anchor, value-chain dependency, `[visibility,evolution]`, stable identity, evolve/sourcing/inertia, pipeline·scenario·viewport semantics를 재설계
- 완료: `cynefin.md` — 심층 RPI 완료; Cynefin current framing·Mermaid official docs·11.17.2 DB/renderer와 upstream framework-correction issues를 교차 검토하고 contextual sense-making, Aporetic↔`confusion` notation boundary, repeated-domain data loss, transition identity, fixed placement·overflow·self-loop semantics를 재설계
- 완료: `flowchart.md` — 심층 RPI 완료; Mermaid official Flowchart docs와 local diagram principles를 교차 검토하고 dominant edge semantics, stable identity, decision honesty, subgraph semantic/layout boundary, external-edge direction limitation, overview/detail fidelity, shape·animation 의미 경계를 재설계
- 완료: `swimlanes.md` — 심층 RPI 완료; official docs·11.17.2 layout-variant implementation과 current upstream churn을 교차 검토하고 Flowchart semantic reuse, one partition criterion, lane membership/decision authority, cross-lane handoff, direction/lane-order presentation과 beta render gate를 재설계
- 완료: `sequence-diagram.md` — 심층 RPI 완료; official docs·11.17.2 sequence DB와 current parser issues를 교차 검토하고 participant/message identity, interaction order, fragment behavior, activation, autonumber와 split fidelity를 재설계
- 완료: `zenuml.md` — 심층 RPI 완료; official docs·11.17.2 external adapter/no-op parser·`@zenuml/core` renderer와 current issues를 교차 검토하고 sync/async/creation/reply, nesting/control flow, visible comments, fallback fidelity와 actual-render acceptance를 재설계
- 완료: `state-diagram.md` — 심층 RPI 완료; official State docs와 current renderer/layout issues를 교차 검토하고 state/process boundary, initial/final scope, choice/fork/join, composite-state scope와 overview/detail fidelity를 재설계
- 완료: `class-diagram.md` — 심층 RPI 완료; official Class docs와 current generic issues를 교차 검토하고 stable class identity, UML relation strength, multiplicity, generic identity, member excerpt와 namespace boundary를 재설계
- 완료: `er-diagram.md` — 심층 RPI 완료; official ER docs와 current parser issue를 교차 검토하고 grain, cardinality, identifying/non-identifying relation, label perspective, key/nullability, attribute excerpt와 input-safety gate를 재설계
- 다음: **24개 example 전체 package 최종 리뷰 및 PR 수렴 검증**
