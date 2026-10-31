---
description: PR #258의 부트스트랩 실행기에서 mise·uv·Git에 위임할 수 있는 과도한 자체 로직, 중복 설정과 반복 검사를 검토하고 안전 계약을 보존하는 최소 경량화 범위를 결정할 때 참고합니다.
---

# PR #258 — 부트스트랩 경량화 검토

> **결론:** 전면 재작성은 불필요하다. 이미 확보한 격리·잠금·실패 안전성은 유지하고, 명확한 정책 오류 1건을 먼저 수정한 뒤 mise native 위임 가능성만 작은 실험으로 확인한다.
>
> **범위:** [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258), base `b29aa490d0c251d5ca478fa5c787b90258f09d79` → 검토 HEAD [`ebcac30`](https://github.com/mols3131d/mols-agent-assets/commit/ebcac30ad7b04dc44746ff3759a176e968bd23f9) (2026-11-01). 이 문서는 **비정본 정적 검토 보고서**다. 실제 환경 설치·Windows 경로 실행·성능 측정은 수행하지 않았다.
>
> **정본:** 개발환경 정책은 [Development Environment](../../docs/development/development-environment.md), 실행 방식은 [mise 운영 안내](../../docs/references/tooling/mise.md), 버전 선언은 [mise.toml](../../mise.toml)이 소유한다. 이 보고서는 해당 계약을 재정의하지 않는다.

## 판단

현재 [부트스트랩 실행기](../../scripts/development_bootstrap.py)는 약 **508줄**, [전용 테스트](../../tests/scripts/test_development_bootstrap.py)는 약 **688줄**이다. 크기 자체가 결함은 아니다. 다만 **일곱 도구의 exact pin 설치와 프로젝트 `.venv` 준비**라는 core 목적에 비해, npm 패키지의 내부 디렉터리·manifest 탐색, 여러 위치에서의 같은 환경 검사, 명시적 설정과 중복 가능성이 있는 환경변수 주입이 유지보수 비용을 만든다.

| 우선 | 대상 | 현 상태에 대한 근거 | 최소 권고 |
| --- | --- | --- | --- |
| **먼저 수정** | `update`의 `mise.lock` 변경 허용 | 현재 갱신 대상은 `uv.lock`뿐인데 `unchanged_policy()`가 두 lock 모두 예외 처리 | `update` 예외를 `uv.lock`으로만 제한, 회귀 테스트 1건 |
| **검증 후 결정** | npm CLI 실행 경로 직접 해석 | `tool_command()`이 `mise where`, `node_modules`/ `lib/node_modules`, `package.json`의 `bin`과 버전을 자체 확인하고 pinned Node·PATH를 조립 | `mise exec` 등 native 실행으로 같은 보장이 가능한지 작은 Windows/Linux 실험; 동등할 때만 구현과 종속 테스트 축소 |
| **소규모 정리** | 환경변수 주입 | `mise.toml`의 `[settings] lockfile = true`와 자식 `MISE_LOCKFILE=1`은 겹칠 여지가 있음 | 설정만으로 요구가 충족되는지 확인 후 중복 주입 제거; 다른 변수 일괄 삭제 금지 |
| **소규모 정리** | `.venv` 검사 호출 | `check_environment()`가 `main()`과 `python_environment()` 진입·중간에서 반복됨 | 단계 사이의 실제 변경 가능성을 검토하고 불필요한 검사만 축소; 설치·동기화 직전의 안전 검사는 유지 |
| **낮은 우선순위** | 미래 버전 정책·상태 출력 | 4가지 CLI 범위 정책을 상세히 기술하지만 현 구현은 모두 exact pin; `report()`는 선택 기능 생략 안내를 매번 출력 | 미래 계획은 짧게 연결하고 현재 동작을 우선 표기; 출력을 줄여도 `READY` 의미와 선택 기능 미검증은 남김 |

### 1. 즉시 가능한 보완 — Python 전용 update에서 lock 예외 축소

[`unchanged_policy()`](../../scripts/development_bootstrap.py)는 현재 다음 조건으로 `update`의 잠금 파일 검사를 건너뛴다.

```python
if name in ("uv.lock", "mise.lock") and self.mode == "update":
    continue
```

그러나 `python_environment()`의 update 경로는 `uv lock --upgrade --no-python-downloads`만 실행한다. 우연한 `mise.lock` 변경이 있어도 `report()`에서 `[changed] mise.lock`을 출력한 채 `READY`를 반환할 수 있다. **의도적으로 변경 가능한 파일은 `uv.lock`뿐**으로 제한하면 코드가 줄고 실제 계약에도 일치한다. 변경 감시 엔진을 확장하거나 자동 rollback을 만들 필요는 없다.

### 2. 큰 단순화 후보 — npm 실행의 mise 위임

`tool_command()`의 npm 경로 처리는 Windows `.cmd` shim 우회, 설치 패키지 identity 확인, 잠근 Node 실행이라는 이유가 있다. 따라서 코드가 길다는 이유만으로 바로 삭제하면 안 된다.

[mise exec](https://mise.jdx.dev/cli/exec.html)는 선택된 mise 도구의 환경에서 명령을 실행하고, [mise install --locked](https://mise.jdx.dev/dev-tools/mise-lock.html)는 설치 잠금 재현을 담당한다. **이 기능의 존재가 현재 npm backend·Windows 조합에서 기존 방어와 동등함을 입증하지는 않는다.**

최소 실험은 현재 관리되는 Node와 npm CLI 한 종으로, 실제 Windows 및 대표 Unix 환경에서 다음을 확인하는 것이다.

1. `mise exec` 경로에서 **의도한 CLI의 정확한 버전**이 실행되고 호스트의 동명 전역 바이너리를 사용하지 않는지.
2. Windows `.cmd` shim 및 `node` 선택이 기존 경로와 동등하며, 원치 않는 자동 설치·외부 상태 변경이 없는지.
3. 실패 시 기존처럼 nonzero를 반환하고 core 환경을 거짓 `READY`로 보고하지 않는지.

통과하면 npm manifest 직접 파싱과 연결된 테스트를 함께 제거한다. 실패하거나 확신이 없으면 **기존 구현을 유지**한다. 별도 OS 어댑터나 커스텀 실행 프레임워크는 만들지 않는다.

### 3. 환경변수와 반복 검사

- **중복 검토:** `MISE_LOCKFILE=1`은 `mise.toml`의 `lockfile = true`와 중복될 가능성이 높다. 실제 child process가 config를 읽는지 확인한 뒤 제거한다. `MISE_LOCKED` 강제 주입은 직전 커밋에서 이미 제거했고, 설치는 `mise install --locked`를 유지한다.
- **바로 제거하지 말 것:** `MISE_AUTO_INSTALL=0`과 `task.run_auto_install = false`는 적용 범위가 동일하다고 단정할 수 없다. `UV_PYTHON_DOWNLOADS=never`와 개별 `--no-python-downloads`도 영향을 받는 subprocess가 동일한지 확인해야 한다.
- **보존 후보:** `UV_PROJECT_ENVIRONMENT` 격리, 충돌하는 `UV_*` project/group override 제거, 외부 Git 작업 트리 선택 변수 방어, noninteractive Git 실행, Node prerequisite 실패 시 npm 단계 차단은 이유가 분명하다.
- **검사 합치기:** `check_environment()`의 반복 호출 중 단계 사이에 쓰기가 없는 구간은 줄일 수 있다. 반면 `uv lock` 뒤 `uv sync` 직전, 또는 외부 도구 실행 뒤 오염될 수 있는 경계의 검사는 유지한다.

### 4. 테스트·문서의 축소 기준

안전 계약을 지키는 테스트(외부 `.venv`·symlink 및 system-site-packages 차단, Git 격리, `--locked` 적용, `uv` 그룹 강제, dirty input 거부, 필수 실패의 nonzero)는 보존한다. native 위임으로 **사라진 사설 구현의 내부 구조**를 모킹한 테스트만 함께 삭제한다. 모든 OS × 모든 환경변수의 조합이나 새 테스트 프레임워크는 요구하지 않는다.

운영 정본에는 **현재 exact pin 및 Python-only update**를 먼저 설명한다. 4가지 SemVer 범주와 미래 CLI bounded update는 설계 방향으로만 유지하고, 반복된 정책 문구는 링크로 연결한다. 기존 [과설계 검토(2026-10-25)](bootstrap-overengineering-review-2026-10-25.md)는 이전 revision의 조사 근거로 보존하되 현재 결론으로 재사용하지 않는다.

## 작업 경계와 완료 조건

권장 순서는 **(1) `mise.lock` 예외 수정 → (2) npm native 실행의 작은 실증 → (3) 통과한 항목만 코드·테스트 동시 축소 → (4) 설정·문구 중복 정리**다. 본 PR의 머지 판단을 실제로 바꾸는 correctness 문제는 (1)을 우선 처리한다. (2)~(4)는 검증 비용·변경 위험이 이득보다 커지면 후속 작업으로 분리한다.

완료 판단은 줄 수 감소가 아니다. **setup은 잠금 설치를 재현하고, update는 의도된 `uv.lock`만 바꾸며, 기존 사용자/호스트 상태를 침범하지 않고, 실패를 성공으로 보고하지 않는 것**이 기준이다. 기존 PR Gate와 관련 회귀 테스트를 다시 통과하면 충분한 기본 근거가 되며, native npm 대체를 채택할 경우에만 해당 OS 실제 실행 근거를 추가한다.

**비목표:** 전역 패키지 관리자 자체 구현, 범용 환경변수 sanitizer, 자동 설치 승인 UI, 정책 DSL, 자동 복구·rollback, 새 검사 프레임워크, CLI 버전 범위 갱신 기능 도입.
