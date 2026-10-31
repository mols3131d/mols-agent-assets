---
description: PR #258의 Windows cold-cache 설치, native mise 실행 위임 후보, 중복 설정과 환경 검사에 대한 후속 실증 결과 및 남은 OS 검증 범위를 확인할 때 참고합니다.
---

# PR #258 — 경량화·격리 설치 후속 검증

**Windows 격리 설치·반복 복구·Python-only update는 통과했다. npm 실행의 단순한 mise 위임은 호스트 명령 fallback이 재현되어 채택하지 않는다.** setup의 연속 중복 검사만 줄이고 기존 격리·잠금 방어를 유지한다.

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

## 안전 경계와 미검증 범위

후속 중복 검사 축소 전·후에 도구 설치가 `.venv`를 system-site-packages 노출 상태로 바꾸는 fixture를 두 mode에서 검증했다. resolver·sync 차단, nonzero, 오염 상태 보존과 실행 잠금 해제를 확인했으며 bootstrap 회귀 66개와 전체 deterministic tests 329개가 통과했다.

macOS host E2E와 Linux/WSL native 동등성은 미검증이다. 이 세션에서는 WSL·Docker 조회 권한을 확보하지 못했으므로 배포판·daemon·이미지 유무도 확정하지 않는다. 해당 환경이 준비되면 같은 격리 설치와 fallback 실험을 재현한다.
