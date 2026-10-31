---
description: 이 저장소의 개발환경 구축·격리·도구 관리 정책, 버전 수명 주기 거버넌스 및 부트스트랩 승인·운영 절차를 확인할 때 사용합니다.
---

# Development Environment

이 문서는 **이 저장소의 개발환경 구축과 유지보수 운영 정책의 정본**입니다. 개발환경의 격리·재사용 경계, 버전 수명 주기 거버넌스, 부트스트랩 실행 시의 사용자 설치 승인 여부를 판단할 때 먼저 확인합니다.

- **도구별 구체적인 실행 명령·복구·운영 방법:** [mise 안내](../references/tooling/mise.md)
- **도구 및 버전 선언:** [`mise.toml`](../../mise.toml) 및 각 native manifest/lockfile
- **실제 부트스트랩 실행기:** [부트스트랩 스크립트](../../scripts/development_bootstrap.py)
- **재사용 가능한 부트스트랩 설계 판단:** [`mols-dev-env-bootstrap-design` 설계 Skill (PR #256)](https://github.com/mols3131d/mols-agent-assets/pull/256) (설계 판단 자료이며 이 저장소의 권한 정책 정본이 아님)
- **조사 및 논의 근거:** [PR #258 작업 문서](../../inbox/github-258/development-environment-bootstrap-spec.md) (논의 근거일 뿐 운영 지침을 대체하지 않음)

---

## 개발환경 일반 정책

### 1. 환경 유형별 관리 주체와 격리 경계

전역 도구 재사용은 공통 기본값이 아닙니다. 프로젝트가 지정한 실행환경·패키지 격리·도구 관리 방식을 확인하고, 그 **관리 경계 안에서 이미 준비된 자산**만 재사용합니다. 전역에 같은 이름의 명령이 존재한다는 사실이 프로젝트의 격리·잠금 계약을 충족한다는 증거가 아닙니다.

| 대상 | 관리 주체 | 재사용 및 격리 판단 |
| --- | --- | --- |
| Git, Shell 등 호스트 선행 도구 | OS / Host 환경 | 설치된 바이너리가 프로젝트 요구와 호환되면 그대로 사용. 전역 업데이트·수정은 하지 않음 |
| Python 인터프리터 | uv (`.python-version`) | `.python-version`과 `pyproject.toml`의 요구조건에 따라 선택. 허용된 기존 인터프리터는 프로젝트 가상환경(`.venv`)의 기반으로만 재사용 |
| Python 프로젝트 패키지 | uv (`uv.lock`) | **프로젝트 `.venv`와 `uv.lock`을 독점 사용.** 시스템/사용자 site-packages나 PATH의 외부 Ruff/pytest 등을 프로젝트 의존성 대체물로 쓰지 않음 |
| 개발 CLI 도구 (`uv`, `node`, `biome` 등) | mise (`mise.toml`) | `mise.toml`의 pin 및 관리 주체 우선. 해당 관리자의 기존 설치·캐시는 재사용하되 무관한 전역 바이너리로 묵시적 대체 금지 |
| 외부 연동 및 사용자 HOME 자산 | 사용자 / native installer | 도구 설치와 별도 소유권·부작용 검토. 재사용 판단만으로 덮어쓰기나 설치 허가가 발생하지 않음 |

### 2. 자산 재사용 및 프로젝트 환경 보호

- **재사용 가능한 자산의 정의:** 이미 준비된 프로젝트 전용 `.venv`, 도구 관리자(`mise`) 소유의 설치본, 잠금과 일치하는 캐시를 먼저 확인합니다. 단, 해당 manager의 native 검증 기능을 활용하며 독자적인 범용 탐지 로직을 구현하지 않습니다.
- **인터프리터와 패키지 환경 분리:** 시스템 Python을 기반으로 사용하더라도 시스템/사용자 site-packages에 패키지를 설치하거나 공유하지 않습니다. 프로젝트 환경 외부를 가리키는 `UV_PROJECT_ENVIRONMENT` 및 symlink/junction은 차단합니다.
- **기존 프로젝트 환경 갱신 통제:** `uv sync`의 exact sync는 불필요한 패키지를 정리할 수 있으므로, 쓰기 동작으로 간주하고 환경 변경 승인 범위에 포함합니다.
- **불명확 시 격리 계약 우선:** 호스트 전역 설정을 임의로 수정하지 않고 프로젝트 격리 방식을 우선 제안하며, 확인되지 않은 환경에 대한 설치를 강행하지 않습니다.

### 3. 버전 정책 및 수명 주기 거버넌스

- **재현성 우선 (Zero Drift):** 개발환경 복구 및 초기 준비(`setup`)는 언제나 선언된 잠금(Exact Pin 또는 Lockfile)을 100% 재현해야 합니다. 임의의 네트워크 resolver가 최신 버전을 자동으로 탐색·승격하지 않습니다.
- **제한된 갱신 (Bounded Update):** 도구 및 의존성의 버전 갱신(`update`)은 사전에 승인된 정책 허용 범위 내에서만 수행하며, 변경된 lockfile diff를 검토할 수 있도록 보존합니다.
- **4가지 버전 정책 케이스 분류:**
  1. **패치 버전 준수하는 최신 버전 (장기 지원 선호):** Major.Minor 고정, Patch만 추적 (`~X.Y.Z`). 포맷팅/린터/코어 resolver 등 극도의 호환성이 요구되는 도구에 적용.
  1. **마이너 버전 준수하는 최신 버전 (장기 지원 선호):** Major 고정, Minor.Patch 최신 추적 (`^X.Y.Z`). SemVer 하위 호환성을 신뢰할 수 있는 성숙한 도구에 적용.
  1. **메이저 버전 준수하는 최신 버전 (장기 지원 선호):** 지원 수명 주기(LTS)를 준수하며 검증된 최신 메이저 라인 추적. Node.js 짝수 Active LTS 등 플랫폼 런타임에 적용.
  1. **최신 버전 (장기 지원 선호):** SemVer 상한 없는 최신 안정 릴리스 추적 (`latest`). 빠르게 진화하는 외부 생태계 연동 도구에 적용하되 lock 재현 필수.
  - *7개 CLI 도구별 구체적인 케이스 매핑, 현재 pin 버전 및 잠금 소유자는 [mise 안내: CLI 도구 버전 정책](../references/tooling/mise.md#cli-tool-versioning-policy-and-cases)에 명시합니다.*
- **현재 저장소 상태:** `mise.lock`이 도입되어 네이티브 바이너리 도구 4종의 7개 플랫폼별 아티팩트 URL·체크섬 및 npm 도구 3종의 버전이 잠금 관리됩니다. 현재 모든 CLI 도구는 Exact Pin(허용 범위 0) 상태를 유지하며, `update`는 Python 의존성(`uv.lock`)의 bounded upgrade만 수행합니다. CLI 도구의 자동 갱신(range 확장)은 별도 후속 과제로 분리합니다.

---

## 부트스트랩 운영 절차

### 1. 에이전트 실행 의도와 사용자 승인 게이트

- **진단·설계와 실제 쓰기 분리:** 환경 점검, 설계 논의, 코드 구현 요청만으로 사용자 컴퓨터나 공유 캐시에 도구 설치·업데이트를 실행하지 않습니다.
- **작업 묶음 단위 사전 승인:** 에이전트가 설치/갱신 명령을 실행하기 전, **설치 대상 도구·위치(프로젝트 `.venv`, 공유 mise cache, HOME), 의존성 변경 이유, 잠금 변경 범위**를 요약하여 사용자의 명시적 허가를 받습니다. 한 번 승인된 작업 묶음은 해당 범위 내에서 추가 질문 없이 진행할 수 있으나, 범위가 확장되면 다시 허가를 받습니다.
- **호출자 책임 원칙:** 현재 부트스트랩 스크립트에는 대화형 터미널 승인 프롬프트가 없으므로, **에이전트가 명령을 대신 호출할 때의 사전 승인 획득 책임은 에이전트에 있습니다.**
- **권한 상승 금지:** 사용자 승인이 있더라도 관리자 권한(sudo 등) 상승이나 출처 불명의 외부 스크립트 무단 실행은 정당화되지 않습니다.

### 2. Core 부트스트랩 범위와 선택적 연동 분리

부트스트랩의 기본 성공 범위(`READY`)는 **Core 개발환경(mise 관리 CLI 도구 + 프로젝트 `.venv` Python 환경)**으로 엄격히 한정합니다.

| 구분 | 포함 대상 | 실행 및 검증 정책 |
| --- | --- | --- |
| **Core 부트스트랩** | `mise.toml` 관리 CLI 7종, Python 인터프리터, `.venv` 패키지 동기화 | 기본 `setup`/`update`에서 실행 및 검증. 실패 시 nonzero 및 `FAILED`/`BLOCKED` |
| **선택적 연동 (별도)** | Rulesync 외부 설치·projection, 사용자 HOME Skill 동기화, Lefthook Git hooks | 기본 부트스트랩에서 제외. 호스트/사용자 영향 검토 후 명시적 별도 명령으로만 실행 |

- `mise run skills-sync`, `rulesync install --frozen`, `lefthook install` 등은 Core 부트스트랩 완료 후 별도의 영향 설명과 승인을 거쳐 실행합니다. 세부 절차는 [mise 안내: 선택적 연동](../references/tooling/mise.md#optional-integrations)을 참조합니다.

### 3. Setup / Update 작업 경계

| 작업 | 버전·상태 계약 | 허가 및 변경 범위 |
| --- | --- | --- |
| **상태 점검·계획** | 기존 도구 및 정책 확인; version/lock 변경 없음 | 사전 설치 허가 불필요 (읽기 전용 진단) |
| **`setup` (반복 복구)** | 확정된 exact pin과 lockfile 재현; 암묵적 latest 갱신 없음 | 사전 설치 허가 필요. 승인된 mise 관리 영역과 프로젝트 `.venv`에 한정 |
| **`update`** | 선언된 허용 범위 내 최신 해석 후 lock diff 검토 | 사전 업데이트 허가 필요. 버전 정책 임의 확대 불허, 자동 commit 금지 |

- 세부 실행 명령(`mise run setup`, `mise run update`, `--dry-run` 등)과 단계별 복구 절차는 [mise 안내: Setup, update and diagnosis](../references/tooling/mise.md#setup-update-and-diagnosis)를 따릅니다.

### 4. 확인 및 종료 조건

- **결과 판정:** 필수 Core 준비 단계가 모두 통과하면 `READY`(exit 0)를 반환하며, 선택적 연동은 제외되었음을 명시합니다(`excluded and not verified`). 필수 단계가 하나라도 실패하면 `FAILED`/`BLOCKED`와 nonzero exit code를 반환합니다.
- **부분 상태 보존:** 실패 시 사용자 작업 트리나 미완료 상태를 강제로 `git reset`/`clean`하거나 삭제하지 않으며, 원인을 파악할 수 있도록 보존합니다.
- **동시 실행 방지:** `.tmp/bootstrap.lock`을 통해 동일 작업 트리 내의 동시 실행을 차단합니다.
