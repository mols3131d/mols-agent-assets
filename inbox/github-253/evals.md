# Evals — Consistency Findings

## Finding DOC-003 · Verified · Low

**관찰:** [`docs/language.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/language.md)의 H1–H3 heading 언어 규칙은 영어인데 [`evals/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/evals/README.md)의 첫 제목은 `# 평가 (\`evals/\`)`다.

**영향:** eval 안내 README가 repository-wide Markdown 제목 규칙과 불일치한다. eval 계약이나 실행에 기능상 오류가 있음을 뜻하지 않는다.

**반증 확인:** `evals/README.md`는 README형 일반 안내 문서이며 Agent Asset 원문이나 vendor-native/generated 파일이 아니다.

## Other Inspected Relations

[`evals/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/evals/README.md)의 Trigger/Behavior/Smoke 구분과 [`docs/development/evaluation.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/development/evaluation.md), [`docs/skills/mols-loops/evaluation.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-loops/evaluation.md), [`mise.toml`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/mise.toml), [`package.json`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/package.json)의 실행 진입점 표기를 대조했다. **추가 확인된 모순 없음.**

## Coverage Limits

Promptfoo config/cases의 모든 조합과 실제 provider·grader 실행은 확인하지 않았다.
