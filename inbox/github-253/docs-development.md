# Docs Development — Consistency Findings

## Finding DOC-001 · Verified · Low

**관찰:** [언어 정책](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/language.md)의 `Scope` 표는 Markdown H1–H3 제목 언어를 **영어**로 지정한다. 그러나 [`docs/development/source-authority.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/source-authority.md)에는 `# 작성 원본과 권한`, `## 원칙`, `## 책임별 권한` 등 동일 범위의 한국어 제목이 있다. [`docs/using-this-repository.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/using-this-repository.md)의 `# 이 저장소 사용하기` 및 여러 H2도 같은 현상을 보인다.

**영향:** 명시된 문서 언어 규칙과 실제 문서가 다르므로 동일 종류 문서의 작성·검수 기준을 일관되게 적용하기 어렵다. 의미나 실행 동작의 충돌은 확인되지 않았다.

**반증 확인:** 언어 정책의 `Non-Scope`에는 관리 대상 Agent Asset, framework/tool convention, literal 및 generated text가 있으나 위 두 문서는 일반 repository 문서다. 예시·코드 블록의 literal을 문제로 판정한 것이 아니다.

## Other Inspected Relations

[`docs/development/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/README.md)의 authority routing, [`github.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/github.md)의 작성·PR 규칙, [`ci.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/ci.md)의 PR/branch 분리, [`validation.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/validation.md)의 generated output 책임을 관련 source와 표본 대조했다. **추가 verified finding 없음.** 실제 Ruleset enforcement, CI 실행은 별도 검증 대상이다.
