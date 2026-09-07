# CI redesign research

이 문서는 `mols-agent-assets`의 CI를 다시 설계하기 전에 현재 repository의 변경 경로, 검증 표면, projection, GitHub enforcement와 외부 GitHub Actions semantics를 조사한 기록이다. 설계 결정은 `design.md`에서 별도로 다룬다.

## Research question

이 repository는 local Git만으로 변경되지 않는다. `gh` CLI, GitHub API, MCP, ChatGPT/GitHub Plugin, web UI와 coding agent가 remote branch를 직접 수정할 수 있다.

따라서 조사 질문은 단순히 “PR Gate에서 무엇을 실행할 것인가?”가 아니다.

> 어떤 write path로 변경이 만들어져도 repository contract를 잃지 않으면서, branch 단계에서 빠르게 문제를 발견하고 `main` admission에서는 필요한 근거를 빠짐없이 확보하려면 현재 어떤 검증 표면과 도구를 재사용할 수 있는가?

## Current integration surfaces

### GitHub Actions

현재 workflow는 두 개뿐이다.

| Surface | Trigger | Role |
| --- | --- | --- |
| `.github/workflows/targeted-tests.yml` | `pull_request` → `main` | required `PR Gate`; `pytest -q tests` 전체 실행 |
| `.github/workflows/optional-validation.yml` | `workflow_dispatch` | docs frontmatter/index, Agent Asset routes, Rulesync validation을 선택 실행 |

`PR Gate`는 `contents: read`이고 PR merge ref를 checkout한 뒤 test dependency만 설치한다. 별도 formatting, named source validation, projection stage는 없다.

`Optional Validation`은 더 세분화되어 있다. 특히 Agent Asset route 검증은 공식 generator를 실제 실행한 뒤 `route`와 `.agents/route`의 working-tree 변경을 검사한다. 이 형태는 projection freshness를 pytest assertion보다 직접적으로 보고한다.

### Local hooks

`lefthook.yml`은 local Git 경로에 다음 보조 검증을 둔다.

```text
pre-commit
→ scripts.generated_artifacts_sync --staged

commit-msg
→ commit_message_validate.py

pre-push
→ pytest -q tests
```

`pre-commit`은 영향받는 projection을 자동 생성하고 stage한다. 그러나 GitHub Contents API, MCP, Plugin, web UI 같은 remote mutation에는 local hook이 존재하지 않는다.

따라서 local hook은 조기 feedback/maintenance surface이지 repository-wide correctness boundary가 될 수 없다.

### Repository-native entrypoints

`mise.toml`은 이미 재사용 가능한 entrypoint를 제공한다.

- `mise run generated-sync` — committed docs indexes와 routes 재생성
- `mise run test` — root deterministic tests
- `mise run check` — toolchain/lock/selected config checks
- `mise run format-changed` — changed/untracked 파일 write-format
- `mise run format` — repository-wide write-format

Rulesync structural validation은 `npm run rulesync:validate`가 소유한다.

현재 formatting entrypoint는 write-oriented이며 CI에서 그대로 실행할 read-only formatting contract는 별도 정의되어 있지 않다.

## Projection model

`scripts/generated_artifacts_sync.py`는 세 projection을 하나의 registry로 관리한다.

| Projection | Canonical input | Output | External network |
| --- | --- | --- | --- |
| docs indexes | `docs/**/*.md`, index tooling | `docs/**/INDEX.tsv` | 없음 |
| distribution routes | canonical Rulesync skills/subagents | `route/*.jsonl` | 없음 |
| repository routes | locks, Rulesync config, skills lock, route families | `.agents/route/*.jsonl` | 있음 |

Repository route generator는 pinned GitHub dependency의 raw `SKILL.md`를 `urlopen`으로 가져온다. 즉 전체 projection regeneration은 순수 local/deterministic filesystem 작업만은 아니며 외부 GitHub availability에 의존한다.

이 차이는 branch feedback과 authoritative PR validation의 배치에서 중요하다. 값싼 local projection drift와 network-backed projection verification을 같은 빈도로 강제할 필요는 없다.

## Test and validation overlap

현재 root test suite에는 generator 자체의 동작 test와 일부 committed projection freshness assertion이 함께 존재한다.

대표적으로 `tests/scripts/agent_assets/test_routes_distribution_generate.py`의 `test_committed_distribution_routes_are_current`는 committed route가 generator output과 같은지 pytest assertion으로 확인한다.

