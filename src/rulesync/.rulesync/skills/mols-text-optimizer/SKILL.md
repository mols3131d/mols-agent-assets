---
name: mols-text-optimizer
description: >-
  Use this Skill to reduce wording cost in provided or clearly identified text while preserving material meaning, behavior, exact technical content, and existing structure. Apply only as a generic fallback when no more specific Skill, instruction, document/domain guidance, framework contract, or procedure governs the target or task. Trigger on meaning-preserving shortening, compression, deduplication, or requests to reduce token footprint. A more specific owner takes precedence even when this Skill is named explicitly. Do not use for response brevity, summarization, translation, grammar/style/humanization, Markdown/document restructuring, caveman-style speech, or latent context compression.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Text Optimizer

의미와 기능을 보존하면서 불필요한 표현 비용만 줄인다.

## Optimize Wording

안전한 국소 수정부터 한다.

1. 의미 없는 반복과 군더더기를 제거한다.
2. 같은 핵심 의미를 중복한 표현을 줄인다.
3. 사용자가 정한 용어와 표준 도메인 용어는 유지하고 불필요한 용어 변형만 정리한다.
4. 의미 범위와 행동 효과가 같을 때만 더 짧은 표현을 쓴다.
5. 명확하게 안전한 절감이 더 없으면 멈춘다.

모든 단계를 억지로 수행하지 않는다. 안전한 절감이 없으면 원문을 유지한다. 의미 안정성은 별도 확장 목표가 아니라 축약의 제약이다.

Tokenizer가 지정되지 않았거나 실제 token count를 확인할 수 없으면 표현 비용만 줄이고 정확한 token 절감량을 주장하지 않는다. 사용자가 별도 설명을 요청하지 않았다면 최적화한 텍스트만 반환하고 새 머리말이나 설명을 덧붙이지 않는다.

## Preserve Meaning and Behavior

다음 요소는 축약보다 우선해 보존한다.

- **역할과 효과** — 주체, 행동, 대상, 입력/출력, 부수 효과, 실패 동작
- **논리와 제어** — 조건, 예외, fallback, 순서, 의존성, 범위, 인과·논리 관계
- **강도와 불확실성** — 부정, 금지, 의무·권고·허용 강도, 수량자, 불확실성, 비교
- **정확한 사실과 기술 토큰** — 수치, 임계값, 단위, 날짜, 이름, 식별자, 경로, 명령, API, field, code token, exact error string, 인용과 출처 연결
- **에이전트 행동** — 선택·활성화 조건, 권한·허용, 안전 경계, 필수 gate와 stop condition

에이전트용 텍스트에서는 반복 자체가 행동에 영향을 줄 수 있다. 같은 표현이 반복된다는 이유만으로 보호 규칙이나 지침을 제거하지 않는다.

## Protect Structure

이 Skill은 문서나 출력 구조를 최적화하지 않는다. 기존 section과 heading hierarchy, 문장·문단 경계와 순서, list/table/callout/numbering 표현, code fence·delimiter·indentation, JSON/YAML/XML/schema-like structure와 exact format contract를 유지한다.

전체 결과물을 반환해야 하더라도 실제 최적화 대상 밖의 내용을 넓게 다시 쓰지 않는다.

## Check and Stop

변경한 구간과 판단에 필요한 주변 맥락만 한 번 확인한다.

- 핵심 정보가 빠졌는가?
- 주체, 행동, 대상, 조건, 예외, 범위, 순서나 관계가 바뀌었는가?
- 부정, 의무·허용 강도, 수량자나 불확실성이 바뀌었는가?
- 정확한 기술 토큰, 식별자, 수량, 임계값이나 단위가 바뀌었는가?
- 에이전트의 선택 조건, 권한, 안전 경계나 행동이 달라질 수 있는가?
- 보호해야 할 구조를 변경했는가?

하나라도 확실하지 않으면 해당 변경을 되돌리거나 원문을 유지한다. 남은 변경이 문체 선호 수준이거나 절감보다 검토 비용이 크면 추가 반복 없이 끝낸다.

## Boundary

이 Skill은 범용 표현 비용 절감만 담당한다. 대상별 작성 규칙, 일반 응답 간결화, 정보를 줄이는 요약, 번역, 문법 교정, humanization, tone/persona, Markdown·문서 재구성, caveman-style speech, latent context compression, tokenizer algorithm은 담당하지 않는다.
