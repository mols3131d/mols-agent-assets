# Developer bootstrap: CLI, 인자, OS 호환성 조사

> PR #256 · 2026-10-24. **조사 근거와 선택지**를 기록한 inbox 아티팩트이며 현재 구현 또는 검증된 플랫폼 지원 선언이 아니다. 상위 연구: [bootstrap-deep-research.md](bootstrap-deep-research.md). 실행 계약 초안: [bootstrap-cli-os-design.md](bootstrap-cli-os-design.md).

## 조사 질문 / 범위 / 증거

- 사용자가 첫날과 평소에 기억해야 할 **명령 수와 인자 수**는 최소 얼마인가?
- `mise run setup`, `mise run update`의 `--help`, `--dry-run`, `--yes`, `--verbose`, `--json`, `--only` 등은 실제로 어디까지 전달되는가? 무슨 부작용을 보장할 수 있는가?
- Windows native, Windows WSL, macOS Intel/Apple Silicon, Linux 배포판·libc/CPU 종류를 어떻게 인식·지원·진단하는가?
- OS별 셸, path, privilege, package manager, 캐시, Git hooks, 외부 설치기 차이가 실패·성능·UX에 미치는 영향은?
- 실제 설치와 mock/test가 없는 상태에서 어디까지 확실하게 권장할 수 있는가?

**방법:** mols-loops 기반 Research → Plan → Work(공식 소스 비교·기존 코드 확인) → Review, 조건을 추가한 재조사 후 최종 판단. repository head는 조사 시작 시 `8772df89d2589c969a5aef4cb3455577755a5121`. 기존 `mise.toml`과 `skills_sync.py`는 GitHub Plugin에서 현재 브랜치의 원본을 읽었으며, 외부 CLI semantics는 문서 끝의 공식 소스와 대조했다. 벤더의 최신 문서가 이 저장소에 pin한 도구 버전과 같다는 가정은 하지 않는다.

## Loop 1: 실제 CLI UX와 인자 전달 분석

### 현재 repository의 입력 표면

- `mise.toml`: `setup`은 5개 명령의 `run` 배열. `update`와 bootstrap-only `doctor`/`preview`는 아직 없음. `check`·`test`는 별개 진입점.
- `scripts/agent_assets/skills_sync.py`: Python `argparse`에서 `--dry-run`만 받아 lock source와 adapter를 출력. 실제 설치 대상의 현재 상태 확인은 하지 않음. Git clone/checkout, Bash-native installer 실행은 외부 user-level side effect.
- `lefthook.yml`: mise, uv, Python, Git hook 연동 경로. OS, shell, PATH, Git hooks 설정이 영향을 줌.
- `.github/workflows/pr-gate.yml`: Ubuntu Linux의 제한된 설치만 검증. 이 통과만으로 macOS, Windows native/WSL 지원을 보장할 수 없음.

### 공식 mise CLI 인자 semantics

| 기제 | 확인된 의미 | 부트스트랩 UX 위험 |
| --- | --- | --- |
| `mise run TASK [ARGS]` | task 이름 **뒤**의 인자는 task로 전달; mise 자체 옵션은 task 이름 앞에 배치 [S1] | 중첩 호출에서 mise flag와 task flag 충돌 |
| `run = ["cmd1", "cmd2"]` | usage spec 없으면 추가 인자는 **마지막 배열 항목**에만 전달 [S1] | `mise run setup --dry-run`이 전체 작업을 preview한다는 오해. 마지막 `lefthook install`에 전달될 수도 있음 |
| `usage = '...'` | 구문·choice validation, per-task `--help`와 completion, `usage_<arg>` 또는 template map 제공 [S2] | validator의 값을 실제 installer에 전달하는 연결을 따로 구현해야 함 |
| `raw_args = true` | 자체 argument parser가 있는 하위 프로그램으로 모든 인자를 넘김. `--help`도 forwarding [S3] | 간단한 task 공용 스펙보다 별도 wrapper가 적합한 경우에만 |
| `mise run --dry-run TASK` | mise의 task 실행 계획을 미리 보는 것. upstream 각 installer가 어떤 파일을 바꿀지는 **보장하지 않음** [S1] | `--dry-run`이라는 단어만 같아도 단계별 preview와 결과 정확도가 다름 |
| `run_windows` / `shell` | Windows 전용 command 정의 가능. 기본 inline shell은 Unix `sh`, Windows `cmd /c`. 명시적 PowerShell 설정에서는 `-NoProfile` [S3] | bash-ism, PowerShell 변수 문법, 복합 command quote가 달라짐 |
| `dir` | 기본 task cwd는 config root, 기존 사용자의 cwd와 다를 수 있음 [S3] | 상대 경로, subprocess 실행 대상 혼동 |
| `confirm` / `interactive` | task별 prompt와 terminal 권한 제공 [S3] | confirm 이전 dependencies 실행 가능성, non-TTY hang; 'user scope opt-in'의 안전 경계가 되어야 함 |
| `task.run_auto_install` | 사용 도구가 task 시작 전에 설치될 수 있음 [S4] | script 내부의 `--dry-run`·`--no-install`만으로 선행 설치를 통제할 수 없음 |

