# CI · Lefthook 품질 게이트 개선 인계

## 목표

로컬 코딩 에이전트의 Lefthook은 빠른 피드백을, GitHub Actions는 **GitHub Plugin·API·웹 UI·클라우드 에이전트의 Hook 없는 변경까지 포함하는 독립 검증**을 맡는다. `main`에서 거부해야 할 오류는 required `PR Gate`에서 차단하고, 검사 선택·설치·실행 비용은 근거에 따라 최소화한다.

- **원칙:** Hook의 통과 여부를 서버 검증의 근거로 쓰지 않는다. Hook과 CI의 중복 제거는 허용하지만 당연히 최적이라고 가정하지 않는다.
- **비목표:** Hook 자동 설치, 일반 소스 자동 포맷·stage, CI commit/push, 유료 LLM 평가 상시화, 새 CI provider·거대 검사 라우터·OS matrix, Ruleset 무단 변경.
- **작업 상태:** 설계·인계 준비 단계. 구현, 변경된 검증 명령 실행, 개선 후 비용 측정은 아직 수행되지 않았다.

기준: `main` @ `c39d094f72cfb331217bc70abb303c738493dd4c`, 브랜치 `mols/chore/ci-lefthook-quality-gates`. 구현 시작 시 최신 ref와 이미 반영된 변경을 확인하되, 이 PR의 base를 승인 없이 변경하지 않는다.

## 현행 경계와 근거

