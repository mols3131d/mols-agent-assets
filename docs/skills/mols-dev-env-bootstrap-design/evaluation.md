---
description: mols-dev-env-bootstrap-design의 positive·near-miss routing과 설계 인계 behavior를 로컬 모델로 평가하고 실제 bootstrap 검증과 구분할 때 사용하는 계약입니다.
---

# Bootstrap Design Evaluation

이 Skill의 [case fixture](../../../evals/skills/mols-dev-env-bootstrap-design/cases.json)가 behavioral contract를 소유하며, [Promptfoo config](../../../evals/promptfoo/mols-dev-env-bootstrap-design.yaml)는 기존 [공통 evaluator](../../../scripts/agent_assets/skills_promptfoo.py)에 연결한다. 별도 Skill 전용 provider나 grader는 만들지 않는다.

## What this measures

| Suite | Input | Criteria |
| --- | --- | --- |
| Trigger | 사용자 요청 + canonical Skill frontmatter만 | 설계·리뷰 요청 3개의 selection, 일반 package update·단일 도구 설치·CI-only 요청 3개의 rejection |
| Behavior | 사용자 scenario + full canonical Skill | portable owner, bounded update, host/HOME 권한, 부분 실패, dirty state와 플랫폼 evidence를 설계 인계에 반영 |

Trigger는 expected selection과 deterministic하게 비교하며 Skill body를 제공하지 않는다. Behavior는 activation을 이미 마친 상태로 보고 output contract와 case별 semantic rubric을 평가한다. Rubric은 관찰할 수 있는 응답을 평가하며 실제 도구 실행이나 HOME 변경 여부를 증명하지 않는다.

이 suite는 **capability 평가**다. 작은 단일 trial의 성공률을 regression gate나 다른 model/runtime의 보장으로 사용하지 않는다. Negative 요청에서 해당 Skill을 선택하지 않는 것은 의도한 성공이지 평가 누락이 아니다.

## Run locally

이미 사용 가능한 Ollama 모델을 선택한 뒤 repository root에서 실행한다. 기본 runtime/grader 이름에 해당하는 모델이 설치되어 있다고 가정하지 않는다.

```bash
npm run eval:promptfoo:mols-dev-env-bootstrap-design
```

`PROMPTFOO_RUNTIME_MODEL`과 `PROMPTFOO_GRADER_PROVIDER`를 명시하고, 필요하면 `-- --filter-metadata suite=trigger` 또는 `suite=behavior`로 분리한다. 네트워크 모델 다운로드는 이 평가의 자동 선행 작업이 아니다. 현재 공통 runner가 선택한 Promptfoo version·local/no-sharing 설정을 재사용한다.

## Evidence and limitations

2026-10-25에 로컬 Ollama와 Promptfoo 0.122.0으로 실제 runtime을 실행했다. 첫 `qwen2.5-coder:7b` trigger trial은 positive 3/3, near-miss 0/3이었다. Broad topic keyword가 별도 activation처럼 읽히지 않도록 canonical description의 lifecycle-design 조건을 좁혔다.

수정 후 같은 모델의 10-case capability run은 trigger positive 3/3, near-miss 0/3, behavior 2/4였다. Missing-host/HOME 및 dirty-state/platform scenario에서 구체적인 처분을 빠뜨렸으며, description refinement만으로 routing 문제가 해결됐다고 주장하지 않는다.

같은 case·Skill·Promptfoo harness에서 runtime만 `nemotron-3-nano:4b`로 바꾸고 grader `ollama:chat:qwen2.5-coder:7b`를 유지한 trial은 trigger 6/6, behavior 3/4, 전체 9/10이었다. Exact-pin case의 응답은 setup/update 분리와 pin 유지를 명시했는데 grader reason은 이를 누락했다고 잘못 설명했다. 다만 응답에 lock diff 검토·검증·복구 인계가 없어 세 번째 criterion은 충족하지 못하므로 이 case를 pass로 덮어쓰지 않는다. Model마다 routing/행동 성능이 다르며 전체 capability gap이 해소됐다는 결론은 내리지 않는다.

- Model runtime output과 model-grader 판정은 별개의 evidence다. 비어 있거나 parse되지 않은 output은 transport/schema 문제인지 먼저 구분한다.
- Common evaluator fixture projection test와 Rulesync structural validation은 이 runtime 결과를 대신하지 않는다.
- 실제 Windows/macOS/Linux/WSL bootstrap, HOME installer containment, native Skill discovery/harness selection은 이 isolated prompt capability suite의 측정 대상이 아니다.
- 재현 가능한 실패는 capability gap으로 남긴다. Expected answer를 바꾸거나 near-miss를 제거해서 통과율을 올리지 않는다.
