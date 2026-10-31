# Bootstrap safety architecture — 전역 영향 통제 설계 인계

> PR #256 · 2026-10-24 · **제안된 안전 계약과 테스트 계획이며 아직 구현·실행하지 않음**. 입력: [안정성/전역 영향 심층 조사](bootstrap-safety-global-effects-research.md), [부트스트랩 명세](development-environment-bootstrap-spec.md), [CLI·OS 설계](bootstrap-cli-os-design.md). 이 문서는 프로젝트용 local delta이며 범용 `mols-dev-env-bootstrap-design` Skill의 실행 원본을 대체하지 않는다.

## 최우선 불변 조건

1. **No surprise global writes:** 명시적으로 허용한 프로젝트 및 관리형 도구 영역 밖의 변경은 사전에 경로·효과를 식별하고 별도 opt-in/명령 없이는 진행하지 않는다.
1. **No accidental system-Python sync:** 실제 `uv` sync 목적지는 이 저장소가 소유한 canonical project venv로만 제한한다. 환경변수, symlink 또는 상대경로가 `/usr/local`·다른 venv·외부 사용자 디렉터리로 향하면 거부한다.
1. **Setup never promotes policy:** setup은 승인된 lock state만 재현한다. 버전 정책·lock을 재해석하거나 불필요한 repository 파일을 변경하지 않는다.
1. **Ownership before cleanup:** 삭제, 교체, 백업/이동, 외부 Git checkout의 `clean`은 소유한 경로임을 확인하기 전에는 수행하지 않는다. `--force`·OS 관리자 권한·global config rewrite는 default에서 금지한다.
1. **Failure is visible:** 필수 도구 누락·사용자 공유 작업 미승인·실패한 외부 installer·검증 실패는 정확히 단계별 기록하고, 실제 READY 여부를 거짓으로 보고하지 않는다.
1. **Process authorization != install authorization:** config trust, Git ref lock, task dry-run과 OS-level sandbox는 서로 대체할 수 없으며, 외부 코드가 읽을 수 있는 환경(토큰·SSH agent·HOME·네트워크)도 영향 범위에 포함한다.
1. **Platform claims require evidence:** Windows에서 Linux/macOS용 mise sandbox 정책은 filesystem/network를 강제하지 않는다. Windows native에서 동일한 containment를 보장한다고 쓰지 않는다.

## 설계안: 두 단계 승인 경계

### Phase A — preflight (최대한 read-only, mise task 실행 전 영향도 포함)

**진입 전:** `mise` 자체가 없는 상태는 명시적 사용자 준비 안내. `mise run`은 tool pre-install과 config trust를 유발할 수 있으므로 단지 `tasks.setup.run` 맨 앞에 preflight를 두어도 충분하지 않다. 현재 사용하는 mise 버전에서 사전설정 `task.run_auto_install=false`/`MISE_TASK_RUN_AUTO_INSTALL=false`, 명시적 locked installation task 분리, native trust semantics를 PoC로 확인한다. Automated preflight는 self-install이나 user-level config trust를 안전하게 자동 허용하지 않는다.

**탐지:** 현재 Git top-level/ref/worktree, OS/arch/shell, 실제 PATH executable, venv resolved realpath, uv/mise/cache roots, HOME/native Skill destinations, Rulesync projection targets, effective `core.hooksPath` + config origin, unknown/dirty symlink/lock states, installer source/ref의 integrity와 네트워크 접근이 필요한지 확인한다.

**출력:** each operation의 ID, 대상 범위, 쓰기·삭제·네트워크·외부 코드 실행·승인 필요 여부, blocking prerequisite와 next action. 인가되지 않은 sensitive 경로는 세부 HOME/token 경로를 그대로 출력하지 않는다.

예상 작업 예시 (실제 로그가 아님):

```text
Project bootstrap preflight
  ready      repo + pinned manifests
  permitted  .venv sync (locked)
  permitted  mise-managed tool cache, specified versions
  blocked    UV_PROJECT_ENVIRONMENT points outside managed project .venv
  optional   user-level agent skills -> explicit separate command
  review     Lefthook hook destination differs from expected project hook path
Result: BLOCKED; no apply started
```

### Phase B — apply / verify / report

