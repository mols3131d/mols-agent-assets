---
description: PR #257의 Rulesync 관련 CI와 테스트에서 과설계·중복·검증 공백을 근거 기반으로 식별한 검토 보고서입니다.
---

# PR #257 — Rulesync CI·테스트 검토 보고서

> **시점:** 본 검토의 코드·CI 관측은 **v16.24.1 기준**이다. 이후 PR #257은 Rulesync pin을 **v40.2.0**으로 변경하고 root `doctor --strict` 단계를 추가했다. 이 보고서의 '현재'와 이전 green CI는 작성 당시의 snapshot이다. 남은 v40 lock/설치 검증과 실제 HEAD 상태는 [업그레이드 계획](rulesync-v40-upgrade-plan.md) 및 [인계 보고서](rulesync-v40-handoff.md)를 참고한다.

## 결론

**Rulesync 관련 CI와 테스트의 최적화가 필요하다.** 기존 `Branch Check`와 `PR Gate` 자체가 과설계라는 뜻은 아니다. 현재 복잡성의 주요 원인은 (1) Git transport용 설치 래퍼와 그 내부 구현 테스트, (2) 서로 다른 Rulesync workspace의 검증 경계 혼동, (3) upstream이 소유하는 스키마·출력 형식을 자체 검증으로 반복할 가능성이다.

별도 설계는 [Rulesync 검증 수준 최적화 제안서](rulesync-verification-proposal.md)에 둔다. 이미 합의된 transport 방향은 [GitHub transport 유지 요청](rulesync-github-transport.md)을 따른다.

- 검토 기준: [PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257) HEAD `2b0d4bc5c730bae0bd1d9976a0ff94bcb080adc2`, base `7e595952aba994c46dd4c40cb95238c0eaf2b7f1`
- 방법: PR diff, 저장소의 CI·테스트·설치 코드, 실제 Actions 실행 기록, Rulesync **고정 버전 v16.24.1**의 공식 문서 정적 대조
- 검증 한계: 이번 조사에서 코드 변경이나 로컬 실행, 고장 주입 실험은 수행하지 않았다. GitHub Actions의 통과는 **당시 구현**에 관한 근거이며, 제안 변경의 통과 근거가 아니다.

## 현재 실제 검증 경로

| 경로 | 실제 검증 | 범위 및 한계 |
| --- | --- | --- |
| [`Branch Check`](../../.github/workflows/branch-check.yml) | frontmatter, 전체 pytest, 네트워크 없는 로컬 projection drift | branch tip의 빠른 피드백; merge candidate 전체를 검증하지 않음 |
| [`PR Gate`](../../.github/workflows/pr-gate.yml) | frontmatter, 전체 pytest, 변경 영향 projection drift, Rulesync 검증 | `main`과의 merge candidate; required check |
| [`rulesync:validate`](../../scripts/agent_assets/rulesync_validate.py) | `src/rulesync`에서 `doctor --strict`, `generate --dry-run`; JSON 성공·warning 검사 | **재사용 라이브러리만 검증**. 루트 `rulesync.jsonc`와 `rulesync.lock`에 대한 `install --frozen`은 실행하지 않음 |
| [repository routes](../../scripts/agent_assets/routes_repository_generate.py) | 루트 config/lock의 일부 값으로 route를 구성하고 remote SKILL을 읽어 확인 | repository-owned routing 계약을 검증하지만 Rulesync 전체 config/lock semantics나 실제 설치를 대신하지 못함 |
| [`mise run rulesync-install`](../../mise.toml) | `rulesync_install.py`를 거쳐 frozen 설치 | `setup`의 실제 설치 경로이며 **현재 CI에서는 호출하지 않음** |

