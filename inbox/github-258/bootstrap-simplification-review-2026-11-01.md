---
description: PR #258의 Windows·WSL cold-cache 설치와 복구, native mise 잠금 실패 경계, 실행 위임 후보 및 남은 OS 검증 범위를 확인할 때 참고합니다.
---

# PR #258 — 경량화·격리 설치 후속 검증

**Windows와 WSL Ubuntu의 격리 설치·반복 복구·Python-only update는 통과했다. WSL의 native 잠금 실패 경계와 전체 테스트 335개도 통과했다.** npm 실행의 단순한 mise 위임은 Windows에서 호스트 명령 fallback이 재현되어 채택하지 않는다. macOS native E2E는 미검증이다.

이 문서는 2026-11-01의 비정본 검토·실증 기록이다. 정본은 [개발환경 정책](../../docs/development/development-environment.md)과 [mise 운영 안내](../../docs/references/tooling/mise.md)가 소유한다. 최초 검토와 변경 과정은 Git history에서 확인한다.

## 판단과 반영

| 대상 | 근거와 결정 |
| --- | --- |
| Python-only update의 CLI lock 변경 예외 | [`8f7bf53`](https://github.com/mols3131d/mols-agent-assets/commit/8f7bf537f0d17d88f54eb4956463b5e65ed9f395)에서 수정. `uv.lock`만 변경을 허용하고 예기치 않은 `mise.lock` 변경은 보존하면서 중단한다. |
| npm manifest·pinned Node 직접 실행 | native 위임 후보에서 PATH fallback을 재현했다. 기존 package identity·managed prefix 검증을 유지한다. |
| `MISE_LOCKFILE=1` | 상속값이 `0`이면 프로젝트 설정을 덮어쓰고 strict locked install이 실패한다. 중복으로 간주해 제거하지 않는다. |
| 반복 환경 검사 | setup에서 외부 명령 없이 연속 수행하던 검사 1회를 제거한다. update의 resolver 전·후와 두 mode의 sync 전 검사는 유지한다. |
| CLI bounded update·플랫폼 lock | 현재 exact pin·Python-only update 범위를 유지한다. 정책과 지원 플랫폼이 다른 이전 로컬 인계 커밋은 이식하지 않는다. |

## Windows native 실행 실증

mise `2026.10.17 windows-x64`에서 `MISE_AUTO_INSTALL=0`과 `MISE_EXEC_AUTO_INSTALL=0`을 적용했다. 기존 설치만 사용했으며 이 실험에서는 도구를 설치하지 않았다.

| 실행 조건 | 관측 결과 |
| --- | --- |
| 잠근 Node + npm CLI 3종 | Node `24.19.0`의 managed executable, Biome `2.5.6`, Rulesync `40.2.0`, skills `1.5.23` 확인 |
| child가 `exit(23)` | mise도 exit 23 반환 |
| 잠금에 없는 `npm:skills@0.0.0`, 동명 호스트 명령 없음 | 오류와 exit 1 |
| 동일 요청, PATH 앞에 exit 0인 임시 `skills.cmd` | lock 경고 뒤 `HOST_FALLBACK` 출력, exit 0 |

재현의 핵심 명령은 다음과 같다. 동명 fixture는 프로젝트의 임시 디렉터리에 만들었으며 실제 전역 명령을 변경하지 않았다.

```powershell
mise exec --locked node@24.19.0 npm:skills@0.0.0 -- skills --version
```

`--locked`만으로 package identity와 호스트 fallback 차단을 보장할 수 없다는 이 버전의 관측이다. 현재 실행기의 결함이나 다른 mise 버전·OS의 결과로 확대하지 않는다. 단순 교체 대신 기존 구현을 유지한다.

또한 `MISE_LOCKFILE=0`을 상속한 `mise install --locked --dry-run node@24.19.0`은 `locked mode requires lockfile to be enabled` 오류로 실패했다.

## Windows cold-cache 설치와 복구

설치 검증 source는 [`8f7bf53`](https://github.com/mols3131d/mols-agent-assets/commit/8f7bf537f0d17d88f54eb4956463b5e65ed9f395)이다. 기존 mise 실행파일과 Python `3.13.11`을 재사용하고, 별도 snapshot·Git 저장소·mise data/config/state/cache·npm cache/config·uv cache·임시 디렉터리에서 실행했다. Python 다운로드와 HOME Skills·사용자 Git hooks 설치는 제외했다.

| 순서 | 관측 결과 |
| --- | --- |
| 빈 도구·패키지 캐시에서 setup | CLI 7종 설치·정확한 버전 검증, Python sync/check, `READY`. 정책·잠금 8개 파일의 hash 보존 |
| 같은 환경에서 setup 반복 | `READY`, 같은 8개 파일 hash 보존 |
| update | `READY`, `uv.lock`만 변경. CLI lock·manifest·외부 자산 revision 보존 |
| update 후 setup | `READY`, 갱신된 `uv.lock` hash 보존. 최종 Git 변경은 `uv.lock` 한 파일 |
| 후속 중복 검사 축소 코드로 `mise run setup` | 준비된 같은 격리 캐시에서 `READY`, 정책·잠금 8개 파일 hash 보존 |

cold-cache부터 복구까지의 진입점은 `python scripts/development_bootstrap.py setup|update`이며, 마지막 행에서 실제 mise task 진입점도 확인했다. 이 결과를 완전한 호스트 초기 설치나 다른 OS의 검증으로 해석하지 않는다.

## 회귀와 읽기 전용 검증 이력

후속 중복 검사 축소 전·후에 도구 설치가 `.venv`를 system-site-packages 노출 상태로 바꾸는 fixture를 두 mode에서 검증했다. resolver·sync 차단, nonzero, 오염 상태 보존과 실행 잠금 해제를 확인했으며 bootstrap 회귀 66개와 전체 deterministic tests 329개가 통과했다.

### 최신 head의 설치 없는 후속 검증

검증 source는 [`f70a8bd`](https://github.com/mols3131d/mols-agent-assets/commit/f70a8bd258895dbdd5616157131abb32b48d5836)이며 실행기 코드는 변경하지 않았다. 기존 Windows Python 3.13.11과 WSL Ubuntu Python 3.13.13을 사용했다.

| 검증 | 관측 결과 |
| --- | --- |
| Windows bootstrap 회귀 | 71개 통과. 실제 uv lock/sync를 수행하는 `test_native_uv_update_respects_upper_bound_and_setup_lock` 1개는 설치 승인이 없어 제외 |
| Windows 전체 회귀 | 334개 통과, 같은 native uv 통합 사례 1개 제외 |
| Windows setup/update `--dry-run` | 두 mode 모두 exit 0·`PLAN`. 정책 파일 8개의 SHA-256과 `.tmp` 존재 여부 보존 |
| Windows worktree를 WSL에서 직접 사용 | setup 계획은 통과. update는 `.git`의 Windows 드라이브 절대 경로를 WSL Git이 해석하지 못해 exit 1·`BLOCKED`. 실행기 결함으로 판단하지 않음 |
| WSL의 독립 Git snapshot | 로컬 저장소를 네트워크 없이 복제해 정확한 head에 고정. 두 mode 모두 exit 0·`PLAN`, 정책 파일 8개 hash 보존, `.tmp` 생성과 Git 변경 없음 |

WSL 검증은 셸 시작 파일을 읽지 않고 Python 절대 경로로 실행했다. 이 결과는 resolver·installer를 실행하지 않는 계획 경로의 근거일 뿐 Linux core readiness나 cold-cache 설치 성공을 증명하지 않는다.

## WSL Ubuntu 실제 설치와 복구

사용자가 앞서 설명한 실제 설치 검증 묶음을 승인한 뒤 실행했다. Source는 [`f70a8bd`](https://github.com/mols3131d/mols-agent-assets/commit/f70a8bd258895dbdd5616157131abb32b48d5836)이며 실행기 코드는 변경하지 않았다. 기존 mise `2026.6.2 linux-x64`와 Python `3.13.13`을 재사용했다. WSL Ubuntu x86_64의 `/var/tmp/pr-258-native-67x3tmgw` 아래에 독립 Git snapshot, HOME, XDG·mise data/config/state/cache, npm cache/config, uv cache와 임시 경로를 분리했다.

| 순서 | 관측 결과 |
| --- | --- |
| 빈 도구·패키지 캐시에서 setup | CLI 7종 설치·정확한 버전 검증과 Python sync/check, exit 0·`READY`. 정책 파일 8개의 SHA-256 보존 |
| 같은 환경에서 setup 반복 | exit 0·`READY`, 같은 8개 파일 hash 보존 |
| Python-only update | exit 0·`READY`, `uv.lock`만 변경. CLI lock·manifest·외부 자산 revision 보존 |
| update 후 setup | exit 0·`READY`, 갱신된 `uv.lock`을 포함한 8개 파일 hash 보존 |
| `mise run setup` | 실제 task 진입점에서 exit 0·`READY`, 정책 hash 보존 |
| update 후 전체 테스트 | managed uv `0.12.1`을 PATH에 넣고 실행. Native uv upper-bound/locked setup 통합 사례를 포함해 **335 passed**, skip/deselect 없음 |
| 최종 Git 상태 | snapshot의 `uv.lock` 한 파일만 변경. 실행 잠금 `.tmp/bootstrap.lock`은 해제 |

설치·버전 검증 대상은 uv `0.12.1`, Node `24.19.0`, rumdl `0.2.54`, Lefthook `2.1.10`, Biome `2.5.6`, Rulesync `40.2.0`, skills CLI `1.5.23`이다. Python 다운로드, 외부 Agent Asset 설치/projection, HOME Skills 및 Git hook 설치는 실행하지 않았다. 실제 작업 트리의 lock도 갱신하지 않았다. 첫 setup의 단일 관측은 22.09초, 반복 setup은 1.00초였으며 일반적인 성능 보장이나 완전한 host 초기 설치의 근거는 아니다.

최초 probe의 Node 실패는 검증 harness가 npm user/global config에 같은 파일을 지정한 탓이었다. 두 빈 설정 파일을 분리한 뒤 새 cold-cache 설치가 통과했다. 이를 실행기 결함으로 분류하지 않는다. 원본 실행 로그와 JSON hash 결과는 로컬 작업 트리의 `.tmp/pr-258-linux-install/`에 보존했다.

### Native strict-lock 실패 경계

준비된 설치본으로 인한 우회를 피하기 위해 각 실패 fixture의 mise data/cache/state를 다시 분리했다. 실제 `mise install --locked node@24.19.0`을 실행했으며 mock이나 dry-run을 사용하지 않았다.

| Fixture | 관측 결과 |
| --- | --- |
| `mise.lock` 없음 | exit 1, `No lockfile URL found ... on platform linux-x64 (--locked mode)`. Lock 생성 없음, Node 설치 없음 |
| Node 버전은 일치하지만 macOS platform 항목만 존재 | 동일 오류와 exit 1. Fixture lock의 bytes 보존, Linux Node 설치 없음 |

두 실패는 의도한 fail-closed 결과다. Lockfile을 자동 재생성하거나 다른 플랫폼·host Node로 fallback하지 않았다.

## 남은 실환경 검증

macOS 실행 환경을 확보하지 못해 native 설치·반복 복구·update E2E는 미검증이다. Linux arm64·musl 등 다른 OS/architecture도 이번 WSL x86_64 관측으로 확대하지 않는다. Python 최초 다운로드·OS-level containment·HOME native installer 검증은 이번 core 설치 묶음 밖이다. 이 기록은 merge 승인을 대신하지 않는다.
