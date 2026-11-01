---
description: PR #257에서 사용하는 Rulesync v16.24.1의 자체 진단·생성 검사·frozen 설치 기능과 저장소 검증의 중복 및 공백을 구분한 조사 보고서입니다.
---

# PR #257 — Rulesync 자체 테스트·검증 기능 조사

> **버전 기준 알림 (2026-10-24):** 아래 본문은 업그레이드 **이전 v16.24.1**을 대상으로 수행한 역사적 조사다. PR #257에서 `mise.toml`의 pin을 **v40.2.0**으로 변경했다. 40.x 공식 변경점과 아직 수행하지 않은 CLI·lock migration 검증은 [v40 업그레이드 조사·계획](rulesync-v40-upgrade-plan.md), 실행 인계는 [인계 보고서](rulesync-v40-handoff.md)를 따른다. 아래의 16.x 실행 상태를 v40.x에서의 통과 근거로 인용하지 않는다.

## 결론

**Rulesync 자체 검증 기능은 있다. 별도의 공개 CLI `rulesync test` 또는 `rulesync validate` 명령이 있는 것은 아니다.** 이 저장소가 고정한 **v16.24.1**은 이미 다음을 제공한다.

- **`doctor --strict`**: `rulesync.jsonc` / `rulesync.local.jsonc`의 구문, 설정 키·타입, 지원 target/feature 및 설정 충돌을 진단한다.
- **`generate --dry-run`**: 실제 벤더 출력 파일을 쓰지 않고 configured asset의 읽기·파싱·변환 경로를 실행한다. *생성 가능성 점검*이지, 출력이 최신인지의 판정은 아니다.
- **`generate --check`**: 생성 결과와 현재 출력 파일의 차이가 있으면 실패한다. *커밋된 vendor projection의 최신성 검사*에 적합하다.
- **`install --frozen`**: `sources`와 잠긴 ref/lock의 일치 여부를 확인하면서 원격 artifact를 설치한다. **read-only/offline 검사가 아니다.**
- **`--json`**: 명령의 성공/실패와 warning을 기계 판독할 수 있다. 자체 테스트 framework가 아니라 CLI 결과 전달 방식이다.

따라서 **Rulesync가 소유하는 config schema나 source frontmatter의 field/type을 Python·pytest로 다시 정의하지 않는 방향이 맞다.** 다만 `doctor`는 자산 본문을 검사하지 않으며, `generate`는 이 저장소만의 `targets` 명시 규칙·route 관계·모델 행동을 보장하지 않는다. 현 `rulesync_validate.py`의 warning 승격은 Rulesync가 경고로 넘기는 상황을 fail-closed로 처리한다는 점에서 남길 이유가 있다.

조사 대상: [PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257), head `100856dd2ce4d049ad6d655791a98aca0e3f3177`, Rulesync 버전 [`mise.toml`](../../mise.toml)의 `npm:rulesync = 16.24.1`. **공식 v16.24.1 태그 문서·소스와 저장소 파일을 정적으로 대조했다. CLI 직접 실행, 고장 주입, 설치 실험은 하지 않았다.**

## 자체 기능별 보장 범위

| 기능 | upstream에서 확인한 검증 | **검증하지 못하는 것 / 주의** | PR #257에서의 용도 |
| --- | --- | --- | --- |
| `rulesync doctor --strict` | JSONC 파싱, 알 수 없는 상위 키, 잘못된 target/feature, 설정 충돌, source 설정의 구조/타입, 일부 경로·schema 경고를 오류로 판정 | `SKILL.md` 본문·각 자산의 의미, 원격 파일 존재, lock 무결성. **설정 파일 부재도 info일 뿐 실패하지 않을 수 있음** | 루트와 라이브러리 각각의 설정 검증 |
| `rulesync generate --dry-run` | 설정된 targets/features의 파서·source loader·adapter를 실행해 생성 예정 사항 표시; 파일 write 없음 | output drift가 없어야 한다는 보장은 없음. 일부 feature의 invalid source는 **warning + skip**일 수 있음 | 라이브러리 source의 최소 생성 가능성 확인 |
| `rulesync generate --check` | 생성 결과와 관리 대상 output이 다르면 exit 1; write 없이 drift 탐지 | output을 커밋하지 않는 workspace에 무조건 적용하면 아직 생성하지 않은 정상적인 산출물도 drift로 판단 | vendor projection을 버전 관리하는 경우에만 적용 |
| `rulesync install --frozen` | 선언한 source와 기존 lock의 정합성, 잠긴 revision의 dependency fetch/install | 네트워크/인증 의존, curated artifact write 발생; 모델/벤더 행동 검증 아님 | **루트 `rulesync.jsonc`/`rulesync.lock` 변경 시** 후보 검증 |
| `rulesync --json <command>` | 성공 여부·warning 및 진단 결과의 machine-readable 전달 | `doctor --strict` 이외 명령의 warning을 언제나 nonzero exit로 승격하지는 않음 | 경고까지 실패시켜야 하는 repo wrapper의 좁은 역할 |
| Rulesync upstream `pnpm test` / `test:e2e` | Rulesync **개발자가 Rulesync 구현 자체**를 검사하는 Vitest suite | 설치된 소비자 프로젝트의 설정/자산을 검사하는 `rulesync test` 명령이 아님 | CI에 복제하거나 프로젝트별로 실행할 필요 없음 |

