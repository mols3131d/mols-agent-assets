# Mermaid Diagram Examples Review

`src/rulesync/.rulesync/skills/mols-mermaid-diagram/references/examples/`를 한 번에 전부 수정하지 않고, **파일 하나씩 `리뷰 → 개선 → 재리뷰`**한다.

## 원칙

- 현재 `examples/README.md`의 질문별 인덱스 순서를 따른다.
- 한 번에 한 파일만 다룬다.
- 최신 Mermaid 공식 문법과 target renderer 책임을 확인한다.
- syntax catalog를 복제하지 않고 local design judgment만 남긴다.
- semantic fidelity, layout ≠ semantics, portability, viewport composition을 공통 기준으로 적용한다.
- 완료는 `리뷰 → 개선 → 재리뷰`가 끝난 파일만 체크한다.

## TODO

### 절차·분기·ownership
- [ ] `flowchart.md`
- [ ] `swimlanes.md`

### message order
- [ ] `sequence-diagram.md`
- [ ] `zenuml.md`

### lifecycle
- [ ] `state-diagram.md`

### domain model·schema
- [ ] `class-diagram.md`
- [ ] `er-diagram.md`

### architecture·boundary
- [x] `architecture-diagram.md`
- [x] `c4-diagrams.md` — `c4-context.md`에서 rename
- [x] `block-diagram.md`

### chronology·planning·work
- [x] `timeline.md`
- [ ] `gantt.md`
- [ ] `git-graph.md`
- [ ] `kanban.md`

### hierarchy·experience·requirements
- [ ] `mindmap.md`
- [ ] `tree-view.md`
- [ ] `user-journey.md`
- [ ] `requirement-diagram.md`

### specialized relationship·sensemaking
- [ ] `packet-diagram.md`
- [ ] `event-modeling.md`
- [ ] `venn.md`
- [ ] `ishikawa.md`
- [ ] `wardley.md`
- [ ] `cynefin.md`

## Current

- 완료: `architecture-diagram.md`
- 완료: `c4-diagrams.md` — 리뷰 → 개선 → 재리뷰 완료
- 완료: `block-diagram.md` — 심층 RPI 완료; 공식 docs·11.17.2 parser/layout tests·release history·open layout issue·local design principles 교차 검토
- 완료: `timeline.md` — 심층 RPI 완료; 공식 docs·11.17.2 DB/tests/LR·TD renderer·11.14 direction release를 교차 검토하고 chronology·temporal precision·section·causality 경계를 재설계
- 다음: `gantt.md` 리뷰
