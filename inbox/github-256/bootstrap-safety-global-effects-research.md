# Bootstrap stability and global side effects — 심층 조사

> PR #256 · 2026-10-24 · **Research artifact / 근거와 제안, 현재 runtime 보장 아님**. 조사 기준 branch: `mols/feat/dev-environment-bootstrap` @ `817a354d3a1181a5d41f37c315d10e56fa980c81`. 후속 설계: [safety handoff](bootstrap-safety-design.md). 기존 UX/OS 조사: [deep research](bootstrap-deep-research.md), [CLI/OS](bootstrap-cli-os-research.md). 원본은 GitHub Plugin으로 확인했고 실제 사용자 컴퓨터에서 설치기는 실행하지 않았다.

## 질문과 핵심 발견

목표는 '성공하는 설치 스크립트'가 아니라 **실패·중단·재실행·다른 프로젝트와의 공존 중에도 기존 컴퓨터 환경을 보호하는 bootstrap**이다. 전역(global)을 OS/system 관리자 범위로만 좁히면 실제 변경 표면을 놓친다.

- **OS/system:** 관리자 패키지, 시스템 Python, 서비스, 레지스트리/HKLM, machine-wide PATH 및 실행 정책.
- **사용자 전체(user-wide):** `~/.claude`, `~/.codex`, Gemini extensions, `~/.config`, `~/.gitconfig`, PATH/profile, shell history/init, npm/global prefix, uv managed Python, mise tool installs.
- **공유 개발 상태(shared):** tool cache, source checkout, Git shared config, worktrees, symlink/alias, editor/IDE integration, 인증정보 노출·네트워크 접근.
- **프로젝트 내부:** `.venv`, generated vendor files, Git hook files, locks, repository configs. 프로젝트 내부라도 `core.hooksPath`가 전역/공유 경로일 수 있고 환경변수/symlink를 통해 외부를 가리킬 수 있다.
- **프로세스 한정:** 현재 실행의 PATH/ENV 변경. 파일을 영구 수정하지 않더라도 하위 프로그램에 자격증명·환경설정이 전달될 수 있다.

**핵심 결론:** 작업의 설치 범위와 실제 코드가 도달할 수 있는 범위는 다르다. 외부 installer를 홈 디렉터리와 인증 환경에 노출한 상태로 실행하면 서류상의 "project-only" 약속을 지킬 수 없다. 안전 기본값은 **예상 쓰기집합을 미리 보여주고, 명시적으로 소유하는 프로젝트/관리 범위만 자동 적용하며, 사용자 공유/OS-global 작업은 격리·승인 또는 별도 명령으로 분리**하는 것이다.

## Research loop 1 — 실제 실행 경로 추적

[현재 mise.toml](../../mise.toml)의 `setup`은 다음 순서다. `mise run` 자체도 사전 도구 설치를 수행할 수 있다 [S01].

| 순서 | 코드/소유자 | 관찰된 변경·가능한 영향 | 범위/우려 |
| --- | --- | --- | --- |
| 0 | mise task 진입·자동 설치 | mise user tool store/cache, binary resolution, trust state의 변경 가능 | 프로젝트 코드 preflight **이전** 실행. 기본 자동 설치는 설정 영향 [S01][S02] |
| 1 | `uv sync --all-groups` | `.venv` 생성/동기화, dependency 제거, uv cache 및 Python manager 다운로드, 일부 경우 `uv.lock` 갱신 가능 | `UV_PROJECT_ENVIRONMENT`가 절대경로/system Python을 가리키면 외부 환경의 패키지도 삭제 가능 [S03][S04] |
| 2 | `rulesync install --frozen` | lock된 source의 다운로드·Rulesync 관리/캐시 영역 설치 | frozen은 허가된 쓰기 범위/보안 격리를 의미하지 않음 |
| 3 | `rulesync generate` | `rulesync.jsonc`의 `outputRoots`가 `"."`이므로 저장소의 vendor projection 파일을 생성/갱신 | 기존 tracked/untracked 파일과 충돌 가능. 명시적 `--global` 작업은 현재 setup 명령에 없음 |
| 4 | `uv run python scripts/agent_assets/skills_sync.py` | XDG cache/HOME 아래 Git clone/fetch/checkout/clean, 외부 Bash `install.sh` 실행 | **사용자 전역 AI 도구 환경을 변경**. lock의 `ref`는 고정 Git tag인데 실제 commit SHA 확인은 안 함 |
| 5 | `lefthook install` | Git hook scripts 생성·설치, `core.hooksPath` 설정과 충돌 가능 | 작업 공간 local integration이지만 Git 공유 설정/다른 worktree에도 영향 가능 [S05][S06] |

