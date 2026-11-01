---
description: PR #264의 도구 버전 고정 정책, 2026-11-02 upstream 안정 릴리스 대조, 후속 검증·교체 우선순위를 확인할 때 참고합니다.
---

# PR #264 — 도구 버전 선택·갱신 검토

> **기준일:** 2026-11-02. 릴리스는 이날 확인한 공식 GitHub `releases/latest` 응답이다. 이 표는 일회성 연구·인계 근거이지 버전 정본이나 업데이트 완료 보고가 아니다.

## 판단

**Exact pin을 버리지 않는다.** `scripts/development_bootstrap.py`는 CLI 7종의 `X.Y.Z` 형태를 요구하며, `mise.lock`에 잠긴 도구로 `setup`을 재현한다. `latest`·`lts`·range를 선언만 바꾸면 실행 계약과 충돌한다. 반대로 보안·지원 종료·호환성 위험을 무시하고 pin을 오래 유지하는 것도 적절하지 않다. **명시적으로 검토하고 버전을 채택한 다음, 다시 exact pin과 lock으로 고정하는 운영 방식**을 우선한다.

## 현재 선택과 공식 최신 안정 릴리스

| 대상 | 현재 정본 선택 | 확인한 upstream 릴리스 | 다음 검토 |
| --- | --- | --- | --- |
| uv | `0.12.1` (`mise.toml`) | [`0.13.6`](https://github.com/astral-sh/uv/releases/tag/0.13.6) | **우선:** [`0.13.4` 인증서 권고](https://github.com/astral-sh/uv/releases/tag/0.13.4) 반영 여부와 bootstrap·Python lock 호환성 |
| Node.js | `24.19.0` | [`26.13.0` Active LTS](https://github.com/nodejs/node/releases/tag/v26.13.0) | 기존 24.x도 지원 중. [`24.22.2` LTS](https://github.com/nodejs/node/releases/tag/v24.22.2) 패치 또는 26.x 전환을 npm CLI·Promptfoo 호환성에 따라 선택 |
| rumdl | `0.2.54` | [`0.3.2`](https://github.com/rvben/rumdl/releases/tag/v0.3.2) | **우선:** parser·Tokio 관련 [보안 권고 2건](https://github.com/rvben/rumdl/releases/tag/v0.3.2) 검토, config·Markdown 출력 diff |
| Lefthook | `2.1.10` | [`2.2.2`](https://github.com/evilmartians/lefthook/releases/tag/v2.2.2) | Git hook validation과 사용자 hooksPath 영향 확인 |
| Biome | `2.5.6` | [`2.6.4`](https://github.com/biomejs/biome/releases/tag/%40biomejs/biome%402.6.4) | `biome.json` schema·formatter 출력 diff, CLI 운영 범위 |
| Rulesync | `40.2.0` | [`43.4.2`](https://github.com/dyoshikawa/rulesync/releases/tag/v43.4.2) | 설정·lock schema·generated projection diff 및 downstream compatibility |
| skills CLI | `1.5.23` | [`1.7.4`](https://github.com/vercel-labs/skills/releases/tag/v1.7.4) | 잠긴 외부 Skill revision을 변경하지 않고 installer·vendor payload 호환성 확인 |
| Promptfoo | `0.122.0` (`promptfoo_run.py`) | [`0.125.1`](https://github.com/promptfoo/promptfoo/releases/tag/0.125.1) | eval runner·grader/model 조건 비교 가능성. mise 관리 CLI와 별도 pin |

## 안전한 버전 변경 계약

1. 공식 릴리스 노트와 보안 영향, 현재 버전의 지원 상태를 확인한다. '최신' 번호가 아니라 **프로젝트에서 수용 가능한 후보**를 선택한다.
1. `mise.toml`의 exact pin과 `mise.lock`을 함께 갱신한다. 현재 exact pin에 `mise lock --bump`만 호출하면 새 버전을 선택하지 않는다. 기존 플랫폼의 checksum·URL과 필요시 npm dependency sidecar를 native tool로 재생성·검토한다.
1. `scripts/development_bootstrap.py`의 명령·버전 검증, `biome.json` schema, Node와 Promptfoo 호환성, formatter 산출물, Rulesync lock/projection을 실제 영향을 기준으로 검증한다.
1. 설치·업데이트 실행은 사용자 승인을 얻어 격리된 환경에서 수행하고, 관련 검증·PR Gate 통과 후 병합한다. `mise run update`는 **Python 의존성(`uv.lock`)만** 갱신하므로 CLI pin refresh로 사용하지 않는다.

## 이번 PR에 적용한 경계

- **반영:** `docs/tools/README.md`의 관리 기준, `docs/tools/mise.md`의 exact pin 갱신 절차와 first-use locked install, 도구별 호환성 점검 보강.
- **미수행:** host 도구 설치, `mise.toml`·`mise.lock` 또는 Promptfoo runner 버전 갱신, 바이너리 해시 생성·검증, Windows·WSL·macOS runtime 검증. 현재 lock과 테스트 결과를 새 버전의 검증으로 해석하지 않는다.
- **권고:** uv와 rumdl의 upstream 보안 대응을 우선 확인한 뒤 실제 CLI pin refresh 작업을 별도 검증 대상으로 진행한다. Node 26·Rulesync 43 등 큰 전환은 필요성·호환성에 따라 분리한다.
