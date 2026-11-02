# 개발 도구 실행 경로·진단 최적화 구현 계획

> 상태: 1차 구현·PR Gate 검증 완료, 추가 검토 중. 이 문서는 PR 진행 중의 작업 근거이며 저장소 정책이나 도구 설정의 정본이 아니다.

## 목표와 범위

`pyproject.toml`, `package.json`, `mise.toml`을 기준으로 개발·검증·평가 실행 경로를 단순화하고, 이미 제공되는 mise/uv/Rulesync 기능을 우선 사용한다. **같은 PR에서 실제 코드·설정 변경, 회귀 검증, 문서 정합성 수정까지 완료**하는 것이 목표다. 세션 진단과 신규 릴리스 발견은 서로 다른 비용·의미의 검사로 설계한다.

범위: `mise.toml`, `pyproject.toml`, `package.json`, `scripts/development_bootstrap.py`, 해당 범위의 `scripts/agent_assets/` 실행 래퍼, 관련 테스트·운영 문서 및 실행 경로가 바뀌는 기존 CI 호출부. 변경이 필요하지 않은 파일은 수정하지 않는다.

제외: 승인되지 않은 설치·업데이트, 실제 CLI 버전 대량 갱신, Promptfoo 평가 계약·모델 선택의 별도 재설계, Agent Asset 원본/프로젝션 일괄 수정, 자동 세션 Hook·상시 서비스·새 범용 프레임워크 도입, 자동 merge.

## 확인된 현황과 문제

1. `mise.toml`에서 uv/Node/rumdl/Lefthook/Biome/Rulesync/skills 7종을 exact pin 및 `mise.lock`으로 관리한다. `setup`은 CLI·Python 환경을 복구하고, `update`는 현재 Python 의존성만 갱신한다. 버전 범위 전환은 bootstrap이 아직 exact pin만 받으므로 별도 호환성 검증이 필요하다.
2. `pyproject.toml`은 런타임 dependencies가 비어 있고 `dev`가 `test` group을 포함한다. Python 의존성의 진짜 설치/잠금 정본은 uv/uv.lock이다. 여러 일반 task에서 `uv run`에 `--locked`가 누락되어 있고 일부 task는 기본 group 선택이 모호하다.
3. `package.json`은 npm dependencies 없이 scripts만 선언한다. `mise` 평가 task → `npm run` → `uv run` → `promptfoo_run.py` → `npx --yes promptfoo@0.122.0`으로 이어지는 다중 실행 계층이 있다. CI의 `npm run rulesync:validate`도 별도 소비자다.
4. npm은 단순히 `npm run`에서만 사용되는 것이 아니다. Biome·Rulesync·skills CLI는 mise의 `npm:` backend가 설치한다. Node.js와 npm backend의 필요성, package.json을 task runner로 사용하는 필요성은 분리해 판단한다. npm 제거를 목표로 삼지 않는다.
5. Promptfoo runner는 CLI 버전을 코드에 고정하나 `npx`로 해석되는 전이 의존성까지 완전히 lock하지 않는다. `PROMPTFOO_*` 설정·외부 provider·네트워크/쓰기 영향과 평가 비교 가능성을 보존해야 한다.
6. Promptfoo 평가 실행은 `mise.toml`에서 asset별 `eval-mols-*` task를, `package.json`에서 asset별 `eval:promptfoo:*` npm script를 반복 선언한다. 현재 차이는 주로 `-c` 설정 파일, `--filter-metadata suite=...`와 `--no-cache --no-write` 옵션이다. PR #272에는 Bootstrap 평가·grader 보정 별칭 2개가 더 추가되어 중복이 계속 증가한다. 실질적으로 독립된 작업 계약이 없다면 별칭을 새로 만들지 않는다.
7. `mise run check`의 버전 출력은 자체로 선언/실행 버전 일치 증명이 아니다. 전체 검증·가벼운 환경 진단·외부 최신성 조회가 구분되어 있지 않다.
8. **열린 PR #272**가 `mise.toml`, `scripts/agent_assets/promptfoo_run.py`, 관련 eval과 문서를 변경 중이다. 작업 전에 최신 head와 병합 상태를 다시 확인하고 변경을 덮어쓰지 않는다. 새 PR은 생성 시점의 main에서 독립적으로 시작한다.

## 네이티브 우선 검토와 결정 기준

