---
description: PR #257에서 Rulesync Git transport 대신 GitHub transport를 유지하도록 변경 범위와 검증 기준을 정할 때 참고하는 작업 요청입니다.
---

# PR #257 — Rulesync transport를 `github`로 유지

> **2026-10-25 구현 상태:** GitHub transport 복귀·v40 공식 lock migration·Git 전용 wrapper 제거와 Windows frozen 설치를 완료했다. 8개 integrity 변경은 동일 98개 파일의 Windows/POSIX 경로 hash 차이로 입증했고 revision은 유지했다. 실제 검증과 CI 승인 대기는 [인계 보고서의 후속 실행 결과](rulesync-v40-handoff.md#후속-실행-결과--2026-10-25-kst)를 따른다. 아래 본문은 최초 변경 요청을 보존한다.

## 요청 결론

[PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257)의 Rulesync 원격 소스는 **`git`으로 전환하지 말고 기존 `github` transport를 유지**한다. 현재 두 소스는 모두 GitHub 공개 저장소이며, Git transport 전환으로 얻는 필수 기능이 확인되지 않은 반면 Git checkout의 줄바꿈 보정과 인증 환경 보존을 위한 별도 설치 래퍼가 추가되었다.

이 문서는 **PR 수정 지시**이며 변경이 이미 적용되었다는 뜻이 아니다. 아래 구현과 검증이 끝나기 전에는 이 방향의 변경 완료 또는 머지 준비 완료로 간주하지 않는다.

- 대상 PR HEAD(작성 기준): `ac13442fdde981d303429e1ca5f601bc9515bb53`
- 범위: Rulesync transport 선택과 그 선택에 따라 생긴 설정·설치 경로·문서·테스트의 정합성
- 범위 밖: 외부 Skill 버전 업데이트, PC별 유효한 로컬 설정 삭제, unrelated Git hook 격리 개선의 무조건적인 되돌리기

## 판단 근거

- **요구 대비 단순성:** 현재 원격 소스는 `mols3131d/mols-agent-assets`, `dyoshikawa/rulesync` 두 GitHub 저장소다. GitLab, 자체 Git 서버, 로컬 `file://` 소스 또는 SSH 기반 접근이 이번 PR의 요구사항은 아니다.
- **불필요한 운영 경로 제거:** Git transport 도입 후 `core.autocrlf=false` 적용, 상위 `GIT_CONFIG_*` 보존, 별도의 `rulesync-install` 태스크와 Python 래퍼·회귀 테스트가 필요해졌다. GitHub transport를 유지한다면 이 중 **Git clone LF 보정을 위한 전용 경로**가 여전히 필요한지 재평가하고 불필요하면 제거할 수 있다.
- **기존 동작 보존:** 소스 식별자와 transport만 원래 형태로 되돌리고 이미 잠긴 dependency의 commit, Skill 선택과 integrity는 유지해 불필요한 dependency 갱신을 피한다.
- **선택의 대가:** `github` transport는 GitHub API/인증·rate limit의 영향을 받는다. 따라서 Git이 무조건 나쁘다는 결론은 아니다. 향후 비-GitHub 저장소나 Git 인증 체계 사용이 실제 요구사항이 되면 그때 `git`을 다시 검토한다.

## PR 수정 요청

1. [`rulesync.jsonc`](../../rulesync.jsonc)의 두 소스를 `mols3131d/mols-agent-assets`, `dyoshikawa/rulesync` shorthand로 돌리고 `transport: "github"`를 사용한다. 기존 `ref`, `path`, `skills`, `targets`는 유지한다.
1. [`rulesync.lock`](../../rulesync.lock)의 source 키도 설정과 일치시키되 `requestedRef`, `resolvedRef`, `resolvedAt`, 모든 Skill의 `integrity`를 보존한다. Transport 복귀에 `install --update`를 사용하지 않는다.
1. [`mise.toml`](../../mise.toml)의 `setup` 설치 단계를 단순화한다. Git transport에만 필요했던 `scripts/agent_assets/rulesync_install.py`, `rulesync-install` task와 전용 `tests/scripts/agent_assets/test_rulesync_install.py`는 **다른 사용처가 없는지 확인한 뒤** 제거한다. 후속 구현에서 삭제했으며 `rulesync install --frozen`을 직접 호출한다.
1. [Rulesync 운영 문서](../../docs/references/tooling/rulesync.md)와 [mise 운영 문서](../../docs/references/tooling/mise.md)의 Git transport·LF 전용 설치 안내를 새 경로에 맞게 정리한다. Git에서 제외된 `mise.local.toml`, `rulesync.local.jsonc`의 오래된 중복 override는 **각 PC에서 검토 후** 정리하도록 안내하되, 필요한 PATH·인증 등 사용자별 설정은 보존한다.
1. 공통 `PYTHONUTF8=1` 설정과 [`tests/conftest.py`](../../tests/conftest.py)의 Git hook 환경 격리는 Git transport와 독립적으로 필요한 개선인지 판단해 **유효하면 유지**한다. 관련 없는 개선까지 기계적으로 되돌리지 않는다.
1. 실제 변경에 맞게 PR 제목·본문의 목적, 검증 결과, 남은 위험을 갱신한다. 이 인박스 문서를 구현 완료의 근거로 사용하지 않는다.

## 완료 조건 및 검증

- `rulesync.jsonc`와 `rulesync.lock`의 source 식별자가 일치하며 `github` transport를 사용한다.
- 기존 11개 Skill의 resolved commit과 integrity, 설치 대상·경로가 의도 없이 바뀌지 않는다.
- 변경된 경로로 `rulesync install --frozen`을 실행해 설치와 lock 불변을 확인한다. 설치 실행이 어려운 환경이면 **미검증**이라고 명시한다.
- 관련 설정·문서·테스트에서 제거된 Git 전용 설치 경로를 참조하지 않으며, 저장소의 source validation, deterministic tests, generated projection validation과 최신 PR Gate가 통과한다.
- PC별 설정 정리는 원격 PR이 자동으로 수행하지 못한다는 점과, GitHub API 인증 및 rate limit 관련 잔여 운영 조건을 PR에 기록한다.

## 참고

- [PR #257](https://github.com/mols3131d/mols-agent-assets/pull/257) — 변경 대상과 당시 검증 근거
- [Rulesync 운영 문서](../../docs/references/tooling/rulesync.md) — 현재 저장소 설치 경로
- [Rulesync 공식 문서 — Declarative Sources](https://rulesync.dyoshikawa.com/guide/declarative-sources.html) — transport 및 선언형 소스 기능

**현재 상태:** 설정·공식 lock migration·wrapper 제거 및 Windows 재검증 완료. 사용자 push 승인 후 root frozen CI의 실제 11개 Skill 설치·lock 불변을 확인하고 High thread를 해결했다. 최신 실행 근거는 [인계 보고서](rulesync-v40-handoff.md#승인-후-게시검증)와 PR 본문을 따른다. Draft 해제·merge는 별도 승인 없이는 하지 않는다.
