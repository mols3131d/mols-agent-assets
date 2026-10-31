# 부트스트랩 CLI 버전 정책 및 mise.lock 잠금 설계

> **상태:** 확정 및 구현 완료 (2026-10-31). 이 문서는 PR #258의 버전 정책 논의 및 `mise.lock` 도입 작업 자료다.
> **정본:** [개발환경 운영 정책 정본](../../docs/development/development-environment.md). 도구별 상세 버전 정책·허용 범위는 [mise 안내](../../docs/references/tooling/mise.md), 실제 선언은 [`mise.toml`](../../mise.toml) 및 [`mise.lock`](../../mise.lock)이 소유한다.
> **대상 PR:** [PR #258](https://github.com/mols3131d/mols-agent-assets/pull/258) · 브랜치 `mols/feat/repository-dev-bootstrap`

---

## 1. 배경 및 문제 정의

이전 부트스트랩 구현에서는 모든 CLI 도구를 `mise.toml`에 exact pin으로만 선언하면서도, 향후 업데이트 지향 정책이나 잠금 파일(`mise.lock`)과의 관계가 불분명했다. 또한 `development_bootstrap.py`에서는 `mise.lock` 존재 시 실행을 사전 차단하고 있어, 멀티 플랫폼 바이너리 무결성을 검증하는 잠금 도입이 지연되었다.

이에 따라:

1. 7개 CLI 도구의 특성에 맞춘 **4가지 버전 정책 케이스**를 정립하고,
1. `setup`(0-drift 잠금 재현)과 `update`(범위 내 최신 갱신)의 역할을 명확히 분리하며,
1. 공식 `mise.lock`을 생성하여 7개 플랫폼 전반의 체크섬과 다운로드 URL을 커밋 잠금 관리한다.

---

## 2. 4가지 버전 정책 케이스 분류

| 케이스 | SemVer 규칙 및 범위 | LTS / 안정성 전략 | 호환성 및 운영 위험도 | 적용 대상 CLI |
| --- | --- | --- | --- | --- |
| **1. 패치 버전 준수하는 최신 버전** | `~X.Y.Z` (`X.Y.*`)<br>• Major·Minor 고정<br>• 최신 Patch만 수용 | 특정 안정 Minor 라인 유지, 보안 패치 및 결함 수정만 지속 반영 | **호환성 최우선 (Zero Risk)**<br>CLI 플래그·포맷 규칙 변경에 따른 churn 및 오작동 원천 차단 | • `uv` (0.x 코어 resolver)<br>• `rumdl` (0.x Markdown 린터)<br>• `npm:@biomejs/biome` (포맷팅 일관성) |
| **2. 마이너 버전 준수하는 최신 버전** | `^X.Y.Z` (`X.*`)<br>• Major 고정<br>• 최신 Minor·Patch 수용 | 장기 지원 메이저 라인 내에서 비파괴적 최신 기능과 성능 개선 지속 흡수 | **제한적 최신성 (Low Risk)**<br>하위 호환성 유지(SemVer 엄격 준수 성숙 도구 대상) | • `lefthook` (v2 Git hook 실행기)<br>• `node` (Active LTS 메이저 내 최신) |
| **3. 메이저 버전 준수하는 최신 버전** | 지원 수명 주기 준수<br>• 비LTS(Current 홀수 등) 배제<br>• 검증된 LTS 메이저 추적 | 릴리스 즉시 승격하지 않고 공식 LTS 전환 및 마이그레이션 검증 후 승격 | **계획된 현대화 (Medium Risk)**<br>Breaking change 가능성이 있어 명시적 검증 후 전환 | • `node` (Node.js 짝수 Active LTS 준수)<br>• `npm:rulesync` (호환 검증된 메이저 라인) |
| **4. 최신 버전** | `latest` / `*`<br>• 상한선 없는 최신 릴리스<br>• 프리릴리스 제외 | 최신 안정 공식 릴리스 선호, Alpha/Beta/RC 배제 | **생태계 동기화 (High Risk)**<br>빠르게 진화하는 외부 스펙 대응 우선, lock 재현 필수 | • `npm:skills` (Agent Skills 생태계 연동) |

---

## 3. 7개 CLI 도구 매핑 및 잠금 소유권

| 도구 | 현재 Pin (`mise.toml`) | 버전 정책 케이스 | 허용 범위 및 선정 사유 | 잠금 소유자 |
| --- | --- | --- | --- | --- |
| `uv` | `0.12.1` | Case 1 (패치 준수) | 0.x 단계에서 resolver 플래그 및 환경 동작 변경 방지 | `mise.lock` |
| `node` | `24.19.0` | Case 2 & 3 (LTS 메이저 준수) | Node 짝수 Active LTS 메이저 내 최신 마이너/패치 | `mise.lock` |
| `rumdl` | `0.2.54` | Case 1 (패치 준수) | Markdown 린터/포맷터 특성상 전체 파일 churn 방지 | `mise.lock` |
| `lefthook` | `2.1.10` | Case 2 (마이너 준수) | v2 메이저 호환성 유지 하에 하위 호환 기능 업데이트 | `mise.lock` |
| `npm:@biomejs/biome` | `2.5.6` | Case 1 (패치 준수) | 코드 포맷/린트 규칙 변경에 따른 대량 diff 방지 | `mise.lock` |
| `npm:rulesync` | `40.2.0` | Case 3 (메이저 준수) | 프로젝트 호환성이 검증된 안정 릴리스 라인 유지 | `mise.lock` |
| `npm:skills` | `1.5.23` | Case 4 (최신 안정) | 외부 스킬 저장소·프로토콜 연동을 위한 최신 안정 지향 | `mise.lock` |

---

## 4. `mise.lock` 잠금 아키텍처 및 구현

1. **플랫폼별 아티팩트 및 버전 잠금 보장 범위 구분:**
   - **바이너리 도구 4종(`uv`, `node`, `rumdl`, `lefthook`):** 7개 플랫폼(`linux-arm64`, `linux-arm64-musl`, `linux-x64`, `linux-x64-musl`, `macos-arm64`, `macos-x64`, `windows-x64`)의 아티팩트 URL, sha256 체크섬, GitHub provenance를 `mise.lock`에 고정.
   - **npm 도구 3종(`biome`, `rulesync`, `skills`):** 최상위 패키지 버전 잠금 적용 (npm 전이 의존성 sidecar는 이번 PR의 필수 범위에 포함하지 않음).
   - `mise.toml`에 `[settings] lockfile = true` 활성화.
1. **실행기(`scripts/development_bootstrap.py`) 연동 및 Strict Locked Mode 강제:**
   - `mise.lock`을 `UPDATE_INPUTS` 및 `POLICY_FILES`에 등록.
   - `setup` 실행 시 `mise install --locked <tool@version>`으로 mise의 **native strict locked install**을 강제. 잠금 누락 시 즉시 실패.
   - `setup` 도중 `mise.lock`이 변조되면 `unchanged_policy()`에서 즉시 실행 차단.
   - `update` 시 미커밋된 `mise.lock` 변경을 `check_update_state()`에서 사전 차단.
1. **Setup vs Update 불변성 및 범위 한정:**
   - `setup`은 언제나 `mise.lock`에 기록된 정확한 바이너리/버전을 재현하며 네트워크를 통한 임의의 상위 버전 조회를 차단함 (Zero Drift).
   - **현재 구현에서 `update`는 Python 의존성(`uv.lock`)의 bounded upgrade만 수행**하며, CLI 도구의 자동 갱신은 수행하지 않고 exact pin을 유지함. CLI 자동 갱신은 후속 과제로 분리.