**첫 번째 결론:** 지금 `setup`에 flag를 추가하는 것은 UX 설계가 아니라 **위험한 API 변경**이다. Task-level flags를 구현한다면 parsing, pre-task auto-install, 전체 step forwarding, validation, exit code를 함께 검증해야 한다. `mise run --dry-run setup`은 도구별 변경 diff와 동등하지 않다.

### 후보 인터페이스 비교

| 안 | 장점 | 단점 | 판단 |
| --- | --- | --- | --- |
| ① `setup` / `update`, 기본 0개 필수 arg | 학습 비용 최소, daily use 간결 | 상세 제어는 별도 명령 필요 | **우선 권고** |
| ② 두 command + 최소 `usage` flags | `--help`, completion, validation 제공 | shell 간 전달·side effect 부주의 위험 | **조건부 검토**: 구현 이후 |
| ③ 새 Python CLI `bootstrap setup --...` 전체 도입 | 명확한 parser, cross-platform 로직 | uv/Python 준비 이전에 실행 불가, 추가 wrapper 책임 | **기본 기각** |
| ④ 모든 flags: `--os`, `--arch`, `--all`, `--force`, `--global` | 제어권이 많아 보임 | 상태 조합 폭증, 환경 오판·권한·안전 경계 우회 | **기각** |

**실용적인 옵션 축**: 필요한 경우에만 `--dry-run`(read-only & real installer skip 증명), `--verbose`(문제 진단), `--non-interactive`(확실한 실패/skip) 등을 도입한다. `--yes`를 도입하더라도 전역 설치 권한으로 해석하지 않는다. `--force`는 guard 우회이므로 기본으로 노출하지 않는다. `--os`나 `--arch`로 실제 host를 속여 설치하게 만드는 기능은 불필요하다. Cross-compile artifact 선택과 실제 실행 플랫폼 탐지는 별개의 concern이다.

**CLI 도움말 최소 목표**: `mise tasks ls`에서 목적이 읽혀야 하고, 각 명령의 도움말은 setup vs update 의미, 변경 scope, preview/no-op, 실패 시 복구를 설명한다. 상세한 vendor command 목록을 flags로 모두 복제하지 않는다.

## Loop 2: 운영체제·환경 모드 분해

**OS 하나로 충분하지 않다.** Host OS, execution environment, shell, machine architecture, C library, filesystem, privilege, network·proxy, installed backend가 독립적으로 영향을 준다. Detection은 **실제 프로세스가 실행되는 환경**에서 수행하며 env var 하나의 추정만으로 vendor installer를 선택하지 않는다.