**Apply scope:** repo-owned `.venv`, mise 관리 영역의 사전 승인된 tool/version, Rulesync project projection 중 안전성이 확인된 경로로 제한한다. 각 작업이 source/target/permissions를 재확인하고 실행한다. 선행 종속 오류의 경우 그 작업만 skip하고 독립 작업은 계속 진행; 상태가 불명확한 경우 결과를 VERIFIED/READY로 추측하지 않는다.

**External Skill install:** 현재 `mise run skills-sync`의 native adapter 계약은 보존하면서 **기본 `setup`에서는 무인 호출하지 않는 정책을 검토·도입**한다. 명시적 opt-in이 있더라도 upstream installer가 쓸 수 있는 Claude/Codex/Gemini HOME·수정 대상 목록을 보여주고 symlink collision, agent prune, extension registration, full ENV inheritance를 사전 평가한다. 가능한 경우 실제 변경을 wrapper가 아닌 native installer에 맡기되, 정확한 실제 설치 상태를 후속 검사한다. `skills_sync.py --dry-run`은 **계획 조회**이지 실제 HOME diff 검증이 아니다.

**Hooks:** `lefthook install`은 repo-local처럼 보이더라도 shared Git config/hook destination에 영향이 있을 수 있다. `git config --show-origin --show-scope --get core.hooksPath`, `git rev-parse --git-path hooks`와 파일 소유권을 점검한다. 기존 custom hooks가 있으면 silent overwrite하지 않고 SKIPPED/BLOCKED + manual command 안내. 강제 옵션은 사용자가 분리해 실행한다.

**Final summary:** project-ready와 optional-feature-ready를 구분하고, 각 skipped/blocked/failure의 source, affected path class, recovery action, exit code를 요약한다. 로그가 없어도 사용자 홈 수정 내역을 알 수 있는 수준의 경량 write manifest를 **해당 동작에 실제로 필요하고 개인정보 없이 저장 가능한 경우만** 추가한다.

## Permission matrix (proposed)

| 실행 단계 | 무인 기본 허용 | 기본 거부/별도 승인 | 사전 검증 |
| --- | --- | --- | --- |
| mise versioned tools | 프로젝트의 기존 승인 범위 내 user-cache 설치 가능 | OS/global 패키지, 별도 backend 스크립트의 미승인 외부 변경 | auto-install preflight, backend, cache root |
| uv Python/packages | repo-local `.venv`, 승인된 managed interpreter 다운로드 | system Python, 다른 프로젝트 env, 외부 절대경로 `UV_PROJECT_ENVIRONMENT` | realpath containment, lock, Python download expectation |
| Rulesync | 소유된 repo-root projections, frozen source | user-global mode, target outside root, 기존 사용자 파일 교체 | source/ref, outputRoots/paths, dry-run/check |
| Source-native Agent Skill | 기본 setup **미포함** | 사용자 홈 링크/에이전트 prune/Gemini 확장 등록 | full target list, collision & owner, opt-in + runtime evidence |
| Git hooks | 기존 설치와 충돌 없는 프로젝트 관리 hook만 고려 | shared/global custom hooks, core.hooksPath reset/force | hook path, config scope, existing files |
| System manager | 없음 | sudo/apt/brew/winget, machine PATH, PowerShell LocalMachine config | user-facing official installation instructions |
| cleanup/reset | 없음 | `git clean`/reset 등 소유권 미검증 삭제, uv-cache prune, stale user agent prune | explicit target ownership, no user-owned loss |
| shell/profile | 현재 process scoped environment만 | .bashrc/.zshrc/PowerShell profile, permanent PATH/registry | user approval and reversible edit guidance |

**중요:** 관리형 도구 다운로드는 예외적으로 user-share 영역에 변화를 남긴다. 사용자 승인이 **관리형 도구의 특정 cache·버전 관리**까지 미리 내려진 경우에만 자동 설치한다. 'mise가 알아서 설치'가 권한의 근거는 아니다.

## Security / reliability layers: 보장과 한계

