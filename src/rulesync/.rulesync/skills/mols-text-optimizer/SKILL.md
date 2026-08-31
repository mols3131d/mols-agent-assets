---
name: mols-text-optimizer
description: >-
  Optimize provided or clearly identified text for lower wording or token cost while preserving material meaning, behavior, exact technical content, and the existing structure. Use only as a generic fallback when no more specific applicable Skill, instruction, document or domain guidance, framework contract, or procedure applies to the target or task. Trigger on requests to shorten, compress, or deduplicate wording without losing meaning. Do not use when a more specific owner applies, even if this Skill is named explicitly. Also do not use for generic response brevity, summarization, translation, style or humanization, Markdown or document restructuring, caveman-style speech, or latent prompt/context compression.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Text Optimizer

의미와 기능을 보존하면서 불필요한 wording 비용만 줄인다.

## Optimize Wording

안전한 local edit부터 적용한다.

1. 의미 없는 반복과 filler를 제거한다.
2. 같은 material meaning을 중복해서 표현한 local phrase를 줄인다.
3. canonical user/domain term은 유지하면서 불필요한 term variation을 정리한다.
4. 의미 범위와 behavioral effect가 같은 경우에만 더 짧은 wording을 사용한다.
5. 명확하게 안전한 절감이 더 없으면 멈춘다.

모든 단계를 억지로 수행하지 않는다. 안전한 절감이 없으면 원문을 유지한다. Semantic stability는 별도 확장 목표가 아니라 reduction의 제약이다.

## Preserve Meaning and Behavior

다음 요소는 compression에 강하게 보존한다.

- **역할과 효과** — actor, action, target, input/output, side effect, failure behavior
- **논리와 제어** — condition, exception, fallback, order, dependency, scope, causal/logical relation
- **강도와 불확실성** — negation, prohibition, modality, permission, quantifier, uncertainty, comparison
- **정확한 사실과 token** — number, threshold, unit, date, name, identifier, path, command, API, field, code token, exact error string, citation, attribution
- **agent behavior** — activation, permission, safety boundary, required gate, stop condition

Agent-facing text에서는 반복 자체가 behavior에 영향을 줄 수 있다. 같은 표현이 반복된다는 이유만으로 guard나 instruction을 제거하지 않는다.

## Protect Structure

이 Skill은 문서나 출력 구조를 최적화하지 않는다. 기존 section과 heading hierarchy, sentence/paragraph boundary와 순서, list/table/callout/numbering 표현, code fence·delimiter·indentation, JSON/YAML/XML/schema-like structure와 exact format contract를 유지한다.

전체 artifact를 반환해야 하더라도 실제 optimization candidate 밖의 내용을 넓게 다시 쓰지 않는다.

## Check and Stop

변경한 span과 판단에 필요한 주변 context만 한 번 확인한다.

- material information이 빠졌는가?
- actor, action, target, condition, exception, scope, order, relation이 바뀌었는가?
- negation, modality, permission, quantifier, uncertainty가 바뀌었는가?
- exact technical token, identifier, quantity, threshold, unit이 바뀌었는가?
- agent-facing activation, permission, safety, behavior가 달라질 수 있는가?
- protected structure를 변경했는가?

하나라도 확실하지 않으면 해당 변경을 되돌리거나 원문을 유지한다. 남은 변경이 style preference이거나 절감보다 검토 비용이 커지면 추가 pass 없이 끝낸다.

## Boundary

이 Skill은 범용 wording-cost reduction만 담당한다. Target-specific text-authoring rule, generic response brevity, information-reducing summarization, translation, grammar-only correction, humanization, tone/persona, Markdown/document restructuring, caveman-style speech, latent context compression, tokenizer algorithm은 담당하지 않는다.