| 실행 환경 | 진입점 / shell | 주요 실패 위험 | 설계 권고 |
| --- | --- | --- | --- |
| Linux x86_64 glibc | mise Linux + sh/bash 선택 | distro/system library, missing Git/curl, mirror/CA, 권한 | Linux generic support를 선언하더라도 supported distro/libc 명시 |
| Linux ARM64 | Linux shell + arm64 바이너리 | 특정 CLI artifact 부재, npm native dependency | 각 관리 도구의 arm64 install 가능 여부 별도 probe |
| Alpine/musl | Linux shell, musl libc | glibc 전용 prebuilt binary 호환 안 됨 | glibc Linux 통과로 musl supported 선언 금지 |
| macOS Intel | mise macOS, zsh/sh | x86_64 tool release, Gatekeeper, Homebrew 구성이 다름 | macOS arch 구분, OS-global brew 자동 설치 금지 |
| macOS Apple Silicon | mise macOS arm64 | Rosetta 혼합, shell architecture와 binary arch 불일치 | native arm64 우선, x64 fallback은 tool별 승인·진단 |
| Windows native PowerShell | mise native Windows + pwsh/PowerShell/cmd | 명령/경로 quote, PATHEXT, CRLF, permission, admin, user PATH | `run_windows` 또는 cross-platform executable 도입; POSIX shell 가정 금지 |
| Windows Git Bash/MSYS2 | Windows 실행파일 + POSIX-like shell | Windows vs MSYS path 변환, Git/Bash 존재와 권한 오판 | Windows native로 분류하되 shell identity를 별도로 기록 |
| WSL2 Linux | Linux mise/uv/Git/bash | Windows exe와 Linux exe 혼합, `/mnt/c` I/O 저하, 경로·ENV 혼동 | 별도 Linux runtime으로 취급, Linux FS 작업 권고 [S8] |
| CI/non-TTY/container | Linux/Windows/macOS runner, no tty | stdin prompt, spinner, privileges, CI PATH, artifact/cache drift | non-interactive default, 다른 승인 방식, CI는 correctness evidence와 분리 |

mise는 Windows native에서 PowerShell/shims/`mise exec`/`mise run`을 지원하지만 **asdf shell-script plugin은 native Windows에서 동작하지 않는다**. npm, aqua, github, vfox backend도 도구 자체가 Windows artifact를 제공해야 한다. WSL은 Linux mise를 별도 설치해야 하며 Windows 설치본을 직접 재사용한다고 가정할 수 없다. [S5][S6]

현재 `mise.toml`의 모든 tool이 각 platform에 설치된다는 것은 **확인되지 않았다**. platform support는 mise 바이너리 지원뿐 아니라 uv, Node, rumdl, Lefthook, Biome, Rulesync, skills CLI, upstream native Skill installer 전체를 대상으로 재확인해야 한다.

### OS 감지 및 기능 검사 결론

1. Host fingerprint: OS/kernel, version, architecture, libc(필요 시), shell, WSL/container, cwd/filesystem, interactive 여부, PATH에 설치된 실제 command 경로. 이 값 중 **의사결정에 사용하는 것만** 출력하거나 검증한다.
1. OS 이름은 초기 routing의 힌트다. 실제로 Git, Bash, uv, Node 등 명령 실행 가능 여부는 capability probe(`--version`, native diagnostic, PATH 확인)로 결정한다. Windows/WSL이므로 자동으로 설치되어 있다고 판단하지 않는다.
1. Python `platform.system()`은 Windows/Darwin/Linux kernel을 구분하지만 WSL은 Linux로 보이므로 subsystem 판정이 별도 필요하다. 환경변수 기반 판정은 spoofable이므로 보조 신호로만 쓰고 독립된 실행 capability를 확인한다.
1. `MISE_OS` 같은 tool-manager OS override는 **실제 host detection 증거가 아니라 target artifact 선택 설정**이다. `--os`를 진단 인자로 쓰더라도 실제 설치 정책을 바꾸게 해서는 안 된다. [S7]
1. OS별 설정 파일을 늘리기보다 공통 task로 시작하고 실제 필요한 최소 platform delta만 `run_windows` 또는 별도 script에 둔다. OS별 lock/platform artifact가 필요해도 명확한 owner가 확인된 후에만 채택한다.
1. PATH 충돌은 Windows에서 대소문자·확장자와 함께, Unix는 login/interactive shell activation과 함께 비교한다. `mise exec -- ...`는 사용자의 shell profile을 수정하지 않고도 project tools를 실행하는 경로다. [S5]

### 파일/경로/캐시/권한 UX

