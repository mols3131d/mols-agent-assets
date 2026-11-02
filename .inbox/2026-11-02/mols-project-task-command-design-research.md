# Project Task/Command Design — 설계 조사

> 상태: 신규 Skill **준비 자료(비정본)**. 향후 `SKILL.md`가 실행 계약을 소유한다. 본 자료 자체는 Skill이나 저장소 정책이 아니다.

## 문제와 목표

빌드·개발·검증·자산 생성·평가 명령이 mise task, Make target, just recipe, npm script, Python/Shell CLI, CI·hook에 걸쳐 중복될 수 있다. 도구별 native 옵션을 반복 alias로 복제하거나, 중계만 하는 wrapper를 층층이 쌓으면 호출 계층과 유지비용이 증가한다.

`mols-project-task-command-design`은 **프로젝트 명령 표면(project task/command surface)의 설계·리뷰·리팩터링 판단**을 맡는 재사용 Skill로 제안한다. 이름의 `task`는 runner가 실행하는 프로젝트 명령 단위이지, 이슈·할 일 관리나 에이전트 작업 분해·스케줄링이 아니다. `task`라는 단어만으로 Skill을 활성화하지 않는다.

특정 runner에 종속되지 않는다: mise, Make, just, npm scripts, tox/nox, shell/Python CLI 등. 실제 옵션·버전 지원 여부는 현재 프로젝트 설정과 해당 도구의 정본 공식 문서로 확인한다.

## 기존 owner와의 경계

| Capability | 기존 owner | 새 Skill의 책임 |
| --- | --- | --- |
| 개발환경 부트스트랩 | `mols-dev-env-bootstrap-design`: setup/update, 설치·잠금·복구·권한 | 기존 정책을 호출하는 명령의 인터페이스 설계 |
| CI | `mols-ci-design`: admission·트리거·검증 증거·권한 | CI가 사용하는 프로젝트 공통 명령의 재사용성과 호환성 |
| 코드 가독성 | `mols-code-comprehension-refactor`: 코드 동작을 보존하는 이해비용 개선 | task/CLI entrypoint·wrapper·매개변수 인터페이스 판단 |
| Agent Asset 작성 | `mols-agent-asset`: Skill 제작·검토·검증 방법 | 해당 제작 프로세스를 재사용하고 도메인 행동만 새 Skill에 둠 |

새 Skill은 자체 버전 관리자, 설치기, CI 정책 엔진이나 범용 CLI framework를 만들도록 유도하지 않는다.

## 재사용 가능한 핵심 판단

1. **줄 수·파라미터 개수는 task 존치 기준이 아니다.** 한 줄이라도 팀/CI/에이전트가 공유하는 공식 진입점, lock·환경·working directory·검증/exit 의미를 고정한다면 유효하다.
2. **네이티브 우선.** CLI의 doctor, outdated, 디렉터리/인수 전달, 설정 파일 선택, lock generation을 먼저 활용한다. 얇은 wrapper를 둘 이유가 있다면 프로젝트 고유 정책 또는 소비자와 검증 가능한 계약을 제시한다.
3. **공개 명령과 구현 단위를 구분.** task runner는 공식 호출 표면·환경·작업 디렉터리를, native 도구는 해당 CLI 옵션·기본값을, 프로젝트 스크립트는 저장소 고유 생성·검증 동작을 소유한다.
4. **별칭 증식보다 매개변수·서브커맨드.** config, suite, 실행 모드의 조합별로 task를 복제하지 않는다. 인수 passthrough, native 옵션, `sync|validate` 등의 서브커맨드로 표현할 수 있는지 검토한다. 단 서로 다른 권한·write/cache·비용 경계는 숨기지 않는다.
5. **삭제 전 소비자를 전수 탐색.** CI, hook, IDE task, 문서, dependency, 외부 automation, 직접 호출자와 호출 시점의 env, cwd, lock, exit, stdout/stderr, OS별 quoting을 확인한다.
6. **진단·변경·갱신은 별도 계약.** read-only 검사와 설치, 수정, Git staging, 모델/원격 호출을 혼합하지 않는다. status만 출력하는 명령을 실제 readiness를 판정한다고 주장하지 않는다.
7. **검증은 변경된 의미에 맞는 최소 근거.** 정적 변경과 단위 테스트는 런타임 실행이나 모든 OS의 동등성을 보증하지 않는다. Native 진단·CLI 기능의 최소 지원 버전과 실제 CI/호스트 버전을 대조한다.