현재 `check`에도 `uv run --locked ... skills_sync.py --dry-run`이 있으나 이 dry-run은 source/adapter **계획만 표시**하고 사용자 홈에 설치된 Skill의 준비 상태나 파일 내용은 확인하지 않는다. `mise run check`를 온전한 read-only 검증으로 부르려면 mise 자동 설치와 실행 프로그램의 실제 side effect도 확인해야 한다.

### 주요 숨은 환경변수 / 설정 경로

| 입력 | 영향 | 사전 확인 |
| --- | --- | --- |
| `UV_PROJECT_ENVIRONMENT` | `.venv` 대신 절대경로 virtualenv/시스템 Python을 대상으로 만들 수 있음. exact sync는 extraneous package 삭제 [S03] | 확정 대상은 실제 repo 안의 관리형 venv인지, path canonicalization/symlink 포함 |
| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME` | 프로젝트 외부의 공유 다운로드 캐시/인터프리터/소스 checkout | 허용된 cache root인지, 소유권·symlink·disk quota 확인 |
| `MISE_DATA_DIR`, `MISE_CACHE_DIR`, `MISE_CONFIG_DIR` 및 글로벌 mise 설정 | 도구/캐시 경로·trust/auto-install, PATH, backend 동작 | 실제 resolved root와 global/project inherited settings 확인 |
| `CLAUDE_HOME`, `CODEX_HOME`, `HOME` | native installer의 전역 Skill·Agent 쓰기 위치; 잘못된 값은 무관한 디렉터리까지 | 대상 디렉터리와 symlink, 사용자 파일·관리 owner 비교 |
| `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `core.hooksPath` | Git config의 적용 및 hook 검색·수정 위치 | `git config --show-origin --show-scope --get core.hooksPath` 등 읽기 확인 [S05] |
| `PATH`, `PYTHONPATH`, `npm_config_prefix`, registry/proxy variables | 잘못된 실행파일 선택, globally installed CLI, 악성/오동작 backend, 네트워크 대상 | resolved executable identity, registry, env overrides 검사 |
| `CI`, `MISE_YES`, trust/safe settings | mise config 실행·trust 정책에 영향 | non-TTY와 승인을 동일시하지 않음 [S02] |

**강한 안전 조건:** `UV_PROJECT_ENVIRONMENT`가 repo-local 예상 경로가 아니면 **즉시 차단**. 저장소 바깥 symlink/realpath를 통해 경계 밖으로 나가는 cache/prune/installer target도 자동 허용하지 않는다. 영향경로를 알 수 없으면 "영향 없음"으로 가정하지 않는다.

## Research loop 2 — 외부 설치기 원본 검토

