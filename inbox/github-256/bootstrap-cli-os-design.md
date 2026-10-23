# Bootstrap CLI / OS 설계 인계

> PR #256 · 2026-10-24. **구현 전 제안**. 근거: [CLI/OS 조사](bootstrap-cli-os-research.md), [UX 설계](bootstrap-ux-design.md). 본 문서의 명령은 현재 기존 `mise.toml`에서 제공되는 범위와 향후 구현 예정인 범위를 구분한다.

## Minimal UX contract

사용자가 기억할 명령은 `mise run setup`(최초·반복 복구), `mise run update`(명시적인 허용 범위 내 갱신) 두 개다. `mise` 설치와 현재 지원 플랫폼 안내는 실행 시작 전 prerequisites다. 기존 `mise run check`와 `mise run test`의 역할을 혼동하지 않는다.

### CLI 진입점 제안

| 기능 | 현재 구현 | MVP 목표 | 도입 가드 |
| --- | --- | --- | --- |
| `mise run setup` | 존재; ordered `run` array, lock mutation 가능성 있음 | locked reconcile, 권한 검사, 안전한 partial recovery와 summary | clean/warm/native OS 테스트 |
| `mise run update` | **없음** | 선언된 허용 version requests로만 native lock resolution/install/verify | bounded update+sidecar tests |
| `mise tasks ls` / `mise run setup --help` | mise 자체 제공 가능 | 한눈에 알아볼 description/help; unknown flag 거부 | 사용 버전의 `usage` 여부 확인 |
| `mise run --dry-run setup` | mise native option, 설치기별 dry-run 아님 | 실행할 mise tasks preview만; 전체 변경 예측으로 오인 금지 | tool pre-install side effect 검증 |
| `mise run setup --dry-run` | **구현 안 됨** | 별도 기능을 입증하기 전에는 지원한다고 안내하지 않음 | run array 인자 전달 문제가 먼저 해결돼야 함 |
| `mise run update --dry-run` | **미구현** | 모든 lock/source/version candidate에 대한 실제 read-only preview 가능할 때만 | resolver side effect == 0 증명 |
| `--verbose` / `--non-interactive` | 미구현 | 필요하면 실제 runner별 구현 후, 스펙 1개로 제공 | CI/no-TTY arg tests |
| `--yes` / `--force` / `--os` / `--global` | 미구현 | 기본 공개 제외 | 권한·호환성 우회 방지 |

가장 먼저 개선할 부분은 **`setup`을 제어하는 방법**이지 인자 목록을 늘리는 것이 아니다. 기존 배열형 `run`에는 실행 인자가 마지막 command에만 전달된다. 초기 구현은 0개 인자 안정성을 먼저 확보하고, 범위 넓은 flag는 runner wrapper 또는 mise `usage` spec과 연결 테스트 후 공개한다.

### Flag 위치 및 파서 결정

- mise 자체의 옵션: `mise run --dry-run setup`처럼 **task 이름 앞**.
- bootstrap 전용 인자: 검증해 제공하는 경우에만 `mise run setup --some-flag`처럼 task 이름 뒤.
- Validated usage: `usage`가 합법 값 검증, help, completion 소유. Python `argparse`를 사용한 wrapper라면 `raw_args`와 `--help` 전달 계약을 명확히 한다.
- 로컬 debug 목적은 기존 mise verbose/native command로 먼저 해결. 유사한 이름의 flags가 서로 다른 수행 단계에 다른 의미를 주지 않게 한다.
- 별도 CLI 문법/enum을 소유하지 않고 실제 user intent가 있는 옵션만 선언. 파일 경로·토큰·OS 이름을 사용자 입력으로 받아 문자열 기반 shell을 만드는 것은 피한다.

## Platform resolution contract

**지원/검증 상태와 자동 OS 감지를 분리한다.** 예: WSL에서 `platform.system() == "Linux"`일 수 있으나 WSL/Windows path semantics가 같다거나 Linux binary 설치 상태가 준비됐다는 뜻은 아니다.

### 탐지할 정보 (필요한 경우)

1. Runtime OS: Windows / macOS / Linux, architecture x64/arm64, Linux에서 필요한 경우 libc glibc/musl 및 distro release.
2. Execution mode: Windows PowerShell/cmd/Git Bash, WSL Linux, Unix sh/bash/zsh, non-TTY/CI; runner가 선택한 shell의 availability/version.
3. Runtime capability: mise/uv/Git/Bash/Node/Rulesync/Lefthook 등 필요한 명령과 version, PATH resolution, platform artifact 사용 가능 여부.
4. Working directory: repository root, tracked config/lock, current filesystem 성질. WSL + Windows-mounted location은 **성능 경고**이지 무조건 실패로 취급하지 않는다.
5. Installation authority: managed cache, project local, user-home, OS-global 중 어디를 변경하는지와 permission/승인.