- Windows `C:\...`, drive letter, UNC path, spaces/Unicode, extension, CRLF, symlink permission을 shell 문자열 결합 대신 argv/path-aware API로 다룬다. POSIX의 `sh`/`chmod`/`rm` 명령이 native Windows에 존재한다고 가정하지 않는다.
- WSL에서 Linux tool로 프로젝트를 빌드한다면 Windows mount (`/mnt/c`)보다 WSL Linux filesystem(`~/projects`)가 일반적으로 빠르다. 이는 기능 지원을 막는 이유는 아니며 성능 진단과 안내에 활용한다. [S8]
- uv는 platform cache를 사용하고 같은 파일 시스템에서 cache와 venv를 두면 링크 효율이 높다. Windows 기본 hardlink, macOS/Linux 기본 clone(CoW); cache를 임의 정리하거나 symlink 모드를 기본 적용하지 않는다. [S9]
- OS-global package install, 관리자 승격, PowerShell remote install script 또는 Git Bash 설치는 기본적으로 사용자 안내만. 기계가 처음부터 `mise` 없이 시작하면 어느 OS에서도 `mise run setup`은 자기 자신을 설치할 수 없다.
- Git hook의 기존 `core.hooksPath`가 있으면 Lefthook 설치가 중지될 수 있다. `--force`와 `--reset-hooks-path`는 명시적 인간 결정이 없으면 쓰지 않는다. [S10]
- 로깅은 shell/terminal 별로 ANSI color 지원, CI/no-color, stderr, UTF-8, Unicode path를 고려한다. raw process output에 credential, token, HOME secret path 등이 나타나지 않도록 redaction 정책을 검토한다.

**Review:** 모든 OS에 동일한 user experience를 약속하는 것과 모든 OS의 설치기가 동일하다는 것은 다르다. 실제 capability가 없는 기능을 '지원'이라고 말하지 않고 **core ready / optional skipped / blocked with explicit instruction**으로 처리한다.

## Loop 3: 반례, 보안·운영 UX 검토

| 반례 | 방지할 실패 | 필요한 검증 |
| --- | --- | --- |
| 사용자가 `mise run setup --dry-run` 입력 | 마지막 Lefthook에만 플래그 전달 / 설치 선행됨 | 동일 커맨드에서 모든 write 0, 전체 step preview 또는 명확한 reject |
| 잘못된 `--os windows` 지정 | 실제 Linux 환경에 Windows 바이너리 설치 | host detection/target override 분리 |
| `--yes` + native installer | 무동의 HOME/global 변경 | privilege scope 별 explicit opt-in |
| PowerShell `--verbose` | shell parser가 task flag를 삼킴 | shell별 argv round-trip |
| Windows 경로에 한글/공백 | subprocess/quote 오류 | temp directory에 UTF-8·space path 테스트 |
| Unix shell에서는 되지만 cmd에서는 실패 | `sh`, `$HOME`, `&&` 가정 | supported shell contract 및 `run_windows` 검증 |
| WSL에서 Windows Git/Python 경로 혼용 | cache·.venv·Git path 불일치 | native Linux 실행 path probe |
| 플랫폼에 해당하는 npm package artifact 없음 | 자동 글로벌 설치 또는 실패 은닉 | per-platform supported/unsupported 보고 |
| `--no-color` 없는 CI | ANSI/spinner 때문에 로그 읽기 어려움 | `NO_COLOR` / no TTY 검증 |
| task 시작 전에 mise 자동 설치 | `--dry-run` 거짓 안전감 | pre-task auto-install 별도 확인 |
| 둘 이상의 update flag 충돌 | policy 우회, lock 손상 | unexpected flags early reject, atomic write scope |
| Ctrl-C/timeout/재실행 | partial state를 완전 성공으로 표현 | interruption state + idempotent retry |

추가로 안전성: Shell injection 회피(사용자 경로/옵션을 문자열 결합해 `sh -c`로 실행하지 않음), token masking, 관리 작업 시 system PATH를 조용히 덮어쓰지 않음, 플랫폼 별 installer checksum/ref 검증, shell profile 수정 강제 금지. Native 기능이 이미 있는 경우 별도 wrapper를 만들지 않는다.