| 수단 | 확보하는 것 | 확보하지 못하는 것 |
| --- | --- | --- |
| exact pin + lock + checksums | 허용된 버전/다운로드의 일부 integrity | 이미 설치된 cache 파일 무결성, upstream installer의 권한/행동 |
| mise trust / paranoid | config 승인 정책과 변경 검출(설정·모드별) | task의 HOME/ENV/network sandbox |
| `MISE_SAFE=1` | version metadata/resolve에서 config code 실행 차단을 돕는 안전 모드 | 일반 `mise run`을 계속 실행하거나 파일을 read-only로 만드는 보장 |
| mise sandbox | 지원 OS에서 task child-process 권한 일부 제한 | task 이전 mise install/config/hooks, Windows filesystem/network 격리 |
| native `--dry-run` | 해당 command에 한정된 미리보기 | 하위 installer·setup 전체 경로의 no-write 보장 |
| 경로 realpath/owner 검증 | 실수·path escape 위험 감소 | 사전 검사 이후 변경되는 TOCTOU 공격의 완전 방지 |
| isolated container/temp HOME | 검증 시 사용자 실제 상태와 격리 | host integration/GUI 설치의 실제 사용성 및 권한을 그대로 재현하지 못함 |

옵션의 정확한 동작과 현재 mise v2026.9.x / uv 0.12.1 지원은 별도 runtime PoC 전제로 둔다. 최신 공식 문서의 변경 사항을 현재 pinned version의 증거로 사용하지 않는다.

## 실패·복구 계약

- **Preflight stop** — 경계 위반·global side-effect 무승인 시 apply 전 거부, safe next command만 출력.
- **Stage failure** — 실패한 owner의 후속 단계만 차단, 별도의 준비 기능은 성공할 수 있음. Required vs optional은 사용자의 workflow에 따라 선언.
- **Non-atomic install** — repository cache, `.venv`, HOME, Git hooks 등 서로 다른 state owner를 하나로 자동 rollback하지 않음. 해당 작업이 소유한 임시 파일을 정리하는 범위만 허용.
- **Post-check** — 설치기 exit 0만으로 READY 판정 금지. upstream Gemini registration의 오류 은닉처럼 실제 ready probe가 필요.
- **Interrupted / concurrent** — 같은 HOME/native Skill installer와 cache Git checkout에 경쟁 중단/직렬화·재시도. stale temp/artifact는 소유자가 확인된 것만 정리.
- **Recovery** — 사용자가 직접 변경한 repo/host 파일은 덮어쓰기/삭제하지 않는다. 정확한 충돌 대상과 선택 가능한 수동 해결 방법을 제시한다.

## MVP implementation phases

1. **P0 위험 차단**: 기존 setup의 user-home installer를 자동 경로에서 분리; managed tool install의 선행 범위 통제; absolute/external `UV_PROJECT_ENVIRONMENT` 차단; PATH/tool/cache/host fingerprint 확인; history/lock update 금지.
1. **P0 충돌/불일치 처리**: symlink/hook/projection 관리 범위 점검, user-managed files 변경하지 않음, optional 실패 exit/status, network/capability errors.
1. **P1 보안/공급망 강화**: upstream adapter source immutable SHA/검증 근거; ref/integrity mismatch block; 실행 전에 env exposure 최소화; 실제 installer outcome verification; 필요 시 OS 격리. 단순 Git tag 문자열을 immutable artifact로 취급하지 않는다.
1. **P1 UX**: 첫 사용/반복 사용에서 영향 목록과 다음 행동을 한 화면으로 표기, 충돌시 clear manual path, read-only diagnosis와 process scope detection.
1. **P2 최적화**: verified no-op, installed cache reuse, safe concurrency, 디스크 quota·성능 baseline. 안정성 증명 전 병렬화하지 않음.

변경 대상 후보는 `mise.toml`, narrow preflight/orchestration code(필요성이 입증될 경우), `scripts/agent_assets/skills_sync.py` (native installer 호출과 검증 guard), bootstrap guidance/test harness. OS-global manager, system configuration, 사용자 HOME 파일을 실제로 바꾸는 코드는 이 계획에 포함하지 않는다.

## Acceptance test matrix