| 문제 | 먼저 검토할 네이티브 기능 | 조건부 대안 |
| --- | --- | --- |
| 가벼운 개발 환경 진단 | `mise doctor project --json`와 `[doctor.checks]` | 설치된 mise가 미지원이거나 구조화 출력에 실질적인 빈틈이 있을 때만 얇은 보조 스크립트 |
| 도구 최신성 탐지 | `mise outdated --no-global --bump --json` | 실패·오프라인 시 UNKNOWN, 자체 release/SemVer 엔진 구현 금지 |
| 잠금·선택 버전 확인 | `mise ls --current --json`, `mise.lock`, `uv lock --check` | 정확한 실행 바이너리 확인이 필요하면 기존 bootstrap 검증을 재사용 |
| 작업 진입점 | `mise run` task 직접 호출 | npm scripts가 별도 소비자에게 실제로 필요한 경우만 보존 |
| Python 실행 | `uv run --locked`와 필요한 group 지정 | bootstrap setup/update만 승인된 재현·갱신 경계 유지 |
| Rulesync 진단 | `rulesync doctor --strict` 및 기존 검증기 | 경로·warning 정책 같은 실제 계약이 필요한 최소 래퍼 유지 |

### Promptfoo 평가 task 정리 결정

- **하나의 매개변수화된 진입점 우선:** 기존 `promptfoo_run.py`의 `eval` 인수를 재사용하며, `mise` task는 `raw_args = true`로 Promptfoo 네이티브 CLI 인수를 전달한다. 예: `mise run eval -c evals/promptfoo/mols-loops.yaml --filter-metadata suite=trigger`.
- **설정 선택은 Promptfoo가 소유:** `-c`, `--filter-metadata`, `--no-cache`, `--no-write`, grader 옵션 등을 mise에 중복 구현하거나 asset별 별칭으로 복제하지 않는다. 설정 파일·fixture가 평가 semantics를 소유한다.
- **별칭의 존치 기준:** 실제 외부 소비자/자동화의 안정적 인터페이스이거나, smoke·grader처럼 별도의 계약을 가진 경우에만 좁게 유지할 수 있다. 단순 편의를 위한 동일 옵션의 조합은 제거한다. 기존 문서/CI/사용자 진입점 전환·호환성 영향을 확인한다.
- **중요한 차이 보존:** `mols-test-design` 평가의 `--no-cache --no-write`와 smoke/실모델 평가 구분을 무시하지 않는다. PR #272가 추가한 `PROMPTFOO_RUNTIME_PROVIDER`·timeout·grader 설정 및 평가 프로토콜을 보존한다.
- **기본 실행이 의도치 않은 쓰기/모델 호출을 유발하지 않도록 검토:** 단일 `eval` 실행은 외부 API·결과 기록 가능성이 있으므로 세션 기본 `preflight`에 포함하지 않고, 사용자가 어떤 config를 실행하는지 명시해야 한다.
- **검증:** 전체/trigger/behavior/smoke/grader 사례의 CLI args, 선택 fixture, cache/write semantics, error/exit code, `.env` 전달을 회귀 테스트한다. 플랫폼별 인수 quoting과 실제 Promptfoo 버전에서 지원하는 옵션을 확인한다.

공식 참고: https://mise.jdx.dev/tasks/running-tasks.html · https://mise.jdx.dev/tasks/task-configuration.html · https://www.promptfoo.dev/docs/usage/command-line/

`mise doctor project`는 공식 문서에 존재하지만 현재 CI의 mise 설치 버전과 사용자 PC 버전에서 지원하는지는 미확인이다. 진단 명령도 shell을 실행하며 샌드박스가 아니므로 read-only 검사를 명시해야 한다. `uv run --locked`는 lock 변경을 막지만 환경 동기화까지 자동으로 비활성화하지 않으므로 '읽기 전용 세션 진단'에 무조건 사용하지 않는다.

공식 근거:
- https://mise.jdx.dev/configuration/project-diagnostics.html
- https://mise.jdx.dev/cli/outdated.html
- https://mise.jdx.dev/tasks/task-configuration.html
- https://docs.astral.sh/uv/concepts/projects/sync/

## 구현 순서