이 구조는 correctness를 잡기는 하지만 failure class를 숨길 수 있다. PR #222에서는 새 canonical Skill을 추가한 뒤 generated `route/skills.jsonl`이 누락되었고, PR Gate는 이를 정상적으로 차단했지만 거대한 JSON assertion diff로 보고했다.

반면 `Optional Validation`의 route check는 generator 실행 후 changed path를 직접 출력한다. 같은 실패를 더 진단 가능하게 표현한다.

따라서 다음 책임은 분리 가능하다.

- generator parsing/ordering/failure/output semantics → deterministic tests
- committed projection freshness → projection generation + comparison

## Write-path model

이 repository에서 고려해야 할 변경 경로는 다음과 같다.

| Write path | Local hook 기대 가능 | Server-side branch state 생성 |
| --- | --- | --- |
| local Git commit/push | 가능하지만 설치/환경 의존 | 예 |
| `gh` CLI | 명령 방식에 따라 다름 | 예 |
| GitHub Contents/API | 아니오 | 예 |
| GitHub MCP / Plugin / connector | 아니오로 간주 | 예 |
| GitHub web UI | 아니오 | 예 |
| coding agent / automation | runtime마다 다름 | 예 |

Tool별 quality standard를 만들 이유는 없다. 중요한 것은 persisted branch state가 동일한 repository contract로 수렴하는가이다.

API/MCP/Plugin path가 자주 사용되는 이 repository에서는 PR이 생성되기 전 remote branch 상태도 실제 작업 feedback surface다. 현재는 open PR이 없으면 GitHub Actions 검증이 전혀 없다.

## GitHub enforcement

현재 `protect-main` Ruleset은 다음을 강제한다.

- default branch 삭제 금지
- non-fast-forward 금지
- linear history
- Pull Request 필요
- squash merge만 허용
- unresolved review thread 해소
- required status check: `PR Gate`
- bypass actor 없음

따라서 `main` admission의 server-side enforcement point는 이미 명확하다. Branch validation을 추가해도 required `PR Gate`를 대체할 이유가 없다.

## GitHub Actions semantics relevant to the design

현재 GitHub 공식 문서에서 확인한 사항:

### `pull_request` validates the merge candidate

Open, mergeable PR의 `pull_request` workflow는 기본적으로 `refs/pull/<number>/merge`를 사용하고 `actions/checkout`도 그 merge ref를 checkout한다. 현재 PR Gate의 merge-candidate validation 방식은 이 동작과 일치한다.

Source: <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request>

### `push` and `pull_request` together create separate runs

한 workflow가 두 event를 모두 구독하면 각각 독립적으로 trigger된다. Open PR의 head branch에 push하면 branch feedback과 PR validation을 동시에 두었을 때 중복 실행이 생길 수 있다.

Source: <https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow>

중복 자체가 correctness 문제는 아니다. 이를 제거하기 위해 PR lookup, cross-workflow state나 복잡한 routing을 추가하는 비용이 실제 실행 비용보다 큰지 따져야 한다.

### Required workflows should not be workflow-level path-skipped

Required status check를 제공하는 workflow가 path/branch filter나 skip annotation 때문에 실행되지 않으면 associated check가 Pending으로 남아 merge를 막을 수 있다.

Source: <https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks>

따라서 required `PR Gate` 자체에 workflow-level path filtering을 넣는 방식은 적합하지 않다. 필요하면 workflow는 항상 실행하고 job/step 내부에서 안전하게 scope를 줄여야 한다.

### Concurrency can cancel superseded runs

`concurrency` + `cancel-in-progress: true`는 같은 logical change의 이전 실행을 취소하는 표준 수단이다. 현재 PR Gate도 PR number 단위로 이를 사용한다.

Source: <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency>

### `pull_request_target` is not a general solution for immutable trusted CI

`pull_request_target`는 base repository의 privileged context에서 실행되며 untrusted PR code를 checkout/execute하면 위험하다. 이 repository의 test/generator는 PR content를 실행·import하므로 일반 PR validation을 `pull_request_target`로 옮기는 것은 안전한 기본값이 아니다.

Source: <https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target>

Workflow/control-surface 변경의 독립 검토 문제는 repository policy와 human approval로 다루고, privileged event로 우회하지 않는 편이 안전하다.

## Cost observations

현재 Python test dependency는 작고 root suite는 매우 빠르다. PR #222에서 226 tests는 약 1.14초에 실행되었다. 현재 규모에서는 pytest selection/router를 새로 만드는 것보다 전체 deterministic test를 반복 실행하는 편이 더 단순할 가능성이 높다.