OS fingerprint에는 개인 디렉터리·사용자명 등 식별 데이터를 기본 출력하지 않는다. OS/version과 capability만으로 진단 가능하면 나머지는 수집하지 않는다.

### 플랫폼별 MVP acceptance matrix

| 대상 | 셸·runtime | 요구 검증 | 현재 결론 |
| --- | --- | --- | --- |
| Linux x64, glibc | sh/bash | clean setup / repeat / bounded update / missing Git/Bash | **CI에 Ubuntu Linux 검증만 존재. bootstrap E2E 미검증** |
| Linux arm64, glibc | sh/bash | managed tools binaries/native Skill installer availability | 미검증 |
| Linux musl | sh | glibc-only binary 여부와 unsupported 메시지 | 미검증. 지원을 가정하지 않음 |
| macOS x64 | sh/zsh | 첫 설치·cache·Git hooks·platform lock | 미검증 |
| macOS arm64 | sh/zsh | native arm64, Rosetta 유무, Apple tool artifact | 미검증 |
| Windows native | PowerShell 또는 cmd.exe | `run_windows`, native tool install, quoted paths, Git hooks, optional Bash installer | 미검증; mise 자체는 native Windows 지원 |
| Windows Git Bash | MSYS2 shell + Windows executables | 경로 변환/quote, native Git·Bash, HOME 동작 | 미검증 |
| WSL2 | Linux runtime + Linux toolchain | Linux filesystem/repo 위치, Windows exe 혼동, PATH | 미검증 |
| Linux CI/non-TTY | Ubuntu runner | non-prompt, read-only validation, exit code | 기존 PR CI 통과는 특정 validation만 증명 |

**릴리스 범위:** MVP에서 지원 검증을 통과한 조합만 official supported로 기록한다. 나머지는 "지원 미확인/시도 가능"으로 표현한다. Windows가 mise 자체를 지원한다고 Skill installer까지 자동 통과한다고 주장하지 않는다. Alpine/musl, ARM64는 해당 artifact 가능 여부를 개별 조사한다.

### Cross-platform 구현 전략의 선택지

**A. Simple native TOML commands 유지.** 현재처럼 `uv sync`, `rulesync install`처럼 shell-independent한 단일 명령만 실행하면 OS 분기가 거의 필요 없다. 우선 선정.

**B. OS별 작은 task delta.** bash-specific / PowerShell-specific 명령이 필요한 단계만 `run_windows` 또는 OS별 script를 사용. 쉬운 검증·수정 가능. Windows용 별도 전체 bootstrap을 복제하지 않는다.

**C. Python-based scoped orchestrator.** 여러 tool의 optional/required dependency, preflight/report, process args/exit, paths, OS details에 공통 실행 규칙이 실제 필요하고 Python을 uv로 마련할 수 있을 때만 도입. Python script 자체는 첫 uv 준비 전 실행할 수 없으므로 **entrypoint prerequisite chain**을 설계해야 한다. `subprocess.run([...], shell=False)`, `pathlib` 등 argv/path-aware API 활용; no sudo/OS-package-manager.

**D. Full machine manager 또는 Nix/Container migration.** Host configuration 자체를 소유해야 하는 요구가 없는 현재 PR에서는 기각. 기존 tools/lock과 dual-authority 비용을 감수할 근거 없음.

선택 순서: A→B, A/B로 required graceful degradation을 구현할 수 없다는 검증 근거가 있을 때만 C. OS별 unsupported platform은 조용히 성공 처리하지 않는다.

## 출력·오류·비대화형 UX

**출력 예시는 목표 계약이며 구현된 결과가 아님.**

```text
$ mise run setup
Preflight: windows-x64 / PowerShell / non-TTY=false
  [ready]      project toolchain
  [blocked]    external Git/Bash: not installed
  [ready]      Python project dependencies
  [skipped]    user-home Skill: explicit approval needed

Result: READY or DEGRADED or BLOCKED (depends on required policy).
Next: install missing prerequisite using the official instructions; rerun setup.
```

출력에 OS fingerprint를 표시할 때 PATH, HOME full path, token 등을 기본 노출하지 않는다. 실제로 존재하지 않는 도구나 버전이 설치된 것처럼 표시하지 않는다.