**판독 유의:** `generate`는 기능별로 오류 처리가 다르다. v16.24.1 문서는 malformed rule/command/skill frontmatter는 실패할 수 있으나, **subagent 및 check 자산은 warning을 내고 건너뛸 수 있다**고 명시한다. 따라서 `generate --dry-run`의 **exit code 0만으로 모든 입력이 유효하다고 판단하면 안 된다.** 현재 wrapper가 `--json`의 `warnings`를 실패로 보는 것은 실제 검출 범위를 늘린다.

## PR #257의 실제 검증과 겹치는 부분

| 저장소 현 상태 | 판단 |
| --- | --- |
| [`npm run rulesync:validate`](../../package.json) → [`scripts/agent_assets/rulesync_validate.py`](../../scripts/agent_assets/rulesync_validate.py) | 라이브러리 `src/rulesync`에서 이미 `doctor --strict` + `generate --dry-run` 실행. **upstream 기능을 활용 중**이며 새 field/type validator가 아님 |
| 같은 wrapper의 JSON 성공·warning 처리 및 [8개 pytest](../../tests/scripts/agent_assets/test_rulesync_validate.py) | upstream schema에 대한 테스트가 아닌 **repository-owned adapter** 테스트. 명령 실행·warning fail-closed 같은 최소 계약은 보존하되, 오류 JSON의 모든 형식 변형까지 유지해야 하는지 축소 검토 가능 |
| [`.github/workflows/pr-gate.yml`](../../.github/workflows/pr-gate.yml) | Rulesync 검사 단계가 **재사용 라이브러리에 한정**됨. 변경한 루트 `rulesync.jsonc`/`rulesync.lock`의 실제 frozen 설치 검증은 없음 |
| [`mise run rulesync-install`](../../mise.toml) | 설치 entrypoint는 있지만 PR Gate는 실행하지 않음. 이번 PR의 Git transport/인증 환경 문제를 지금의 green CI로 증명할 수 없음 |
| 자체 route generator와 projection drift 검사 | Rulesync vendor 기능이 아닌 **이 저장소가 소유한 관계**를 검사하므로 유지 대상 |

**두 workspace를 섞지 말 것.** 루트의 `rulesync.jsonc` + `rulesync.lock`은 dependency **소비자**이고, `src/rulesync/.rulesync/`는 authored asset **라이브러리**다. 라이브러리의 `doctor`/dry-run이 성공했다고 루트 source 설치가 검증되지는 않는다.

## 질문별 판단: 파일·필드·타입까지 테스트해야 하나?

1. **공식 입력 구문, JSONC key, value type, target/feature enum:** *검증은 필요하나 직접 구현한 단위 테스트는 기본적으로 불필요하다.* 각각 해당 workspace의 `doctor --strict`에 맡긴다.
2. **`SKILL.md`, rule, subagent의 frontmatter/type·변환 호환성:** `generate --dry-run` + **warning 검사**로 Rulesync가 실제 해석하는 입력을 검증한다. 이 검사의 성공을 모든 frontmatter key의 존재, 사용자가 의도한 의미 또는 전체 target compatibility의 증거로 확대하지 않는다.
3. **원격 source 선택, lock 불일치, 의존 Skill 다운로드:** 루트의 `install --frozen`으로 확인한다. lock field/hash를 읽어 새 schema를 작성하지 않는다.
4. **이 저장소만의 추가 계약:** reusable asset이 `targets`를 반드시 명시해야 하고 `["*"]`는 안 된다는 규칙, route family/source mapping, index·route 생성 결과 등은 **upstream이 소유하지 않으므로 좁은 자체 검사 유지 또는 필요 시 추가**.
5. **LLM의 Skill 활성화·품질·실행:** Rulesync CLI는 평가하지 않는다. 변경 영향이 실제로 요구할 때만 별도 Eval/smoke를 한다.