실행 기록([PR Gate #40019355465](https://github.com/mols3131d/mols-agent-assets/actions/runs/40019355465), [Branch Check #40019345459](https://github.com/mols3131d/mols-agent-assets/actions/runs/40019345459))에서 두 작업 모두 성공했다. 마지막 실행 job의 시작~종료 시간은 PR Gate 약 **42초**, Branch Check 약 **14초**였다. PR Gate의 `mise` 기반 Rulesync 도구 설치 단계가 약 15초, 라이브러리 Rulesync 검증 단계가 약 6초를 차지했다. 한 번의 실행 관측치이므로 장기 평균이나 최적화 효과 추정치는 아니다.

## 발견 사항 및 처리 의견

### 1. 🟠 High — 루트 원격 소스 설치 검증 공백

`PR Gate`의 Rulesync 검증은 라이브러리 workspace 전용이다. 그러나 PR #257은 루트의 `rulesync.jsonc`, `rulesync.lock`과 설치 entrypoint를 변경한다. 현재 green gate는 새 `rulesync install --frozen`이 lock·실제 remote source와 호환되는지 증명하지 못한다.

**제안:** transport를 `github`로 복귀한 뒤, 루트 source·lock을 바꾸는 변경에 한해 고정 Rulesync CLI의 `doctor --strict`와 `install --frozen`을 검증한다. 설치는 잠긴 ref만 사용하고 lock을 갱신하지 않아야 한다. 실제 설치가 실패할 수 있는 변경을 합치지 않도록 admission 근거를 확보한다. 네트워크·인증 실패는 명확하게 분리해서 보고한다.

### 2. 🟡 Medium — Git transport 전용 구현과 테스트의 존속 근거 부족

[`rulesync_install.py`](../../scripts/agent_assets/rulesync_install.py)는 inherited `GIT_CONFIG_*`를 유지하며 `core.autocrlf=false`를 덧붙이기 위한 래퍼이고, [전용 pytest](../../tests/scripts/agent_assets/test_rulesync_install.py)는 그 래퍼의 4개 동작을 검증한다. 앞서 정한 `github` transport로 복귀하면 해당 Git checkout 보정 계약이 사라질 수 있다.

**제안:** 다른 사용처를 확인한 뒤 래퍼, 그 래퍼만 위한 태스크와 테스트 4개를 함께 제거한다. 테스트만 남기거나 테스트를 이유로 구현을 유지하지 않는다. `PYTHONUTF8` 등 독립 변경은 따로 판단한다.

### 3. 🟡 Medium — 자체 Rulesync JSON 검증기의 책임 재평가

[`rulesync_validate.py`](../../scripts/agent_assets/rulesync_validate.py)는 성공 여부와 warning을 자체 파싱한다. [8개 단위 테스트](../../tests/scripts/agent_assets/test_rulesync_validate.py)는 이 **자체 어댑터**의 동작을 확인하는 것이지 Rulesync field/type semantics의 증거가 아니다.

자체 wrapper가 warning을 반드시 실패로 다뤄야 하는 repository 정책을 표현한다면 일부 테스트는 정당하다. 반대로 CLI 반환 코드만으로 같은 fail-closed 계약을 충족할 수 있다면 JSON parser, 출력 타입별 방어 코드, 해당 테스트 일부를 줄일 여지가 있다. **동일한 실패를 보존하는지 먼저 확인하고** 축소해야 한다.

### 4. 🟡 Medium — pytest 전체 적용 Git 환경 격리

[`tests/conftest.py`](../../tests/conftest.py)의 session autouse fixture는 `git rev-parse --local-env-vars`로 조회한 이름을 모든 테스트의 환경에서 제거한다. Git hook에서 임시 저장소 테스트가 상위 저장소의 `GIT_DIR` 등을 물려받는 오류를 막는 효과는 있지만, 이를 의도적으로 참조하는 테스트와의 호환성은 별도 검토해야 한다.

**제안:** 독립적으로 재현되는 hook 문제라면 격리를 유지하되, 필요 테스트 또는 Git 임시 저장소 helper로 한정할 수 있는지 살핀다. 여러 테스트에서 동일한 우회 구현을 만드는 정도로 과도하게 축소하지는 않는다.

### 5. 🔵 Low — 중복 실행은 있으나 새 CI 프레임워크를 만들 수준이 아님

같은 push에 대해 `Branch Check`와 `PR Gate`가 모두 실행되고 pytest가 중복된다. 그러나 전자는 빠른 branch 신호, 후자는 실제 merge candidate 검증이라는 의미 차이가 있다. 관측된 작업 시간도 수십 초 수준이다.

**제안:** 둘 다 유지한다. 향후 비용이 실제로 문제될 때만 cheap checks의 중복 또는 조건부 선택을 조정하고, 지금은 경로 필터 전용 프레임워크·캐시 계층·OS 매트릭스를 추가하지 않는다.

## 파일·필드·타입 검증에 대한 잠정 판단

파일이 존재하고, 필수 필드와 올바른 타입·enum 값을 가지는지는 **검증할 가치가 있다**. 다만 검증의 소유자를 분명히 해야 한다.

- `rulesync.jsonc`의 키·타입·지원 값: **Rulesync `doctor --strict`** 및 공식 schema. 자체 필드 목록과 타입 정의 복제는 피한다. 공식 FAQ에 따르면 schema는 비엄격(non-strict)이어서 오타를 조용히 무시할 수 있으므로 `doctor`가 의미 있다.
- `SKILL.md`/Rule/Subagent의 형식과 frontmatter: upstream Rulesync가 읽는 것에 대해서는 **공식 parser/validator/generator**를 우선한다. 단순 전 파일 존재·키 타입 검사기를 추가하지 않는다.
- `targets` 명시와 같이 **저장소가 upstream보다 엄격하게 선언한 계약**: upstream이 허용해 버리는 문제일 때만 소규모 자체 검증을 검토한다.
- `rulesync.lock`의 모든 field/type/hash: upstream-owned lock contract다. 전체 구조를 모사하지 않고 `install --frozen`과 repository-owned route/projection 관계로 충분한지 검증한다.
- Route 생성기·파일 명명 충돌·선택 순서 등 **repository-owned behavior**: 최소 대표 사례와 오류 경계에 대한 pytest를 유지한다.

## 다음 작업

1. [GitHub transport 유지 요청](rulesync-github-transport.md)에 따라 Git 전용 설치 분기를 제거한다.
2. 제안서의 **최소 merge-critical 검증**을 기준으로 Rulesync 검증 단위를 나눈다: 루트 source/lock, 재사용 라이브러리, repository-owned route.
3. 독립성이 없는 테스트를 줄인 후 이전 테스트가 잡았던 실패를 **어떤 체크가 대신 탐지하는지** 확인한다. 검출 수단이 없다면 테스트를 제거하지 않는다.
4. 변경 후 실제 검증 결과(필요한 명령·커밋·PR Gate)를 새 HEAD에 대해 기록한다.

## 근거와 한계

- 저장소: [CI 정책](../../docs/development/ci.md), [Testing](../../docs/development/testing.md), [Validation](../../docs/development/validation.md), [Rulesync 통합 문서](../../docs/development/tooling/rulesync.md)
- Rulesync v16.24.1: [CLI 명령](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/reference/cli-commands.md), [Declarative Sources](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/guide/declarative-sources.md)
- Rulesync FAQ: [unknown keys / doctor](https://rulesync.dyoshikawa.com/faq.html)

**상태: 검토 완료, 최적화 구현·재검증 미실시.**