현재 [skills_sync.py](../../scripts/agent_assets/skills_sync.py)에서 `skills-lock.json`의 `humanize-korean` 소스 `epoko77-ai/im-not-ai` `v2.3.2`를 checkout한 뒤 upstream [install.sh@v2.3.2](https://github.com/epoko77-ai/im-not-ai/blob/v2.3.2/install.sh)를 **사용자 HOME을 그대로 상속한 Bash**로 실행한다.

확인된 기능과 실패/보안 리스크:

1. **기본 설치 모드 = symlink.** `~/.claude/skills/{humanize-korean,humanize,humanize-redo}`, `~/.claude/agents/*.md`, `~/.codex/skills/humanize-korean` 등을 가리키는 링크/디렉터리를 생성한다. 즉 repository setup이 다른 workspace의 AI agent discovery를 변경한다.
2. **다른 목적지의 기존 symlink도 이동함.** upstream `prepare_target`의 `-L` 분기는 대상이 동일한 링크가 아니면 `--force` 확인 없이 `.bak.<timestamp>`으로 옮긴다. 일반 기존 파일/디렉터리는 `--force` 없이 거부한다. 'force를 안 줬으니 기존 링크는 안전'하다는 주장은 거짓이다.
3. **기존 전역 Agent 링크를 삭제하는 기능.** upstream `prune_stale_agents`가 자신이 심었던 링크 중 현재 범위 밖이거나 dangling 링크를 `rm -f`로 정리한다. 소유권 판별 로직은 있지만, **기본 setup에서 사용자 전역 상태를 정리/삭제하는 행동 자체**가 있다.
4. **Gemini CLI 전역 extensions link 시도.** `gemini extensions link <checkout>`에 `Y`를 공급하고 등록을 시도한다. 오류를 '이미 등록 또는 수동 필요'로 처리해 install.sh의 전체 exit code 0으로 끝날 수 있어, 성공 요약이 extension 준비 완료의 증거가 아니다.
5. **설치 원본은 mutable location.** checkout된 cache는 `git checkout --detach --force FETCH_HEAD`, `git clean -fdx`를 실행한다. 캐시에는 사용자가 둔 untracked/ignored 내용이 있으면 제거될 수 있다. 설치 결과가 symlink라면 cache 교체가 다른 CLI에서 사용할 Agent contents에도 영향을 준다.
6. **결과 무결성 검증 공백.** wrapper는 ``computedHash`를 읽어 확인하지 않고, upstream tag 문자열이 full immutable commit SHA라고 검증하지 않는다. Tag가 변경될 위험은 공급망 설계 리스크이며 **실제로 변경됐다는 증거는 없다**.
7. **프로세스 권한 전파.** `run_checked`는 `os.environ` 전체를 하위 Git/Bash/CLI에 전달한다(`GIT_TERMINAL_PROMPT=0`만 추가). 승인되지 않은 installer·postinstall이 인증 토큰, 홈 파일과 네트워크에 접근할 잠재적 표면이다. 악성 행위가 있었다는 주장은 아니다.

**Review loop 2.** 외부 installer의 `--dry-run`을 호출하더라도 Bash의 실제 host 접근 권한을 차단하는 sandbox가 되는 것은 아니다. Preview는 사용자가 읽을 **사전 정보**이고, 직접 실행 코드에 대한 **enforced containment**는 별도다. Native adapter를 완전히 재구현하지 않되, host-level 실행을 unconditional setup에서 분리하는 게 가장 작은 안전 개선이다.

## Research loop 3 — OS/global, trust, concurrency, rollback 반증

### 3.1 Trust/lock은 sandbox가 아니다

mise normal mode에서는 `mise run`·`mise install`·`mise exec`가 특정 config를 암묵적으로 신뢰 표시할 수 있으며, `CI`/`MISE_YES` 동작도 trust mode에 영향을 준다. `MISE_SAFE=1`은 config의 unsafe 동작을 제한한 상태에서 version/resolution metadata를 확인하는 데 유용하지만 **모든 command를 read-only로 만드는 모드가 아니다**. Config trust, source lock, runtime process confinement는 서로 다른 통제 수단이다. [S02]

mise sandbox 옵션은 task 프로세스에 filesystem/network/ENV 제한을 걸 수 있지만, **설정 로드·도구 설치·mise hooks는 sandbox 밖**이고, **Windows에서는 filesystem/network 제한이 강제되지 않고 경고 후 실행**된다. 따라서 Linux에서 검증한 sandbox 정책을 Windows host 격리라고 광고할 수 없다. [S07]

mise.lock은 다운로드 artifact를 검증할 수 있어도 **기존에 설치되어 있는 tree 또는 외부 native installer 결과를 자동 검증하지 않는다**. Cache가 이미 오염돼 있으면 locked install이 성공해도 결과 바이트가 무결하다고 증명할 수 없다. [S08]

### 3.2 Stable = 부분 실행, 반경 제한, 검증된 결과

**실패 상태 분류**: 선행 도구 없음 / 설치 승인이 없음 / 네트워크 불가 / incompatible platform / lock-policy mismatch / 기존 user file 충돌 / 권한 거부 / 설치기 실패 / 실행 중단·타임아웃 / 출력 검증 실패. 각 상태는 마지막에 단일 원인, 영향받는 단계, 복구 방법, verified vs unverified를 보여준다. 독립 단계는 계속해도 상위 READY는 필수 검증이 모두 성공해야만.

**원자성 착시 금지**: 여러 manager의 lock·cache·HOME·hooks에는 단일 transaction이 없다. Rollback을 전부 자동화하면 오히려 사용자가 소유한 새로운 파일을 지울 수 있다. Tool-owned local temp staging과 atomic rename이 가능한 영역에서만 보수적으로 사용하고, 공유 user-home은 사전 백업/소유권 추적·복구 제안 중심으로 접근.

**경쟁 상태**: 병렬 worktree가 동일 `~/.cache` Git clone 또는 동일 `~/.claude`/`~/.codex`를 쓰면 두 프로세스가 race를 일으킬 수 있다. uv는 cache 및 대상 venv에 대한 locking을 제공하지만 **우리 wrapper/upstream installer의 HOME 동시 쓰기까지 잠금으로 보호하지 않는다** [S09]. 타깃별 lock(또는 직렬화)과 상태 재검증이 필요하며, symlink path escape를 포함한 테스트를 우선한다.

**OS privilege**: 관리자 권한·sudo·Homebrew/apt/winget·Windows machine PATH·PowerShell ExecutionPolicy 변경은 `setup`/`update`의 기본 권한 밖. PowerShell은 Process, CurrentUser, LocalMachine, Group Policy 등 범위가 분리돼 있으므로 미설치 CLI 때문에 영구적인 LocalMachine 정책을 바꾸지 않는다 [S10]. mise shell activation용 profile 변경도 user-wide configuration이므로 사전 승인 또는 명시적인 사용자 안내를 기본으로 한다.

**Git/worktree**: `core.hooksPath`는 system/global/local 범위에서 설정할 수 있으며 Git config는 일반적으로 worktree 사이에 공유된다 [S05][S06]. 단순히 `.git/hooks`에 쓰는 게 local-only라고 가정하지 않는다. Lefthook 설치는 hook 파일/설정에 영향을 주고 기존 `core.hooksPath`가 있으면 멈추며 강제 플래그는 의도적인 별도 선택이다 [S11].

### 3.3 위협·오작동 모델

| 심각도 | 사건 | 영향 경계 | 최소 방어 |
| --- | --- | --- | --- |
| Critical | `UV_PROJECT_ENVIRONMENT`가 system Python/사용자 공유 환경으로 향함 | 기존 패키지 제거·프로그램 장애 | realpath와 project-root containment 검사, 위험 ENV 거부 |
| Critical | 외부 Bash/native installer가 HOME과 token을 가진 상태로 임의 코드 실행 | 사용자 비밀/전역 files/네트워크 | 기본 setup에서 분리, source review + immutable pin, 가능하면 격리 및 승인 |
| High | 외부 Skill 기존 symlink 교체·구버전 Agent 자동 삭제 | 다른 프로젝트의 AI agent behavior 변경 | target별 manifest/snapshot, 변경 전 승인, 원본 관리 대상만 변경 |
| High | shared cache `git clean -fdx` / symlink escape | 사용자 또는 다른 작업의 cache state 소실 | wrapper-owned checkout identity 검증, 임의 cache cleanup 금지, 충돌 중단 |
| High | mise auto-install/config trust가 preflight 이전 발생 | 공유 tool store/config trust 변경 | 진입점 이전 권한과 config trust 검사, auto-install 범위 통제 |
| High | lockfile/setup이 자동 resolve·rewrite | 예측 못한 버전 변경·supply-chain drift | setup locked/no-write, update만 manifest 범위 내 |
| High | hooksPath/global Git config 충돌 | 다른 worktree commit/push 동작 변화 | effective git config scope + resolved hooks target 확인 |
| Medium | PATH/profile/PowerShell 실행 정책 변경 | 다른 shell/session 도구 선택·접근권 | user/machine settings 기본 불변, 필요한 경우 명시적 승인 |
| Medium | network/mirror/proxy 실패 + silent catch | 미완성 환경을 성공으로 표시 | exit/status/retry/next action, secret redaction |
| Medium | shared cache disk full/clock skew/중단 | 부분 설치, 나중 설치 실패 | disk preflight, native lock/verify, 재실행 idempotency |

## 설계 선택 비교

| 선택 | 안전성/UX | 비용 | 판단 |
| --- | --- | --- | --- |
| 현재 `setup`의 모든 단계 무인 실행 | 초기 편리하지만 HOME/전역 surprise | 높은 incident/복구 비용 | **기각** |
| project-local/manager-approved 자동 + user-wide 분리 | 재실행 쉬움, 권한 명료 | 최소 preflight·summary 필요 | **권고** |
| 모든 명령을 sudo-less라고 안전 취급 | root escalation만 방지 | 사용자 홈/인증정보는 보호 못함 | 기각 |
| 모든 command를 컨테이너에서만 실행 | 격리 강화 가능 | OS/GUI/user-home 연동의 UX 비용 | 기본은 기각, 검증 격리용 채택 |
| mise sandbox만으로 전체 설치 보호 | Linux/macOS에 일부 이점 | 설치/설정은 sandbox 밖, Windows 강제 X | **보조 계층만** |
| 자동 전체 rollback / global cleanup | 복구처럼 보임 | user-owned state 손상 | 기각; 좁은 owned writes만 복구 |

## 검증·근거 공백

**실제 검증하지 못한 것:** Windows/macOS/Linux machine runtime, 실제 Gemini extension registration, 기존 사용자의 custom symlinks, 실제 mise safe/sandbox 실행, package hash mismatch 공격, 돌발 네트워크·disk failure, 여러 worktree 경쟁 설치. 코드를 읽어 도출한 가능한 영향과 실제 재현한 손상을 구분한다.

**사용자 관점 수용 테스트로 인계:** empty user home, home with custom Claude/Codex symlinks, malicious/malformed `UV_PROJECT_ENVIRONMENT`, `XDG_CACHE_HOME` outside expected root, repo path through symlink, shared Git worktree/hooksPath, config normal trust vs safe mode, no-TTY, interrupted install, upstream installer failure not propagated, concurrent worktrees, dry-run 0 writes, Windows sandbox unenforced, output secrets redaction. 구체 완료 기준은 [safety handoff](bootstrap-safety-design.md).

## Official & original source ledger

| ID | 근거 | 검증 포인트 |
| --- | --- | --- |
| S01 | [mise auto-install settings](https://mise.jdx.dev/configuration/settings.html#taskrun_auto_install) | task pre-install 및 글로벌 설정 영향 |
| S02 | [mise security/trust/safe mode](https://mise.jdx.dev/security.html) | normal implicit trust, safe != dry-run, CI/YES |
| S03 | [uv project environment](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path), [uv sync](https://docs.astral.sh/uv/concepts/projects/sync/) | 환경 타깃 경로 override + extraneous removal |
| S04 | [uv Python automatic download](https://docs.astral.sh/uv/concepts/python-versions/#disabling-automatic-python-downloads) | interpreter cache/user-shared install |
| S05 | [git config](https://git-scm.com/docs/git-config) | system/global/local/worktree, core.hooksPath |
| S06 | [Git worktree docs](https://git-scm.com/docs/git-worktree) | shared config와 worktree별 metadata |
| S07 | [mise sandboxing](https://mise.jdx.dev/sandboxing.html) | task-only limitation, Windows no file/network enforce |
| S08 | [mise lockfile integrity](https://mise.jdx.dev/dev-tools/mise-lock.html) | existing installed cache trust vs new download hashes |
| S09 | [uv cache safety](https://docs.astral.sh/uv/concepts/cache/) | uv cache+venv locking, cache 직접 수정 금지 |
| S10 | [PowerShell ExecutionPolicy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies/) | Process/CurrentUser/LocalMachine/GroupPolicy |
| S11 | [Lefthook install](https://lefthook.dev/usage/commands/install/) | hook install, hooksPath conflict, force/reset 선택 |
| S12 | [npm scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts/) | installer/lifecycle scripts 일반 위험; backend semantics 별도 |
| S13 | [외부 install.sh v2.3.2](https://github.com/epoko77-ai/im-not-ai/blob/v2.3.2/install.sh) | Claude/Codex/Gemini HOME 수정, symlink·prune·silent Gemini failure |
| S14 | [skills_sync.py](../../scripts/agent_assets/skills_sync.py), [mise.toml](../../mise.toml) | 실제 호출 체인, 전체 ENV 상속, cache clean, 자동 실행 |
| S15 | [Git clean](https://git-scm.com/docs/git-clean) | `-fdx`가 ignored/untracked cache files까지 삭제 |

**Finalize:** 호스트 변경에 대한 실제 owner·진입점·scope와 실패 반례를 확인했다. 대응 방법과 검증 항목을 별도 설계 문서로 인계한다. 조사 증거를 runnable safety guarantee로 승격하지 않는다.