| ID | 시나리오 | 관찰 가능한 통과 기준 |
| --- | --- | --- |
| S01 | `UV_PROJECT_ENVIRONMENT=/usr/local`, other project's venv, symlink outside | 0개의 외부 package 삭제, preflight BLOCKED |
| S02 | missing mise/tool-manager cache | 권한 밖 install 0, managed-only command scope와 설명 |
| S03 | `CLAUDE_HOME`에 사용자 symlink/custom agent 존재 | opt-in 없는 이동·삭제·교체 0 |
| S04 | upstream importer의 old Agent prune/dangling symlink | 기본 setup에서 user-home unlink 0 |
| S05 | Gemini `extensions link` command failure | 성공으로 숨기지 않고 not-ready/blocked 설명 |
| S06 | malicious/modified upstream install script 또는 floating ref | tag/ref identity 검증 실패 시 external execution 0 |
| S07 | read-only preview/doctor | project/HOME/cache/Git config tracked/untracked write 0 (mise pre-install 포함) |
| S08 | `git config --global core.hooksPath`, existing custom hook | global config mutation 0, 기존 hook 보존 |
| S09 | cached Git checkout에 untracked 사용자 파일 | 무인 `git clean -fdx`로 소유 불명 파일 제거 0 |
| S10 | 동시에 두 worktree가 skills sync | cache corruption, interleaved HOME edits, readiness false positive 0 |
| S11 | uv `sync --locked` 와 lock drift | lockfile mutation 0, fail + explicit next action |
| S12 | Ctrl-C/timeout, disk full, network unavailable | READY 오판 0, 재실행 가능, 이전 user-owned files 보존 |
| S13 | non-TTY/CI, Windows native | 승인 없는 interactive prompt/privilege 변경 0; Windows sandbox 미강제는 pass로 보고 금지 |
| S14 | PATH shadowing/manager override, secrets in ENV | 예상 binary만 실행, credential log leak 0, external code permissions 제한 |
| S15 | 정상 fresh setup + warm rerun | core functionality ready, tracked locks unchanged, unnecessary writes 없음 |
| S16 | allowed bounded update and sidecar + installed caches | 정책 변경 없이 최신 허용 결과, lock diff/review, 이전 전역 설치 overwrite 없음 |
| S17 | Git shared config/worktree hooks, symlink targets | worktree 간 설정/Hook 부작용 보고와 충돌 차단 |
| S18 | project generated files dirty/customized | 기존 사용자 변경과 미충돌 시만 쓰기, 충돌이면 block+remediation |

**검증 순서:** 정적 코드/CLI 옵션 검사 → fake executables + isolated `HOME`/`XDG_CACHE_HOME`/tmp repo → Git worktree concurrency test → Linux/macOS sandbox가 적용되는지 별도 확인 → Windows **실제 격리 테스트 환경** → clean machine smoke. 외부 설치기는 신뢰할 수 없는 코드로 보고, 실제 사용자 HOME에서 시범 실행하지 않는다.

## 리뷰 결과 / 남은 결함

- **Security 관점:** safe/locked/trust/dry-run을 하나의 보안 기제로 혼동하면 P0 위험을 놓친다. HOME install은 실행 격리나 명시적 사용자 승인 전에는 기본 setup에서 분리한다.
- **UX 관점:** 매 실행마다 모든 project-local 설치에 확인을 요구하는 것도 과잉이다. 최초 승인된 managed scope는 조용한 no-op/repair를 제공하되 전역 영향만 명확히 분리한다.
- **운영 관점:** Git hook/외부 Agent 설치는 새 개발자가 반드시 필요한 기능인지 판단해야 한다. 필수가 아니라면 DEGRADED(명시)로, 필수라면 BLOCKED로 표기한다.
- **이식성 관점:** 이 문서의 mise/uv/Claude/Codex/Gemini 구체 경계는 *이 repository의 구현 인계*에 머문다. 공통 Skill은 generic scope/ownership/invariants만 유지한다.
- **불확실성:** 현 mise version과 일부 최신 safe/sandbox 동작의 차이, 실제 OS/유저 HOME, upstream security provenance, cache sidecar, lockfile pin과 artifact 검증 결과는 **실제 실행하지 않았다**.

**Exit:** 의도치 않은 전역 변경의 경계를 명시하고, 차단/승인/검증 우선순위와 실행 가능한 회귀 체크를 수립했다. 실제 runtime 구현/검증은 별도 후속 Work이며 이 설계가 그 결과를 대신하지 않는다.