1. **호출 관계 및 기준선:** 실제 소비자(로컬 task, CI, pytest, eval, docs)를 모두 확인한다. 변경 전 Windows/Linux 경로, 기존 실패 상태, 설치/네트워크 부작용을 구분한다. PR #272 중복 영역을 재확인한다.
2. **실행 계층 단순화:** `mise run eval` 하나에 Promptfoo CLI 인수를 전달하는 계약을 우선 구현·검증한다. 기존 asset/suite별 `mise`·`npm` 별칭을 실제 소비자 필요에 따라 제거 또는 축소한다. `mise.toml`이 작업 entrypoint를 소유하도록 `npm run` 중복 경유를 없앨 수 있는지 검증한다. `package.json`은 npm dependencies 없는 scripts-only 파일이므로 **삭제를 기본 제안**으로 삼되, 먼저 모든 실제 소비자를 옮기고 삭제 후 검증한다. 특히 PR Gate의 `npm run rulesync:validate`, `mise run check`의 `biome check ... package.json`, Rulesync·Node·Promptfoo·Validation 문서의 링크/명령 및 평가 문서, 필요시 hook과 CI를 확인한다. npm backend가 설치하는 **패키지 내부**의 `package.json`과는 다른 대상이다. Promptfoo의 평가 config/모델/데이터/exit code 계약은 유지한다.
3. **진단과 최신성 분리:** 기존 검증과 겹치지 않는 최소 `preflight`(로컬, 빠름, 변경 없음)와 `outdated`(네트워크 필요, 알림 성격)을 배치한다. 새 릴리스 존재는 기본적으로 비차단, 선택/실행 버전 불일치와 필수 도구 결손은 적절하게 실패한다. 미확인 상황을 성공으로 둔갑시키지 않는다.
4. **부트스트랩 단순화:** 이전 Windows/Node/npm backend 테스트가 지키는 안전 계약을 존중한다. mise/uv가 동일한 것을 native로 검증하는지 **실제로 확인한 항목만** 코드에서 제거한다. 설치 승인·잠금 불변·경로 격리·Windows 실행·실패 시 부분 상태 보존은 유지한다. 임의 전역 변경 금지.
5. **Python·평가 실행 일관화:** 일반 task의 `uv run --locked`와 group 선택을 정리한다. Promptfoo의 `npx` 사용은 보존/대체 시 비용·재현성·실제 사용 빈도를 비교해 판단하며, 선택적 평가 실행이 기본 bootstrap에 자동 포함되도록 만들지 않는다.
6. **검증 및 정본 갱신:** 관련 단위 테스트, native 명령 실행, Windows/Linux 호환성 검증, `mise run check`, `mise run test`, PR Gate 및 문서 갱신으로 마무리한다. 본인 환경에서 실행하지 못한 검증은 CI 결과/미검증으로 구분한다.

## 완료 조건

- 불필요한 `mise → npm → uv → Python` 실행 중복이 제거된다. `package.json`은 실제 프로젝트 의존성/외부 소비자 확인 후 필요가 없다면 삭제하고, CI·명령·문서 링크/포맷 대상의 참조가 남지 않는다.
- 일반 작업이 의도치 않게 `uv.lock`, `mise.lock`, 도구 pin을 갱신하지 않는다.
- 가벼운 진단과 최신성 조회가 분리되고 정상·실패·미확인 상태를 구별한다. 자동 설치/업데이트, 외부 서비스 호출, 권한 변경은 발생하지 않는다.
- 기존 bootstrap의 설치 승인, 보존 경계, exact 잠금 검증, Windows fallback에 회귀가 없다. 정책 변화가 꼭 필요하면 명시적으로 기록하고 검증한다.
- 새 평가 대상을 추가할 때 `mise.toml`과 `package.json`에 asset별 task/script를 더 만들 필요가 없고, config와 CLI 매개변수로 선택할 수 있다. 기존 필터·cache/write·grader·smoke 계약은 보존한다.
- Promptfoo/Rulesync/Skills 실행 경로가 깨지지 않고 기존 평가/검증 결과 의미가 유지된다. PR #272의 유효한 신규 동작을 반영한다.
- 테스트와 문서, CI에서 새 단일 entrypoint를 사용하고, 프로젝트 정본과 충돌하는 설명이 없다.
- `main`에는 별도 승인과 PR Gate 없이 병합하지 않는다.

## 세션에서 도출된 재사용 교훈 (2026-11-02 갱신)

이 항목은 이번 작업의 **설계 판단 근거**다. 아직 검증하지 않은 가설을 정책으로 격상하지 않으며, 구현이 끝나면 확정된 것만 정본 문서에 반영한다.