### 인자별 우선순위 결정

- **항상 존재:** `setup`, `update`라는 목적 기반 명령, help/discovery, 결과 요약.
- **검증한 경우만:** read-only preview/dry-run, verbose 또는 diagnostic level, non-interactive. 이 인자들은 기계가 무엇을 설치할지 결정하는 권한을 확대하지 않는다.
- **요구가 나타나야:** `--only`/`--skip` task selection(의존성 그래프 검증), `--json`(실제 머신 consumer), `--offline`(cache 상태 보장 여부), per-user `--install-skill` opt-in, `--timeout`. 이미 native mise flag가 있으면 동일 이름을 복제하지 않는다.
- **기본 배제:** `--force`, 무제한 `--latest`/`--all`, generic `--global`, 임의 `--os`/`--arch` 설치 강제, repo source policy를 덮어쓰는 `--version`.

## 결정 및 범위 밖

**권고:** `mise run setup` / `mise run update` 두 명령, 기본 인자 0개를 유지한다. 변경이 생기는 update의 read-only preview와 필요한 권한만 분명하게 안내한다. 새로운 flags를 설계하기 전에 실제 mise task arg semantics, early fail/no-write, native options overlap, shell 종류를 테스트한다. Native Windows와 WSL을 구분하되 해당 플랫폼을 테스트 전 공식 지원으로 선언하지 않는다.

**남은 질문:** 지원할 최소 OS/arch/shell matrix; native Windows에서 root `mise.toml`의 7개 도구 artifact/installer 실제 실행; 현재 mise CLI version에서 `usage`/`run_windows`/`raw_args` 등 기능 지원; Git Bash vs PowerShell support policy; external Skill installer의 Windows copy mode; CI Windows/macOS matrix 도입의 비용; no-TTY 내역·error aggregation.

**계측:** OS/arch/shell fingerprint(개인식별 내용 제외), cold/warm setup 결과, argv/flag parsing error, prompt count, cache 다운로드/시간, 임의 OS-global write 발생 여부, 재실행 성공 여부. 실제 runtime 시험 없이는 pass를 표기하지 않는다.

## Official source ledger

| ID | 공식 자료 | 해당 조사 근거 |
| --- | --- | --- |
| S1 | [mise running tasks](https://mise.jdx.dev/tasks/running-tasks.html) | task arg 전달, run array 마지막 인자, mise flags 위치, task dry run |
| S2 | [mise task arguments](https://mise.jdx.dev/tasks/task-arguments) | usage spec, validation, help/completion, usage_* variables, env precedence |
| S3 | [mise task configuration](https://mise.jdx.dev/tasks/task-configuration.html) | run_windows, shell, raw_args, dir, timeout, output/interactive |
| S4 | [mise configuration settings](https://mise.jdx.dev/configuration/settings.html) | task.run_auto_install, OS override |
| S5 | [mise FAQ](https://mise.jdx.dev/faq.html) | Windows native/WSL backend 지원 경계, NO_COLOR |
| S6 | [mise installing](https://mise.jdx.dev/installing-mise.html) | Win winget, macOS/Linux installation, shell activation |
| S7 | [mise CLI configuration](https://mise.jdx.dev/configuration/settings.html#os) | MISE_OS target override vs host |
| S8 | [Microsoft WSL filesystems](https://learn.microsoft.com/en-us/windows/wsl/interop), [WSL interop](https://learn.microsoft.com/en-us/windows/dev-environment/wsl-interop) | Windows/WSL separation, filesystem performance/path conventions |
| S9 | [uv cache](https://docs.astral.sh/uv/concepts/cache/) | OS-specific cache/link mode and concurrency |
| S10 | [Lefthook install](https://lefthook.dev/usage/commands/install/) | core.hooksPath, destructive resolution flags |
| S11 | [CLI Guidelines](https://clig.dev/) | human-first help, flags, errors, noninteractive output |

이 문서는 현재 코드의 통과 테스트가 아니며, 후속 설계 문서와 테스트 매트릭스로 결정 사항을 인계한다.
