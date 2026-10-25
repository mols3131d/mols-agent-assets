# PR #258 — 정리 → 리뷰 → 개선 루프

> 2026-10-25 · `mols-loops` 적용 작업 기록. 이 문서는 **진행 중인 근거와 인계**이며 운영 정본이 아니다. 기준 revision: `6ab727a7dfff9934515b14c8401180db5f296bc6`. 정본은 [Development Environment](../../docs/development/development-environment.md), 범위 제한은 [최소 변경 계획](next-steps-minimal-scope.md)을 따른다.

## Goal / Scope

**Goal:** PR #258의 기존 `setup`/`update`를 유지하면서 F1~F3의 실제 환경 오판을 없앤다. 가능한 한 도구 기본 동작, native manifest/lock, 호환되는 전역 환경을 이용하며 새 강제 설정·추상화·작업 범위를 만들지 않는다.

**In:** `scripts/development_bootstrap.py`와 대응되는 `tests/scripts/test_development_bootstrap.py`의 좁은 수정, 기록 갱신, 검증.

**Out:** CLI 도구 버전 범위 업데이트, PR #256의 Skill, HOME/전역 설치, Git hooks/Rulesync projection, 사용자 환경 수정, 새 설치 승인 시스템, 범용 env 필터·환경 탐지 프레임워크. 사용자 설치 승인은 기존 정본의 호출자 책임을 유지.

**Acceptance:** (1) 오염된 Git env에서도 진짜 저장소의 dirty lock 갱신 거부; (2) uv 그룹 제외 env가 sync/check의 준비 결과를 왜곡하지 않음; (3) system-site-packages venv가 READY로 통과하지 않음; (4) 기존 정상 흐름 통과; (5) 실제 실행한 검증과 미검증을 구분.

## 1차 정리 / Research

- 현재 runner: 기존 env를 상속하고 Git/uv/mise 관련 7개 변수를 지정하며 6개를 제거한다. `mise.toml`은 도구 exact pin을 선언하며 [운영 정본](../../docs/development/development-environment.md)은 전역 Python 패키지의 프로젝트 의존성 대체를 금지한다.
- [이전 안전성 검토](bootstrap-isolation-review-2026-10-25.md)는 F1 Git 선택 env, F2 `UV_NO_GROUP`/`UV_NO_DEV`, F3 `include-system-site-packages = true`를 보고했다. F2/F3의 이전 native 재현은 uv 0.10.0으로, 프로젝트 pin 0.12.1과 구별한다.
- 공식 uv CLI는 `--no-group`이 `--all-groups`보다 우선한다고 규정한다. Python의 `venv`는 `pyvenv.cfg`에 system-site-packages 허용을 기록한다. 단지 `--all-groups`를 추가하거나 `.venv` 디렉터리가 존재한다는 이유만으로 안전하지 않다.

## 1차 리뷰 / 독립 질문별 판정

| 관점 | 확인 질문 | 판정 및 개선 결정 |
| --- | --- | --- |
| 정확성 | Git cwd가 대상 repo를 보장하는가? | **아니오.** Git 명령에서 저장소 선택에 쓰이는 알려진 env 3종만 제외하고 실제 toplevel 확인. 전역 Git config 보존 |
| 정확성 | uv의 `--all-groups`가 ambient exclude를 이기는가? | **아니오.** uv 동기화/확인 subprocess에만 `UV_NO_GROUP`, `UV_NO_DEV` 전달을 막고 다른 uv/registry/proxy 설정은 상속 |
| 격리 | 기존 pyvenv.cfg가 시스템 패키지를 노출할 수 있는가? | **예.** 기존 preflight에서 true만 차단, env를 자동 삭제·변경하지 않음 |
| 단순성 | 강제 env 7개를 모두 제거하거나 전역 설정을 일괄 차단할 것인가? | **아니오.** 기존 값의 의미가 확정되지 않은 상태에서 안전 계약을 바꾸지 않음. 신규 기본값 0개, 새 generic wrapper 금지 |
| 증거 | 무엇을 검증할 것인가? | 해당 반례와 정상 경로를 deterministic pytest, 변경 후 PR Gate로 확인. cold-install/타 플랫폼/uv 0.12.1 native 검증이 없다면 별도로 표기 |

## 1차 개선 / Work

- 이 섹션은 이후 실제 코드 변경과 검증 결과로 갱신한다. 승인 없는 사용자 머신/공유 HOME 변경은 진행하지 않는다.

## 2차 리뷰 / Finalize

- **대기:** 변경 후 회귀와 PR Gate, 미해결 위험을 확인하고 결과를 기록한다.
