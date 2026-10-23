# mols-test-design — 구현·검증 리뷰

- PR: [#255](https://github.com/mols3131d/mols-agent-assets/pull/255)
- 검토 범위: 신규 `SKILL.md`, `evals/skills/mols-test-design/cases.json`, `docs/skills/mols-test-design/`, generated distribution Skill route
- 참고: [심층 조사](research-agentic-testing.md), [중첩 oracle 조사](research-oracle-validation.md), [설계 인계](research-loop-review.md)
- 단계: **구현·정적 검증**, 실제 model/runtime eval 및 repository-native CI 검증은 별도

## Review 1 — 계약·책임·선택 경계

**확인한 점**

- 핵심 owner는 software test의 claim, oracle, failure discrimination, 수준 선택·신뢰성 판단이다. CI 실행 시점·merge gate·Agent Asset eval의 다른 owner를 대체하지 않는다.
- 현재 구현/테스트 통과를 oracle의 유일한 근거로 취급하지 않고, 신뢰할 만한 specification/reference와 중요한 반례를 우선한다.
- 정답을 확정할 수 없는 경우 gap/assumption을 드러낸다. 불필요한 테스트 추가, 모든 변경에 TDD나 mutation, 다수 에이전트를 의무화하지 않는다.
- 일반 코드 구현, test-runner debugging, CI와 model-eval-only near-miss를 `description`에서도 구분한다.
- 배포 파일은 `SKILL.md` 하나이고 프로젝트 경로, 특정 언어·프레임워크, sibling Skill을 hard dependency로 갖지 않는다.

**반례/위험 검토**

- **Test writing과 design의 경계:** '주어진 assertion을 Jest 코드로 바꿔줘'처럼 전략 판단이 없는 요청은 별도 test-design activation이 실익 없다. 단 테스트 코드 작성 중 oracle 선택/테스트 수준을 결정해야 한다면 보조적으로 적용할 수 있다.
- **No-new-test 선택:** 표면적인 검사 추가를 의무화하지 않는다. 기존 evidence가 해당 변경을 충분히 보호할 때 재사용을 허용한다.
- **High-risk API/DB:** mock call만 확인하는 unit test를 최종 consumer-observable 계약으로 확대하지 않는다.

**Disposition:** 핵심 contract에 대한 material conflict는 발견하지 못했다. 실제 routing precision·behavior quality는 fixture로만 정의되었고 미실행이다.

## Review 2 — 이식성·비용·증거 진실성

**확인한 점**

- 별도 reference/문서 router/runner/framework를 deployable Skill에 추가하지 않았다.
- 연구 결과는 유지보수·inbox 문서에 남기고 Skill 본문에 논문/벤치마크 수치나 repo-specific 절차를 주입하지 않았다.
- fixture는 positive 5, negative 6, behavior 10, 총 21개. 사례는 잘못된 oracle, feature completeness, 실제 integration boundary, flaky fixture, no-new-test, 실행 불가를 구별한다.
- `route/skills.jsonl`은 기존 30개 엔트리를 바꾸지 않고 정본 Skill metadata에서 신규 엔트리를 생성·정렬했다. 기존 행의 JSON 렌더링을 동등하게 재현하는지 확인했다.

**정적 검사 실행 결과**

| 검사 | 상태 | 근거 |
| --- | --- | --- |
| Skill entrypoint/frontmatter, target 선언, 1,024자 이하 description | PASS | GitHub 브랜치 원본을 직접 읽어 범위 확인. Description 507자 |
| Route의 canonical metadata 일치 및 이름 정렬 | PASS | 31개 route entry; 신규 description/source 일치 |
| Eval JSON parsing/schema 기본 구조, ID uniqueness | PASS | 21개 사례, ID 중복 없음, positive/negative selection shape 및 behavior assertion 확인 |
| Maintainer docs frontmatter 및 Skill의 타 Asset hard dependency 없음 | PASS | 두 maintainer 문서 및 Skill 정적 확인 |
| 해당 repo의 `mise run test` | NOT RUN | 이 Chat runtime에는 repository-native test 환경을 재현한 working tree가 없음 |
| `npm run rulesync:validate`, `mise run generated-validate` | NOT RUN | 원본 Rulesync/mise 실행 및 전 저장소 projection 판정은 수행하지 않음 |
| 실제 trigger/behavior model eval, A/B baseline | NOT RUN | 적합한 runtime/harness·grader의 실제 실행 근거 없음 |
| GitHub `PR Gate` | PASS (commit `f824a78b`) | [run 39958075540](https://github.com/mols3131d/mols-agent-assets/actions/runs/39958075540)에서 source, deterministic tests, affected projections, Rulesync validation 성공 |

검사 표의 PASS는 **명시된 좁은 static subset만** 증명한다. 그 결과로 전체 repository correctness, target compatibility, LLM selection/uplift를 주장하지 않는다.

## 남은 실질적 작업

1. 동일한 model/runtime 조건에서 `mols-coding-context`만 사용한 baseline과 test-design Skill 추가를 비교한다. Oracle 유효성, 중요한 결함 검출력, 불필요한 테스트와 비용을 함께 보며 hidden grade 누출을 피한다.
2. 해당 검증은 GitHub PR Gate에서 통과했다. 이후 head가 변경되면 **새 head/merge candidate 기준 PR Gate 성공을 다시 확인**한다. 동일 실행을 로컬에서 수행했다고 주장하지 않는다.
3. CI 오류가 발생하면 근거를 분리해 수정하고 Draft 해제 전에 최신 head 기준 결과를 다시 확인한다.

**Review decision:** 현재 canonical Skill 설계·fixture 준비에 대한 static review는 통과 후보이며, 관찰된 commit `f824a78b`의 PR Gate도 PASS다. **PR은 계속 Draft** — runtime A/B uplift는 미검증이고 이후 commit의 CI 성공은 별도로 확인해야 한다.
