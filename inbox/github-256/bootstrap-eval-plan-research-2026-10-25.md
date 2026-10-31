# PR #256 — 모델 Eval 연구 기록 (Research v1)

> 2026-10-25 · [Prepare](bootstrap-eval-plan-prepare-2026-10-25.md) 후속 · 실제 실행 없이 repository 원본/기존 기록을 조사함.

## 실증 질문과 직접 근거

| 질문 | 관찰된 계약·근거 | 판정 |
| --- | --- | --- |
| 평가 대상은 무엇인가 | [한국어 Skill](../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md), [11건 fixture](../../evals/skills/mols-dev-env-bootstrap-design/cases.json), [Promptfoo YAML](../../evals/promptfoo/mols-dev-env-bootstrap-design.yaml) | verified |
| 입력과 판정은 어떻게 나뉘나 | `skills_promptfoo.py`에서 trigger=frontmatter/candidate metadata만, behavior=이미 선택된 full Skill. Trigger는 JSON 구조+정답 선택의 결정론적 검사, Behavior는 응답 존재 검사+LLM rubric 3문항/건 | verified |
| 기존 case 분포 | activation 3, activation-negative 3, behavior 5 = 합계 11. 영어 요청 포함; 각 behavior는 3개 영어 판정 기준 포함 | verified |
| 실제 실행기는 무엇인가 | `package.json`의 `npm run eval:promptfoo:mols-dev-env-bootstrap-design` → `uv run --locked --no-default-groups --group test ...promptfoo_run.py` → npx `promptfoo@0.122.0` | verified |
| 로컬 사전조건 | Node >=22.22.0, npx, uv/Python test-group, Ollama HTTP API, 실행 모델과 채점 모델. 기본값은 `PROMPTFOO_RUNTIME_MODEL=qwen2.5`, `PROMPTFOO_GRADER_PROVIDER=ollama:chat:qwen2.5`이나 **모델이 실제 설치됐음을 뜻하지 않는다** | verified |
| 저장소가 데이터 전송을 막는가 | runner가 Promptfoo telemetry/update/remote generation/sharing 비활성 기본값을 부여하고 프로젝트 `.tmp/promptfoo`에 로컬 state 배치. 설정 YAML은 sharing=false, writeLatestResults=false, cache=false, write=false, noShare=true, maxConcurrency=1 | verified (설정) / 외부 영향은 실행 전 확인 |
| 과거 평가 | [evaluation.md](../../docs/skills/mols-dev-env-bootstrap-design/evaluation.md): 구형 영문/10건, Qwen 7B trigger 3/6, behavior 2/4; Nemotron Nano 4B trigger 6/6, behavior 3/4. Grader 오판도 기록 | verified (이전 기록), **현재 Skill 성능으로 환산 불가** |
| 실제 GitHub CI | 최근 PR Gate·Branch Check 성공은 fixture/projection·구조 검사에 관한 근거로만 해석. Ollama 실제 동작 실행 보장 아님 | verified (구분) |
| 제공되는 도구와 격리 | 평가 어댑터는 Ollama `/api/chat`으로 JSON 응답 요청; Skill 시나리오가 설치나 파일 변경을 서술해도 호스트 provisioning을 실행하지 않음. 모델 답변의 제안이 안전한지 평가하는 **텍스트 기반 실험** | verified |

## 유의할 함정 / 반증 방향

1. **모델 부재**: runner 기본 모델명은 설치 증명이 아니다. `ollama list`와 로컬 서비스 접근성, 선택 모델·grader 존재를 사전 확인하고 없으면 설치를 자동 수행하지 않는다.
2. **npx 부작용**: `npx --yes promptfoo@0.122.0`은 캐시가 없다면 설치/네트워크를 수반할 수 있다. `--yes`를 사용자 사전 승인으로 오해하지 않는다. 실행 계획에서 비용·설치 경계 확인 필요.
3. **grader 편향**: rubric은 영어 문장, Skill은 한국어. grader는 영어/한국어 응답을 공정하게 해석하는지 확인해야 하며, 과거 기록에서 grader reasoning 오류를 인정한 전력이 있다.
4. **전문 평가와 실제 설치의 차이**: 실제 Git/uv/HOME 변화는 테스트하지 않는다. '설치하지 않겠다는 응답'은 실제 non-mutation 증거가 아니다.
5. **선택 평가의 한계**: `_routing_candidates`가 빈 배열이면 대상 Skill 단독 후보로 구동될 수 있다. 실제 다중 Skill 환경과 같은 자동 선택이라고 일반화하지 않는다.
6. **단일 trial 불안정**: 의미 판정 0.8 임계값은 결과 해석 보조일 뿐. PASS 하나 또는 FAIL 하나로 Skill 전체를 합격/불합격 처리하지 않는다.

## 결론 / 다음 전이

- 실행 경로와 fixture는 이미 마련되어 있으므로 **새 provider/runner/test framework 필요 없음**.
- **계획 전이:** 사전조건 확인 → 기존 11건 실행(선택·행동 분리) → raw output/채점 근거 검토 → 실패 원인 분류 → 필요할 때만 제한된 재실행 → 문서화.
- **Review 후보:** 설치 승인과 실행 격리 조건, grader calibration 및 실제 native selection과 격리된 metadata selection의 차이를 더 좁은 하위 문제로 검토해야 한다.
- **미확인:** 로컬 사용자의 모델 설치 목록·현재 Ollama 가동 상태·캐시 상태, 실제 평가에 사용할 runtime/grader 최종 선택. 계획에서 사전 확인으로 해결한다.

## 소스 안내

- `scripts/agent_assets/skills_promptfoo.py`: `generate_tests`, `_ollama_request`, `_route`, `_execute_behavior`, `assert_trigger`
- `scripts/agent_assets/promptfoo_run.py`: 버전·Node 사전조건, `npx --yes`, state/telemetry
- `docs/development/evaluation.md`: Eval/Validation 분리, 과도한 fixture 방지, grader calibration, capability/CI 정책