- `READY`: 필수 준비 검증 전부 통과, exit 0.
- `DEGRADED`: **선택적** 단계만 미완료; exit 0(정책 초안), missing item과 명시적 next action.
- `BLOCKED/FAILED`: 필수 준비 미완료, nonzero, 누락 조건·실패 단계와 복구 방법.
- `UPDATE_NOOP`: exact pin/허용 후보 없음, exit 0와 이유.
- Non-TTY: 대기하는 prompt나 spinner 없음, 원치 않는 shell activation/privilege elevation 없음; log redaction.
- Interrupt/retry: Ctrl-C/timeout 시 partial state를 기록하고 lock을 덮어쓰지 않으며, 재실행으로 복구. Shared installer concurrent calls 방지.

## 구체 검증 시나리오

| ID | 입력/환경 | 기대 |
| --- | --- | --- |
| A01 | `mise run setup` 기본 | flags 없이 setup 동작과 summary 일치 |
| A02 | `mise run setup --unknown` | 속성 미지원이면 **실행 전** reject, side effect 0 |
| A03 | `mise run setup --dry-run` | 지원하지 않으면 실행 전 reject; 마지막 단계에 인자 전달·설치 진행 금지 |
| A04 | `mise run --dry-run setup` | native task preview만 제공; 실제 OS installer 변경 결과로 오해 금지 |
| A05 | `mise run update --dry-run` | 구현할 경우 모든 resolver/installer write 0, lock/sidecar diff 0 |
| A06 | `--yes` 등 미승인 flag | user/global installation 권한 부여하지 않음 |
| A07 | help/typo | 설명된 command/flags만 제시, command typo는 친절히 reject |
| A08 | Linux/macOS/Windows shell | argv, space/Unicode path 전달 동등성 확인 |
| A09 | Windows native / WSL2 | 서로 다른 tool cache와 PATH, Linux/Windows binary 잘못 실행하지 않음 |
| A10 | CPU arm64, Linux musl | install artifact 없음은 BLOCKED/UNSUPPORTED, 자동 전역 설치 금지 |
| A11 | `git`/`bash` 없으나 uv 가능 | 독립 Python 준비는 계속; native Skill 단계는 skip/block |
| A12 | `core.hooksPath` 설정 존재 | Lefthook 강제 리셋 금지, 문서화된 사용자 조치 |
| A13 | no-TTY, CI, env HOME missing | prompt 없이 종료, 오류/상태를 machine-readable exit로 구분 |
| A14 | WSL repo mounted Windows FS | 위치 감지(가능하면), 안내만 하고 setup 차단하지 않음 |
| A15 | dirty user files, Ctrl-C | 자동 덮어쓰기·rollback 금지, 재실행 가능 |
| A16 | native tool auto-install 선행 단계 | 승인하지 않은 tool/global 변화 0; preview 주장과 실제 side effect 일치 |

**검증 층위:** 우선 정적 contract/unknown flag tests → mock executable + isolated temp HOME → OS별 isolated smoke → clean-machine cold/warm E2E. GitHub Actions Ubuntu 검사만으로 macOS/Windows 성공을 보고하지 않는다.

## 우선 구현 계획

1. **P0 CLI 안전성:** 기존 mise 배열형 `run`의 task args 전달 위험 제거/사전 차단, 사용 도구 설치 범위, 정확한 bootstrap state 종료 코드.
2. **P0 OS 안전성:** 실제 OS/shell/capability 탐지, native Windows/MSYS2/WSL 구분, user/global installer guard, Python interpreter shell chain 검증.
3. **P1 UX:** 필수 0 args·help/description, optional read-only preview와 next action, non-TTY 규칙.
4. **P1 호환성:** 최소 지원 OS/arch/shell target을 정해 Tool 7개 + optional installer + hooks capability test.
5. **P2 성능:** cold/warm, macOS ARM64 vs Intel, WSL Linux FS vs Windows mount 실측. 불필요한 프로세스 실행/네트워크와 plugin 설치를 줄인다.
6. **보류:** JSON 출력 schema, 대규모 flag matrix, cross-OS installer wrapper, 전체 OS 자동 업그레이드.

이 설계는 `mols-dev-env-bootstrap-design` Skill의 일반 설계 판단을 실제 repository에 적용한 **로컬 delta**이다. 실행지침의 정본은 Skill, 실제 CLI 동작의 정본은 코드/버전별 도구 문서에 남긴다.
