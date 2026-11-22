<!--
Keep Summary, Goal, Tasks, Checklist, and Boundaries as the five required H2 sections, in order.
Split a long H2 into descriptive H3 subsections when distinct topics or workstreams make it easier to scan; otherwise omit H3. Keep the two fixed Checklist H3 groups. Keep the optional Documentation H3 only when relevant.
Remove unused optional sections, empty headings, placeholders, and authoring comments before submitting.
-->

## Summary

<!-- Summarize the outcome; link a related Issue or task when one exists. -->

## Goal

<!-- State the problem, intended outcome, and success criteria. Avoid repeating the Tasks list. -->

## Tasks

<!-- Track concrete deliverables using - [ ] and - [x]. Check only completed work. Group longer task lists under descriptive H3 headings when helpful; do not duplicate the changed-files list or commit history. -->

## Checklist

<!-- Keep the fixed checks below. Check only a criterion that was actually satisfied. Keep failed, pending, or unverified checks unchecked and explain why. For an inapplicable check, replace its entire checkbox item with a plain Markdown bullet in the form `- N/A: <reason>` (for example, `- N/A: no runtime behavior to verify`); do not use any checkbox syntax for N/A because it affects GitHub task progress. Add relevant checks as needed without copying CI logs. -->

### Self-review

- Reviewed HEAD: Pending

<!--
Review the full current PR diff on first review, when the previous reviewed SHA is unavailable,
or when the base changes. Otherwise, review changes since the recorded SHA and their
impact on the full PR diff, Goal, and Boundaries. After review, replace Pending with
the full reviewed commit SHA.
-->

> [!WARNING]
> Self-review is valid only for the recorded `Reviewed HEAD`. After every push, you must uncheck the Self-review items, review the changes, and update the checks and `Reviewed HEAD`.

- [ ] Confirmed the Goal and Boundaries against the current PR diff.
- [ ] Reviewed new changes since the last reviewed HEAD (or the full diff on initial review) for unintended changes and regressions.
- [ ] No blocking findings from self-review remain.

### Verification

- [ ] Task-specific acceptance criteria and runtime/manual behavior verified where applicable.

### Documentation

<!--
선택 항목: 문서가 변경되거나 실질적인 영향을 받을 때만 이 H3 전체를 남깁니다.
목적: 사람과 AI 에이전트가 필요한 정보를 효율적으로 찾고 이해하며,
정확한 판단과 행동으로 이어지도록 합니다. 불필요한 맥락·탐색·추론·
검증·재작업 비용을 줄이되 문서 길이나 토큰 수 자체의 최소화를 목표로 하지 않습니다.
실제로 확인한 항목만 체크하고 미충족 항목에는 사유를 남깁니다.
-->

- [ ] **목적과 독자:** 문서의 역할과 대상 독자가 명확하며, 필요한 이해·판단·행동을 지원한다.
- [ ] **정확성과 완전성:** 사실·계약·제약·근거를 보존하고 변경된 정본과 일치시켰다.
- [ ] **맥락·토큰 비용:** 중복·장황함을 제거하고 필요한 정보만 선택적으로 읽을 수 있도록 구성했다.
- [ ] **탐색 비용:** 정보의 위치·책임·연결 관계가 명확하여 필요한 정본에 쉽게 도달할 수 있다.
- [ ] **추론 비용:** 전제·조건·관계·판단 기준을 명확히 하여 불필요한 추론과 재확인을 줄였다.
- [ ] **가독성과 유지보수성:** 핵심 정보가 우선 제시되고 구조·표현이 명료하며, 향후 변경에도 불필요한 중복 관리가 발생하지 않는다.

## Boundaries

<!-- Record material exclusions, unverified work, unresolved risks, constraints, permissions, side effects, or follow-up work; use N/A when none apply. -->

<!-- Optional: add useful H2 sections such as Risks, Review Focus, Compatibility, Migration, Security, Handoff, or References. Omit empty sections. Add descriptive H3 subsections only when they improve readability. -->