## 결정 프레임

| 상황 | 기본 방향 | 확인 조건 |
| --- | --- | --- |
| 외부 CLI의 단순 조회 별칭 | native CLI 직접 실행 | 프로젝트 고유 contract·소비자 존재 여부 |
| 공식 검증/설치/동기화 호출점 | 짧아도 task 유지 | env, pin, lock, working directory, 검증 경계 |
| config/suite별 반복 task | 인수 기반 하나의 entrypoint | 기본값, filter, cache/write, remote cost, 에러 |
| 디렉터리만 변경하는 중계 Python | runner의 native `dir` 검토 | Windows·CI PATH, cwd, 인수 전달 |
| 하나의 CLI에서 생성/검증 기능 | 명시적 subcommand, 구현 책임은 필요시 분리 | `validate`는 read-only, `sync --staged`만 index 변경 |
| 계약 없이 단순 명령 재포장 | 제거 후보 | 직접 native 명령과 소비자 이관 경로 |

**유지 / 직접 호출 / 통합 / 분리 / 제거** 중 하나를 미리 강제하지 않고 실제 소비자와 운영비용을 비교한다.

## PR #275에서 확인된 사례

참조: [개발 도구 task 정리 PR #275](https://github.com/mols3131d/mols-agent-assets/pull/275). **2026-11-02 시점 독립적으로 진행 중인 PR**이며, 아래 내용을 main의 확정 구현으로 간주하지 않는다.

- scripts-only 프로젝트 루트 `package.json`은 task 실행이 mise로 일원화되면 제거 가능. 다만 Node와 mise의 npm backend는 별도 필요성을 가진다. CI·문서의 `npm run` 소비자도 이관해야 한다.
- Promptfoo 평가별 alias는 `mise run eval -c <config> --filter-metadata suite=<name>`처럼 인수를 활용. 기존 일부 평가의 `--no-cache --no-write` 정책과 원격 모델 비용/전송 경계는 보존한다.
- `generated-sync`·`generated-validate`는 `mise run generated sync|validate` 한 진입점으로 통합하되 내부 **생성+stage**와 **read-only 비교** 로직은 별도 책임으로 보존했다.
- `rulesync-doctor`·`rulesync-preview`는 한 줄이어도 `src/rulesync` workspace 선택 계약이 있어 유지, cwd 변경만 하던 Python 중계는 runner의 native `dir`로 대체했다.
- `outdated` task는 native 조회의 단순 별칭, `preflight`는 준비 상태를 실제로 판정하지 못한 출력 묶음이라 제거했다.
- `mise doctor project`는 `2026.9.6` 이상에서 지원. 설치/갱신이 아닌 제한된 project check에 활용하며 실제 CI 설치 버전과 맞춘다.
- 정확한 버전/잠금은 원래 tool manager가 소유한다. 새 도구 버전 채택 시 native lock 생성·체크섬·실제 locked install 근거가 필요하나, 그 버전 갱신 정책 자체를 이 Skill이 새로 소유하지 않는다.

## Activation 후보와 근접 비적용 사례

- **선택:** “mise task·npm scripts 중복을 정리하자”, “Make target과 Python CLI 진입점을 단순하게 설계해줘”, “config별 평가 명령을 매개변수화하자”, “CI/hook·로컬의 검증 명령을 통합하고 소비자 호환성을 보존하자”.
- **비선택/다른 owner:** 개인 To-do/이슈 우선순위, 에이전트 장시간 스케줄링, 단일 CLI 옵션 사용법, 패키지 한 개 업데이트, 일반 Python 내부 가독성, CI admission 기준만 재설계.

Activation description은 키워드 나열보다 **프로젝트 명령 표면의 설계·최적화 의도**와 비해당 범위를 나타내야 한다.

## 아직 결정하지 않은 부분

- Skill이 설계·리뷰 및 구현 인계만 기본 수행할지, 명시적 요청 시 실제 실행 파일 변경까지 지원할지는 작성 시 기존 owner와 scope를 검토해 결정한다.
- 도구별 command reference, maintainer doc, scripts, eval fixture를 관성적으로 추가하지 않는다. 독립적인 loading·reuse·validation 필요가 있는 경우에만 분리한다.
- 주기적 task 최적화나 무인 실행을 새 Skill의 목표로 자동 확장하지 않는다.