1. **세션 시작의 핵심 문제는 도구·컨텍스트 최신성이다.** 업데이트가 존재해도 에이전트가 고정된 구버전을 관성적으로 사용하거나, 현재 도구와 맞지 않는 명령/API를 선택할 수 있다. 선언 버전·실행 버전 불일치, 허용된 최신 버전 후보, 에이전트가 참조하는 문서 버전을 구분해 진단한다.
2. **명령보다 결정론적 진단 우선.** 에이전트가 긴 문서를 반복해서 읽고 판단하기보다 기존 native 명령이 결과를 판정하고, 성공이면 짧은 결과, 문제가 있으면 범위를 좁힌 구조화된 출력만 제공한다. 시작·종료 Commands/Hook은 필요성이 확인될 때 단순 호출 표면으로만 쓴다.
3. **Doctor·매니저의 기능을 직접 복제하지 않는다.** 먼저 mise/uv/Rulesync가 제공하는 doctor, outdated, lock 검증, project task와 args 전달을 사용한다. 특정 mise 버전에서 지원하지 않는 기능은 사전 실행 확인 후 제한된 호환 대안만 고려한다.
4. **진단·갱신·실행은 서로 다른 계약이다.** 매 세션 빠른 로컬 진단과 주기적 네트워크 최신성 조회를 분리한다. 새 버전이 존재하는 것만으로 설치·전환·작업 차단을 하지 않는다. exact pin과 lock의 의도를 보존하며, 변경은 별도 영향 검토·승인·검증이 필요하다.
5. **중복된 task 정의는 매개변수로 줄인다.** Promptfoo는 config `-c`, suite `--filter-metadata`, cache/write 등의 CLI 인수로 선택한다. 평가 대상이 추가될 때 mise/npm 양쪽에 별칭을 쌓지 않는다. smoke, grader, 실제 모델 호출과 비용 경계는 단순화 전후 유지한다.
6. **`package.json` 제거와 npm 생태계 제거를 혼동하지 않는다.** 프로젝트 루트의 `package.json`은 현재 scripts-only이고 패키지 의존성 선언이 없다. 직접 호출하는 CI·문서·task를 이관하면 삭제 가능성이 높다. 반면 `mise.toml`의 `npm:` backend, Node와 `npx`는 별도 기능이므로 필요성을 개별 판단한다. bootstrap이 확인하는 **설치 패키지의 package.json**은 프로젝트 루트 파일을 삭제해도 필요하다.
7. **최적화는 삭제가 목적이 아니라 안전한 경로 단순화다.** 예전 Windows fallback에서 검증된 실행/잠금 경계를 성급히 제거하지 않고, 대표 테스트로 비용·실패 의미·호환성을 비교한다. `--locked`는 lockfile 수정을 막지만, uv 환경 동기화까지 원천 차단하는 읽기 전용 옵션은 아니다.
8. **동시 PR은 과거 가정을 무효화할 수 있다.** PR #272가 Promptfoo 실행 방식과 mise task를 함께 고치므로 작업 직전 최신 ref·diff·사용자를 확인하고 새 개선 사항을 덮어쓰지 않는다.

## 실행 기록과 추가 교훈 (2026-11-02)

- 신규 커밋 `5f4008e324ef451e8442568176632d8926ba20df`: 루트 `package.json` 삭제. mise의 `eval` 범용 task 및 Rulesync 세 작업 task 추가; CI의 npm 검증 호출을 mise로 이전; 문서 정합화. 기존 CLI pin·bootstrap·Promptfoo runner와 provider 로직은 변경하지 않음.
- **실제 PR Gate 성공:** GitHub Actions run `41452133512`에서 문서 계약, 결정론적 tests, 생성물 검증, mise 설치 및 Rulesync doctor/install/validate 단계 모두 통과. 이는 대상 CI 경로에 대한 evidence이며 로컬 OS·Promptfoo 실모델 eval 성공을 뜻하지 않음.
- **후속 검토로 발견한 문서 잔여:** `docs/skills/mols-test-design/evaluation.md`의 옛 별칭 및 `--no-cache --no-write` 기본값, `docs/skills/mols-loops/evaluation.md`의 과거 별칭 설명을 명시적 옵션 예시로 교체. Bootstrap evaluation 문서의 옛 npm 서술과 mise 인수 구분 기호도 수정.
- **mise Doctor 지원 버전 교훈:** 프로젝트 Doctor가 처음 도입된 버전은 `2026.9.6`, 현재 CI의 mise 설치 버전은 `2026.9.2`이다. 최신 upstream 문서의 기능을 현 환경에서 사용 가능하다고 추정하면 안 된다. 호스트 및 CI 업그레이드가 검증되기 전에는 기존 `mise ls --project --json`과 `uv lock --check`로 경량 점검을 제공한다. `preflight`는 완전한 실행/설치 상태 검증이 아니며 자동 update를 하지 않는다.
- **확인된 범위 밖:** `pyproject.toml` 자체의 dependency group을 재편성할 이유는 발견되지 않아 변경하지 않았고, `development_bootstrap.py`의 Windows/npm shim·격리 검증은 재현 계약을 보존하기 위해 그대로 두었다. PR #272의 Promptfoo provider 변경은 독립 진행 중이며 후속 동기화 시 새 head 검토 필요.

## 준비 시 검증 상태

- ✅ Pass — `main`의 관련 manifest, 주요 bootstrap/runner, 기존 테스트·CI 호출 경로 직접 조회.
- ✅ Pass — mise Doctor/Outdated 및 uv Locked의 공식 문서에서 기본 의미 확인.
- ⚪ Not Verified — 로컬 mise 버전의 Doctor 기능, Windows/Linux 실행, 최신성 탐지 결과, 구현 후 테스트와 CI.
- ⚪ Not Verified — PR #272 최종 diff 반영(작업 착수 시 다시 점검).

이 문서는 준비 근거만 보존한다. 구현이 끝나면 결과와 검증 근거는 PR·정본 문서·코드에 반영하고, 중복 작업 문서는 `.inbox/` 수명 주기에 따라 정리한다.
