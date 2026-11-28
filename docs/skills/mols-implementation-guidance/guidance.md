---
description: mols-implementation-guidance의 설계 의도와 지침 채택·제거 및 평가 기준을 확인할 때 사용합니다.
---

# Implementation Guidance

[Skill 원본](../../../src/rulesync/.rulesync/skills/mols-implementation-guidance/SKILL.md)은 구현 과정의 엔지니어링 판단 오류를 줄인다. 실행 절차를 소유하지 않는다. 언어별 판단은 독립 Skill 대신 조건부 Reference로 두어 별도 선택과 관리 책임을 만들지 않는다.

## Maintenance

- 모델·기존 자산·결정적 도구로 충분히 해결되지 않는 반복적 실패나 비용이 큰 판단 위험에 근거해 지침을 채택한다. 일반 지식, 도구의 기계적 규칙, 저장소 정책 및 전문 workflow는 복제하지 않는다.
- 언어 독립적 판단은 Core에, 고유한 실행 의미와 계약은 해당 언어 Reference에 둔다. 실익이 사라진 지침은 제거하며 압축 시 조건과 예외를 보존한다. 파일 길이만으로 추론 비용 절감을 주장하지 않는다.
- 필요한 시점에만 Reference를 읽고 유효한 컨텍스트를 재사용한다. 런타임 호출 횟수를 강제하지 않는다.

## Evaluation

[평가 정책](../../development/evaluation.md)에 따라 자동 Eval은 Skill 선택·비선택만 검사한다.

```bash
mise run eval -c evals/promptfoo/mols-implementation-guidance.yaml
```

Reference 로딩·재사용과 결과물 품질은 routing 결과로 증명되지 않는다. 본문은 정적 리뷰와 실제 사용에서 확인한 오류·결과를 근거로 개선한다.

## References

- [pstack (Lauren Tan)](https://github.com/cursor/plugins/tree/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack) — domain modeling, premise checking, shared state, contract-oriented testing, failure boundaries, reader load, measurement 및 피드백·보호 장치 판단. [MIT license](https://github.com/cursor/plugins/blob/9e278fe4d4ecd8bfe98b1b79bf4be662efb338cc/pstack/LICENSE).
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — 모델 발전에 따른 절차형 지침과 컨텍스트 과잉 재검토.
