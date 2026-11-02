# 개발 도구 실행 경로·진단 최적화 구현 계획

> 상태: 준비 완료, 구현·검증 미착수. 이 문서는 PR 진행 중의 작업 근거이며 저장소 정책이나 도구 설정의 정본이 아니다.

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
6. `mise run check`의 버전 출력은 자체로 선언/실행 버전 일치 증명이 아니다. 전체 검증·가벼운 환경 진단·외부 최신성 조회가 구분되어 있지 않다.
7. **열린 PR #272**가 `mise.toml`, `scripts/agent_assets/promptfoo_run.py`, 관련 eval과 문서를 변경 중이다. 작업 전에 최신 head와 병합 상태를 다시 확인하고 변경을 덮어쓰지 않는다. 새 PR은 생성 시점의 main에서 독립적으로 시작한다.

## 네이티브 우선 검토와 결정 기준

| 문제 | 먼저 검토할 네이티브 기능 | 조건부 대안 |
| --- | --- | --- |
| 가벼운 개발 환경 진단 | `mise doctor project --json`와 `[doctor.checks]` | 설치된 mise가 미지원이거나 구조화 출력에 실질적인 빈틈이 있을 때만 얇은 보조 스크립트 |
| 도구 최신성 탐지 | `mise outdated --no-global --bump --json` | 실패·오프라인 시 UNKNOWN, 자체 release/SemVer 엔진 구현 금지 |
| 잠금·선택 버전 확인 | `mise ls --current --json`, `mise.lock`, `uv lock --check` | 정확한 실행 바이너리 확인이 필요하면 기존 bootstrap 검증을 재사용 |
| 작업 진입점 | `mise run` task 직접 호출 | npm scripts가 별도 소비자에게 실제로 필요한 경우만 보존 |
| Python 실행 | `uv run --locked`와 필요한 group 지정 | bootstrap setup/update만 승인된 재현·갱신 경계 유지 |
| Rulesync 진단 | `rulesync doctor --strict` 및 기존 검증기 | 경로·warning 정책 같은 실제 계약이 필요한 최소 래퍼 유지 |

`mise doctor project`는 공식 문서에 존재하지만 현재 CI의 mise 설치 버전과 사용자 PC 버전에서 지원하는지는 미확인이다. 진단 명령도 shell을 실행하며 샌드박스가 아니므로 read-only 검사를 명시해야 한다. `uv run --locked`는 lock 변경을 막지만 환경 동기화까지 자동으로 비활성화하지 않으므로 '읽기 전용 세션 진단'에 무조건 사용하지 않는다.

공식 근거:
- https://mise.jdx.dev/configuration/project-diagnostics.html
- https://mise.jdx.dev/cli/outdated.html
- https://mise.jdx.dev/tasks/task-configuration.html
- https://docs.astral.sh/uv/concepts/projects/sync/

## 구현 순서

1. **호출 관계 및 기준선:** 실제 소비자(로컬 task, CI, pytest, eval, docs)를 모두 확인한다. 변경 전 Windows/Linux 경로, 기존 실패 상태, 설치/네트워크 부작용을 구분한다. PR #272 중복 영역을 재확인한다.
2. **실행 계층 단순화:** `mise.toml`이 작업 entrypoint를 소유하도록 `npm run` 중복 경유를 없앨 수 있는지 검증한다. `package.json`은 남은 필수 소비자가 없을 때만 삭제하고 CI의 `rulesync:validate` 호출·문서도 함께 옮긴다. Promptfoo의 평가 config/모델/데이터/exit code 계약은 유지한다.
3. **진단과 최신성 분리:** 기존 검증과 겹치지 않는 최소 `preflight`(로컬, 빠름, 변경 없음)와 `outdated`(네트워크 필요, 알림 성격)을 배치한다. 새 릴리스 존재는 기본적으로 비차단, 선택/실행 버전 불일치와 필수 도구 결손은 적절하게 실패한다. 미확인 상황을 성공으로 둔갑시키지 않는다.
4. **부트스트랩 단순화:** 이전 Windows/Node/npm backend 테스트가 지키는 안전 계약을 존중한다. mise/uv가 동일한 것을 native로 검증하는지 **실제로 확인한 항목만** 코드에서 제거한다. 설치 승인·잠금 불변·경로 격리·Windows 실행·실패 시 부분 상태 보존은 유지한다. 임의 전역 변경 금지.
5. **Python·평가 실행 일관화:** 일반 task의 `uv run --locked`와 group 선택을 정리한다. Promptfoo의 `npx` 사용은 보존/대체 시 비용·재현성·실제 사용 빈도를 비교해 판단하며, 선택적 평가 실행이 기본 bootstrap에 자동 포함되도록 만들지 않는다.
6. **검증 및 정본 갱신:** 관련 단위 테스트, native 명령 실행, Windows/Linux 호환성 검증, `mise run check`, `mise run test`, PR Gate 및 문서 갱신으로 마무리한다. 본인 환경에서 실행하지 못한 검증은 CI 결과/미검증으로 구분한다.

## 완료 조건

- 불필요한 `mise → npm → uv → Python` 실행 중복이 제거되거나 유지 근거가 문서화된다. `package.json` 존치/삭제 결정에는 호출자 전체가 반영된다.
- 일반 작업이 의도치 않게 `uv.lock`, `mise.lock`, 도구 pin을 갱신하지 않는다.
- 가벼운 진단과 최신성 조회가 분리되고 정상·실패·미확인 상태를 구별한다. 자동 설치/업데이트, 외부 서비스 호출, 권한 변경은 발생하지 않는다.
- 기존 bootstrap의 설치 승인, 보존 경계, exact 잠금 검증, Windows fallback에 회귀가 없다. 정책 변화가 꼭 필요하면 명시적으로 기록하고 검증한다.
- Promptfoo/Rulesync/Skills 실행 경로가 깨지지 않고 기존 평가/검증 결과 의미가 유지된다. PR #272의 유효한 신규 동작을 반영한다.
- 테스트와 문서, CI에서 새 단일 entrypoint를 사용하고, 프로젝트 정본과 충돌하는 설명이 없다.
- `main`에는 별도 승인과 PR Gate 없이 병합하지 않는다.

## 준비 시 검증 상태

- ✅ Pass — `main`의 관련 manifest, 주요 bootstrap/runner, 기존 테스트·CI 호출 경로 직접 조회.
- ✅ Pass — mise Doctor/Outdated 및 uv Locked의 공식 문서에서 기본 의미 확인.
- ⚪ Not Verified — 로컬 mise 버전의 Doctor 기능, Windows/Linux 실행, 최신성 탐지 결과, 구현 후 테스트와 CI.
- ⚪ Not Verified — PR #272 최종 diff 반영(작업 착수 시 다시 점검).

이 문서는 준비 근거만 보존한다. 구현이 끝나면 결과와 검증 근거는 PR·정본 문서·코드에 반영하고, 중복 작업 문서는 `.inbox/` 수명 주기에 따라 정리한다.