반대로 Rulesync validation은 Node + Rulesync 설치가 필요하고 repository route projection은 external GitHub fetch를 수행한다. 이 둘은 Python-only deterministic suite와 같은 비용/신뢰성 tier로 취급하지 않는 편이 합리적이다.

## Findings

### F1. PR Gate는 correctness boundary로는 작동하지만 integration lifecycle 전체를 다루지 않는다

현재 remote branch push 자체에는 server-side feedback이 없다. Hookless API/MCP/Plugin write는 PR이 열릴 때까지 projection drift나 source-level 문제를 발견하지 못할 수 있다.

### F2. Local hook과 server-side validation의 책임이 비대칭이다

Local pre-commit은 projection sync를 수행하지만 PR Gate는 named projection gate를 가지지 않는다. Local path가 더 많은 maintenance 지식을 갖고 있다.

### F3. Projection freshness가 generic test에 섞여 있다

Generator correctness와 committed projection freshness가 pytest 안에서 일부 중첩된다. 실패 검출은 되지만 diagnosis와 ownership이 약하다.

### F4. 모든 projection은 같은 비용이 아니다

Docs index와 distribution route는 local generation이지만 repository route는 external GitHub fetch가 필요하다. Branch feedback에서는 이 차이를 활용할 수 있다.

### F5. Formatting은 현재 CI-ready read-only contract가 없다

Repository formatter는 write task로 정의되어 있다. Pure style을 blocking evidence로 만들지 여부도 별도 정책 판단이 필요하다. Parseability/explicit representation contract와 단순 style preference를 구분해야 한다.

### F6. Full deterministic tests의 최적화 필요성은 현재 낮다

Test runtime이 매우 짧아 impact router나 test matrix를 도입할 근거가 부족하다. Setup/extra tool installation이 오히려 비용의 큰 부분이다.

### F7. Required PR Gate는 항상 보고되는 단일 admission check로 유지하는 편이 안전하다

현재 Ruleset이 `PR Gate` 하나를 require하고 있고 GitHub의 skipped-required-check semantics를 고려하면, required workflow 자체는 항상 실행되는 구조가 단순하고 안전하다.

### F8. Workflow 변경은 self-validation 한계를 가진 control-surface 변경이다

`pull_request`는 PR merge branch의 workflow를 사용하므로 workflow 변경은 수정된 workflow가 자기 자신을 검증하는 성격을 갖는다. Repository의 기존 GitHub policy가 요구하는 independent evidence와 explicit human approval을 유지해야 한다.

## Constraints passed to design

설계 단계에서는 다음을 제약으로 취급한다.

1. `main`의 authoritative admission은 required `PR Gate`로 유지한다.
2. Local hook은 correctness prerequisite가 아니라 optional acceleration이다.
3. API/MCP/Plugin/web/agent remote writes를 first-class change path로 취급한다.
4. Remote branch update에 early server-side feedback surface가 필요하다.
5. PR Gate는 merge candidate를 검증하고 workflow-level path skip을 사용하지 않는다.
6. Verification workflow는 기본 read-only이며 repository write-back을 하지 않는다.
7. Existing validators, generators, tests와 `mise` entrypoint를 재사용하고 CI YAML에서 semantics를 재구현하지 않는다.
8. Generator behavior test와 committed projection freshness check를 분리한다.
9. Network/tool-heavy checks는 merge-criticality가 증명되지 않으면 값싼 branch feedback과 동일한 빈도로 실행하지 않는다.
10. 현재 test 규모에서는 impact router, matrix, cache complexity를 새로 정당화하지 않는다.
11. Pure formatting preference와 explicit representation contract를 구분한다.
12. Workflow/control-surface 변경에는 수정된 CI 자체 외의 review evidence와 explicit human approval이 필요하다.

## Research conclusion

현재 문제는 “PR Gate가 약하다” 하나가 아니다. **Local-only maintenance knowledge, hookless remote writes, PR-only server validation, projection/test ownership 중첩**이 함께 존재한다.

다음 설계는 CI를 최소 세 surface로 보아야 한다.

```text
local feedback
→ remote branch validation
→ authoritative PR admission
→ deferred/manual evidence when justified
```

각 surface의 구체적인 check와 실행 순서, projection tier, formatting boundary, workflow 구조는 다음 설계 단계에서 결정한다.
