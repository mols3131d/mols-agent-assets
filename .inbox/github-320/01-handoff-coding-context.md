# Implementation Guidance 작업 인계

[PR #320](https://github.com/mols3131d/mols-agent-assets/pull/320)의 통합 설계는 [유지보수 문서](../../docs/skills/mols-implementation-guidance/guidance.md)에 기록한다. 실행 지침은 단일 Skill 및 Python Reference가 소유한다. 기존 [정적 리뷰](00-review-coding-context.md)는 당시 revision의 기록이다.

- [ ] 최종 HEAD의 PR Gate와 실제 모델 routing Eval 결과 확인. 로컬 실행: `mise run eval -c evals/promptfoo/mols-implementation-guidance.yaml`.
- [ ] 변경된 지침에 의존하지 않는 최종 독립 리뷰와 사람의 머지 승인.

실제 Reference 로딩과 결과물 개선은 routing Eval의 범위 밖이다. 외부 소비자 이관 및 레거시 호환 처리는 사용자 결정에 따라 이번 작업에서 제외한다.
