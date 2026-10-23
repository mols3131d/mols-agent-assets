# Test Design Improvement Loop — Oracle Validation

- PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)
- 목적: [research coverage review](review-research-coverage.md)의 F1–F6를 기존 portable Skill의 최소 책임 변경으로 해결
- 범위: `mols-test-design` 본문, **필요 시 읽는 하나의 reference**, 해당 behavioral fixtures, maintainer 평가 설명, source-derived route metadata
- 이 작업은 `mols-loops`의 Research → Plan → Work → Review를 사용하며 **실제 다중·독립 서브에이전트 호출은 수행하지 않았다.**

## Loop 1 — Research → Plan → Work → Review

**Research:** 현재 core는 '구현을 정답으로 복제하지 말라'와 '중요한 결함이 테스트에서 실패해야 한다'를 명시하지만, 테스트가 **허용된 정상 동작까지 실패시키는 잘못된 oracle**을 분리하지 않는다. 테스트가 실패했을 때 곧바로 제품 코드를 수정하거나 테스트 자체를 바꾸는 것도 근거가 부족하다. 구현 요청에 실질적 테스트 설계가 포함된 mixed intent에는 activation 문구가 모호했다.

**Plan:** F1, F2, F3의 공통 판단을 SKILL.md에 짧게 반영. F4 관찰/재현 seam과 F5 requested deliverable/위험 기반 stop은 기존 항목의 확장으로만 처리. Conditional deeper logic은 [Oracle validation](../../src/rulesync/.rulesync/skills/mols-test-design/references/oracle-validation.md) 하나에 둔다. 두 번째 boundaries/isolation reference와 framework별 사용법은 보류.

**Work:**
- 모든 테스트가 지켜야 할 **정상 수용 / 실제 결함 거부**의 양방향 기준과 요구된 산출물·연결 계약 확인
- 실패 시 **제품 / oracle·test / fixture·runner·환경**의 원인 후보를 구분한 뒤 수정 책임 판단
- 관찰할 수 없거나 재현할 수 없을 때 범위가 좁은 testability seam 제안, 아키텍처 재설계 금지
- 실제 구현 요청에도 material test design subtask가 있으면 선택 가능함을 discovery description에 반영, 일반 구현·runner debugging은 제외
- reference는 oracle이 의심되거나 증거를 더 강화해야 할 때만 읽으며 일반 테스트 설계에는 읽지 않음
- 34개 기존 fixture 유지, 11개 신규 near-miss/behavior 사례 추가 → **45개(positive 10, negative 10, behavior 25)**

**Review 1 — concrete finding:** reference의 최초 로딩 설명은 **테스트 실패/의심스러운 기대값**에만 명시적으로 걸려 있어 '정상 동작은 명확하지만 강한 결함 반례가 필요한' 상황에서 optional reference route가 빠져 있었다. **Disposition: absorb.** `SKILL.md`에 *불확실하거나 충돌하는 oracle, 중요한 결함을 더 강한 반례로 검증해야 하는 경우에만*이라는 조건을 명확히 했다. 일반 사례에서 자동으로 reference를 읽지 않도록 보존.

## Loop 2 — adversarial Review & validation

| Lens | Stress case | Review judgment |
| --- | --- | --- |
| Correctness | Mutation score가 높아도 정상 reference를 거부 | **Pass by static design**: 두 방향의 oracle 판정과 잘못된 기대값 교정 우선. Behavior 실측은 아직 없음 |
| Truthfulness | 환경 timeout과 계산 오류가 섞인 test fail | **Pass by static design**: 수정 전 product/test/runner 후보 분리. 재현 없는 PASS 주장 금지 |
| Ownership | 구현과 함께 테스트 설계를 요청 | **Pass by static design**: material test design subtask에는 선택, 일반 구현에는 미선택 |
| Portability | 일반 테스트에도 모든 연구·framework 가이드를 로드 | **Pass by static design**: core 약 3.5k자, conditional reference 약 4.9k자, vendor/Skill hard dependency 없음 |
| Negative counterexamples | 단순 arithmetic helper, 불필요한 full suite, Pact/framework cookbook | **Reject**: 레퍼런스·복잡한 도구를 항상 사용하는 계약 아님 |
| Architectural boundary | 관찰 불가능한 scheduler timeout에 대한 강제 구조 변경 | **Pass by static design**: testability 개선을 제안할 수 있으나 아키텍처 변경 자체는 별도 owner |
| Maintainability | oracle 내용을 2개 reference로 중복 분리 | **Reject**: 이전 independent testability 설계는 core와 기존 18개 fixture로 충분; 두 번째 reference는 효용 입증 전까지 보류 |

### Narrow static validation

- `SKILL.md`의 7 targets와 metadata, distribution route description/source parity, 정렬 및 31개 canonical Skill 엔트리 확인
- `references/oracle-validation.md` 링크와 경로 존재 확인; 일반 테스트 설계에서 의무 로딩하는 조건 없음
- 45개 fixture의 JSON 구조, 고유 ID 및 positive 10 / negative 10 / behavior 25 분포 확인
- portable package에 다른 mols Skill, 프로젝트 경로, 특정 test tool/runtime에 대한 하드 의존성 없음
- maintainer 문서 frontmatter와 source-vs-maintainer ownership 확인
- **이 검사는 정적 구조·지침 점검이다. 실제 모델 selection/behavior, reference loading 여부 또는 개선율을 측정하지 않았다.**

## Remaining evidence & Finalize boundary

1. 현재 **source 변경 revision**의 GitHub PR Gate에서 source contracts, deterministic tests, affected projections, Rulesync validation 성공 확인.
2. runtime이 제공되는 환경에서는 `mols-coding-context` 단독 baseline과 추가 Skill의 실제 routing/behavior를 같은 model/harness/tool/context budget에서 비교. 새 평가 사례의 oracle false rejection, test triage, required deliverable 누락과 near-miss를 중점 채점.
3. reference 로딩률과 문맥·지연 비용이 관찰되면 실제 유용성 재평가: 사소한 테스트 설계에서 상시 읽힌다면 core로 흡수하거나 삭제할 것.
4. 그 결과 전에는 '테스트 설계 성능이 향상됐다'고 주장하지 않으며 PR은 **Draft**, merge하지 않는다.

**Review disposition:** material instruction gaps는 정적 설계상 해결했다. 두 번째 reference 등 비입증 확장은 제외했다. **CI 및 model-eval evidence boundary는 별도로 확인**한다.