| 실행면 | 현행 검증 | 한계 및 유지 사항 |
| --- | --- | --- |
| [Lefthook](../../lefthook.yml) | pre-commit의 staged projection sync, commit-msg validator, pre-push pytest | 로컬 Git에서 **설치된 경우에만** 동작; source 자동 포맷·stage 금지. staged 경로 선택과 실제 worktree/index 내용의 차이를 주의 |
| [Branch Check](../../.github/workflows/branch-check.yml) | non-main push의 frontmatter, pytest, 로컬 projection 3종 | 초기 피드백. 현재 uv만 설정하며 mise/rumdl/Biome은 준비하지 않음. 필수 merge gate는 아님 |
| [PR Gate](../../.github/workflows/pr-gate.yml) | main 대상 PR merge 후보의 frontmatter, pytest, 영향 projection, mise Doctor, Rulesync | required check 유지. 현재 mise는 `install: false` 후 Rulesync에 필요한 도구만 설치 |
| [mise](../../mise.toml), [pyproject](../../pyproject.toml) | Ruff·rumdl·Biome 버전과 formatter write task | Ruff는 `dev` group에만 존재; `test` group에서 사용 불가. `mise run check`는 전체 소스 린트가 아닌 도구/설정 진단 |
| [Projection selector](../../scripts/generated_artifacts_sync.py) · [validator](../../scripts/generated_artifacts_validate.py) | Git 변경 경로를 네 projection에 매핑, git diff 실패 시 전체 검사 | 공통 제어 코드 변경은 매핑되지 않을 수 있음. `--local-only`는 네트워크 의존 repository route 검사를 제외 |
| [Ruleset](https://github.com/mols3131d/mols-agent-assets/rules/21094860) | required `PR Gate`, squash-only, 리뷰 대화 해결 | 승인 리뷰 0개, strict-base 비활성. 운영 정책 검토 사항이며 이번 PR에서 설정 자동 변경 금지 |

기준 실행: [Branch Check](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710194442), [PR Gate](https://github.com/mols3131d/mols-agent-assets/actions/runs/43710198355) 성공. 단일 실행에서 약 12초/29초가 관측되었을 뿐, 새 검사나 비용 개선의 증거는 아니다.

### Authoring 경로별 동작

| 경로 | Hook | 서버 검증 |
| --- | --- | --- |
| 로컬 Git·코딩 에이전트 | 설치 상태에 따라 실행 | push: **head** Branch Check; PR: **merge candidate** PR Gate |
| ChatGPT GitHub Plugin·Contents API·웹 UI | 실행되지 않음 | 정상 push/PR 이벤트 발생 시 동일한 CI 적용. 실제 run 생성 및 required check 상태를 확인 |
| 클라우드 자동화 | 미보장 | 사용 토큰·이벤트 종류에 따라 실행 여부 확인. **`GITHUB_TOKEN` push는 후속 Actions 실행을 유발하지 않음**; `GITHUB_TOKEN`에 의한 특정 PR 이벤트는 승인 대기 실행이 될 수 있음 |

GitHub 공식 근거: [GITHUB_TOKEN의 workflow trigger 예외](https://docs.github.com/en/actions/concepts/security/github_token), [PR merge ref의 SHA 의미](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows). 원격 쓰기 성공이나 agent의 검증 진술을 CI 실행 증거로 간주하지 않는다. 권한을 늘리거나 다른 토큰을 사용하여 이벤트를 강제하는 변경은 자동으로 도입하지 않는다.

## 실패 → 최소 검증 근거

| 실패 유형 | Merge admission | 실행 위치 |
| --- | --- | --- |
| Python·generator·validator 동작 회귀 | 차단 | pytest: PR Gate 필수; Branch Check의 조기 피드백은 비용 비교 후 선택 |
| Frontmatter·source 계약 오류 | 차단 | 기존 validator; 로컬·branch·PR 중 적절한 조기 검사 |
| INDEX/route 산출물 drift, 영향 매핑 실패 | 차단 | PR merge 후보에서 공식 checker; 선택 불가 시 fail-safe 확대. Branch는 local projection 유지 |
| Rulesync 관리 자산의 구조 불일치 | 차단 | 변경 영향에 필요한 strict doctor/dry-run; 기존 PR Gate 유지 |
| Ruff·rumdl·Biome 진단 | **분류 후 결정** | 명시한 안전·파싱·규약 위반만 PR blocking, 단순 스타일은 로컬 피드백/선택적 검사 가능 |
| Hook 설정 문법·실행 불일치 | 관련 변경 시 확인 | `lefthook validate` 및 필요한 동작 테스트. CI가 Hook을 설치/실행했다고 추정하지 않음 |
| LLM 동작/semantic | 변경 위험에 필요한 경우 별도 판단 | 기존 deterministic fixture만 PR 기본 대상, 모델 호출은 필요한 경우에만 한정 |
| commit-msg 규칙 | 추가 검토 | 현재 로컬 Hook만 검사. Plugin/API commit과 squash PR 제목의 적용 필요성을 먼저 확인하고 무조건 gate에 추가하지 않음 |

## 구현 순서와 계약

1. **기준선·검증 계약:** `mise.toml`, `.rumdl.toml`, `biome.json`, `pyproject.toml`과 기존 소스에서 read-only formatter/linter 결과를 확보한다. `ruff check`/`ruff format --check`, `rumdl check`/`rumdl fmt --check`, `biome format`(read-only) 및 필요시 `biome lint`/범위가 더 넓은 `biome check`를 구분한다. 실제 잠긴 버전의 지원 옵션을 확인한다. **기존 `biome format --write`와 신규 `biome check`를 동등하게 취급하지 않는다.** 적용 범위/강제 여부를 검증 규약별로 정하고 기존 전체 파일을 일괄 수정하지 않는다.
2. **Projection 선택기 보강:** `scripts/generated_artifacts_sync.py`의 공유 매핑을 재사용하면서 `scripts/generated_artifacts.py`, `scripts/generated_artifacts_validate.py` 등 공통 생성·판별 코드의 변경이 필요한 검사 대상으로 확산되게 한다. 경로 자체가 무관한 변경과 영향 판별 실패를 구별한다. `git diff` 실패의 현행 전체 fallback은 보존한다. source 삭제, output 삭제/변경, 공통 코드 변경과 영향이 없는 변경을 `tests/scripts/`에서 테스트한다.
3. **로컬 Hook:** 기존 projection sync/stage를 유지하고, 필요한 staged 파일 정적 검사를 빠르게 추가한다. 읽기 전용 원칙을 지키며 `stage_fixed`와 일반 파일 `git add`는 금지한다. **staged 파일 목록 ≠ index blob 내용**임을 전제로 부분 스테이징, unstaged 수정, 공백/비ASCII 경로, 삭제·이름 변경, 순서·실패 전파의 현재 동작을 확인한다. 인덱스 스냅샷 검사가 과도하면 Hook의 검증 한계를 명시하고 PR Gate의 committed tree 검증을 필수로 남긴다.
4. **서버 CI:** `Branch Check`와 `PR Gate`에서 필요한 정적 검사를 수행하도록 구성한다. Branch는 현재 uv만 있고, PR은 mise는 있으나 Ruff·rumdl·Biome이 준비된 상태가 **아니므로**, 필요한 `uv --group dev`와 pinned mise 도구의 설치 범위를 먼저 설계한다. 각 단계는 최소 권한(`contents: read`), `uv --locked`, read-only 검사를 유지한다. PR Gate의 merge ref/첫 부모 변경 범위와 required check 이름을 보존한다.
5. **중복 비용 판단:** Branch는 head, PR은 merge candidate를 실행하므로 둘을 단순히 "같은 SHA의 중복 테스트"로 간주하지 않는다. 실측 setup 시간·검사 시간·오류 조기 발견·merge 후보 독립성을 비교한다. branch pytest, Rulesync 설치, lint 반복 등은 **실제 이익이 있고 admission 기준이 유지될 때만** 줄인다. 조건부 path filter·추가 workflow·cache/matrix는 필요성이 확인되지 않으면 도입하지 않는다.
6. **정합성:** 정본 의미가 바뀐 문서만 [CI](../../docs/development/ci.md)·[Formatting](../../docs/development/formatting.md)·[Validation](../../docs/development/validation.md)·[Lefthook](../../docs/tools/lefthook.md) 등에 반영한다. 워크플로처럼 통제 표면을 변경한 PR은 별도의 독립 검토 근거와 사람의 명시적 merge 승인을 받는다. Ruleset의 사람 승인/최신-base 설정 변경은 이 PR 범위 밖이다.

## 완료 조건

- [ ] GitHub Plugin/API의 대표적인 Hookless commit → branch/PR run 증거를 확보한다. 로컬 Git·웹 UI·클라우드 자동화는 트리거 계약과 실제 검증된 범위를 구분한다. `GITHUB_TOKEN`의 미트리거·승인 대기 예외를 누락하지 않는다.
- [ ] Ruff·rumdl·Biome 검사 경로·도구 설치·적용 파일·차단 여부·실패 종료 코드가 구체적으로 검증된다. 기존 순수 스타일을 근거 없이 merge-blocking으로 바꾸지 않는다.
- [ ] 생성물 검사에서 공통 코드 변경·source/output 삭제·영향 판별 실패가 누락되지 않고, 무관한 변경은 불필요한 원격 설치를 일으키지 않는다.
- [ ] Hook은 일반 파일을 포맷·stage하지 않으며 부분 스테이징에서 false pass 여부와 한계를 명시한다.
- [ ] required `PR Gate`는 merge 후보·read-only 권한·lock 검증·기존 deterministic tests를 유지한다. 신규 검사 실패를 실제 Actions 또는 동등한 신뢰할 수 있는 독립 실행으로 확인한다.
- [ ] 유지/제거한 중복 검사는 measured cost와 evidence boundary로 정당화한다. 런타임·model 호출·새 provider는 불필요하게 추가하지 않는다.
- [ ] 관련 정본·구성·테스트의 변경 범위가 일관되며, 통제 표면 수정분은 수정된 검증에 의존하지 않는 리뷰와 사람의 명시적 승인 이후에만 merge한다.

## 인계

이 파일은 비정본 작업 계획이다. 실제 구현 전 [GitHub 정책](../../docs/development/github.md)과 해당 경로 `AGENTS.md`를 확인한다. 필요하면 `mols-ci-design` 및 `mols-loops`의 원본을 적용한다. PR의 체크박스는 **구현을 끝낸 항목만** 완료 처리한다. 실행하지 않은 테스트와 측정하지 않은 비용은 통과·개선으로 보고하지 않는다.