예외: `doctor`가 설정 파일 누락을 `info`로만 보고할 수 있으므로, 파일 존재 자체를 **저장소가 필수로 지정한 경우**에 한해서 그 존재 여부는 별도 경계에서 확인한다.

## 권고: 충분한 최소 검증 구성

**당장 중복 schema validator를 추가하지 않는다.** 기존 CI 구조를 유지하면서 아래 순서로 검증 대상을 명확히 한다.

1. **루트 config:** PR Gate에서 루트 cwd의 `rulesync doctor --strict` 추가를 검토한다. 필요하다면 mandatory root config 존재 여부만 별도 검사한다.
2. **라이브러리:** 기존 `npm run rulesync:validate` (`doctor --strict`, `generate --dry-run`, warning fail-closed)를 유지하되 wrapper 테스트는 검출력이 보존되는 최소 대표 사례 위주로 간소화한다.
3. **루트 설치 변경:** `rulesync.jsonc` 또는 `rulesync.lock` 변경 시 ephemeral runner에서 `rulesync install --frozen` 및 **lock 불변 여부**를 확인한다. 프로젝트가 사용하는 인증·Git/HTTPS transport·네트워크가 실제 작동하는지까지 확인하는 단계이므로 정적 검사보다 비용이 크다. 접근 장애는 명확히 실패 원인으로 드러내고 임의로 통과시키지 않는다.
4. **vendor output drift:** 이 저장소가 커밋하지 않는 vendor projection에는 `generate --check`를 기본 PR gate로 강제하지 않는다. 커밋하는 projection은 existing official generator + diff로 검사한다.
5. **repository-owned route와 Python 실행 로직:** 기존 deterministic pytest와 generated projection gate에서 검증한다. Rulesync 공식 테스트 suite를 프로젝트에 복사하지 않는다.

새로운 CI 프레임워크, 모든 OS의 상시 매트릭스, 모든 파일/필드의 snapshot은 지금 단계에서 권고하지 않는다. 검증 수준 변경 전에 **의도적으로 설정 key 오타, 잘못된 authored frontmatter, warning-only subagent, stale lock, stale route**를 각각 한 번씩 만들어 어느 단계가 실패시키는지 확인하면 충분하다. 이 고장 주입 확인은 **권고**이며 이번 조사에서 수행하지 않았다.

### 실제 명령의 작업 위치

```bash
# repository root: root config를 검증
rulesync doctor --strict

# reusable library: authored sources를 검증 (실제 현재 CI 경로)
npm run rulesync:validate
# 개별 native 명령을 직접 확인할 때만:
(cd src/rulesync && rulesync doctor --strict && rulesync generate --dry-run)

# CI 임시 checkout에서만: root config/lock 변경 시 dependency 검증
rulesync install --frozen
git diff --exit-code -- rulesync.lock
```

`install --frozen`은 curated 디렉터리에 쓰거나 외부와 통신하므로 사용자 checkout에서 무조건 read-only 검증으로 실행하지 않는다. 실제 CI 추가 시 자격 증명과 git 환경, 경로 조건을 함께 검토한다.

## 근거 및 검증 상태

### Upstream v16.24.1 (**현재 고정 버전의 직접 증거**)

- [공식 CLI 명령 — `doctor`, `generate`, `--json`](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/reference/cli-commands.md)
- [공식 Dry Run 안내 — `--dry-run`과 `--check` 차이](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/guide/dry-run.md)
- [공식 Declarative Sources — 설치·lock·frozen 모드](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/docs/guide/declarative-sources.md)
- [CLI 등록 소스 — 공개 subcommand 확인](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/src/cli/program.ts)
- [`doctor` 구현](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/src/cli/commands/doctor.ts), [`install` 구현](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/src/cli/commands/install.ts)
- [upstream `package.json` — 개발자용 test scripts](https://github.com/dyoshikawa/rulesync/blob/v16.24.1/package.json)

### Repository와 기존 검토

- [Rulesync 운영 문서](../../docs/development/tooling/rulesync.md), [Validation](../../docs/development/validation.md), [Testing](../../docs/development/testing.md), [CI](../../docs/development/ci.md)
- [Rulesync CI·테스트 리뷰](rulesync-ci-test-review.md), [검증 최적화 제안](rulesync-verification-proposal.md)

**✅ 확인:** 고정 버전 공식 태그의 명령·소스와 현 PR 구성의 정적 대조.  
**⚪ Not Verified:** v16.24.1 CLI를 실제 설치하여 실행한 결과, 고장 주입, 이번 head의 root frozen 설치, OS별 동작, 새 CI 반영 여부.

**상태:** 조사·보고서 완료. CI·코드 변경은 이 문서에 포함되지 않으며 별도 작업이다.
