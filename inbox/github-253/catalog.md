# Catalog — Consistency Findings

## Finding DOC-003 · Resolved · Low

**관찰:** [`docs/language.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/language.md)는 H1–H3 Markdown heading에 영어를 요구한다. [`catalog/patterns/workflow/chatbot-driven-development.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/patterns/workflow/chatbot-driven-development.md)에는 `## 목표를 어떻게 구체화할까?`, `### 무엇을 질문하고 무엇을 위임할까?`, `## 완료는 어떤 근거로 판단할까?` 등의 한국어 H2–H3가 존재한다.

**영향:** canonical pattern 문서 작성 관행과 명시된 언어 정책의 적용이 어긋난다. Pattern의 설명 내용이 틀리거나 workflow contract를 강제한다는 의미는 아니다.

**반증 확인:** [`catalog/patterns/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/patterns/README.md)에 따르면 pattern은 reusable reference capsule이며 managed executable Agent Asset이 아니다. 언어 정책의 Agent Asset 비적용 예외로 자동 분류하지 않았다.

**수정:** [`chatbot-driven-development.md`](../../catalog/patterns/workflow/chatbot-driven-development.md)의 H2–H3 제목 7개를 영어로 변경했다. 추가 점검에서 같은 유형을 발견한 [`executable-output-checks.md`](../../catalog/patterns/software-engineering/executable-output-checks.md)와 [`durable-progress-handoff.md`](../../catalog/patterns/workflow/durable-progress-handoff.md)의 H2–H3 제목도 각각 14개, 13개 수정했다. 패턴 본문과 예시는 보존했다.

## Other Inspected Relations

[`catalog/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/README.md), [`skills.json`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/skills.json), [`plugins.json`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/plugins.json), [`patterns/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/patterns/README.md), [`workflow/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/patterns/workflow/README.md), [`artifact-inbox-work-unit-containers.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/catalog/patterns/workflow/artifact-inbox-work-unit-containers.md)의 discovery/authority 구분을 확인했다. **추가 검증된 모순 없음.**

## Coverage Limits

외부 catalog source URL의 최신 유효성·installer별 지원을 검증하지 않았다. 다른 pattern category를 전수 점검하지 않았다.
