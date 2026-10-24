---
description: mols-dev-env-bootstrap-design의 설계 의도, 재사용 경계, setup/update와 설치 권한의 불변 조건, 리뷰·검증 방법을 유지보수할 때 사용합니다.
---

# Developer Environment Bootstrap Design — Maintainer Guide

`mols-dev-env-bootstrap-design`은 개발환경 부트스트랩의 **설계와 리뷰, 구현 준비 인계**만을 담당하는 재사용 Skill이다. 실제 구현은 에이전트의 일반 엔지니어링 역량과 대상 프로젝트의 지침이 담당하며, Skill 자체가 설치 작업을 실행하지 않는다. 처음 환경을 설정하고, 개발 중 반복적으로 상태를 맞추며, **사전에 승인된 버전 범위 안에서만 명시적으로 업데이트**하도록 설계할 때 사용한다.

실행 행동은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md)가 소유한다. 이 문서는 **왜 이런 책임을 선택했는지, 무엇을 보존해야 하는지, 어떻게 검토하는지**를 기록한다. 실행 절차를 다른 authority로 중복하지 않는다.

## Design goals

Skill을 선택한 작업자는 서로 다른 repository/tool manager에서도 다음 판단을 복원할 수 있어야 한다.

- **Lifecycle:** 최초 setup, 동일 명령 반복 실행을 통한 reconcile/repair, 명시적으로 요청한 update의 차이를 확인한다.
- **Version ownership:** 허용 범위를 정하는 manifest/config owner, 구체 버전 선택을 기록하는 lock/resolution owner, installer와 verification owner를 구분한다.
- **Safe provisioning:** 호스트 도구, 언어 인터프리터, 프로젝트 격리 환경·패키지, tool-manager cache 및 OS/사용자 공유 상태를 분리한다. 기존 자산 재사용은 **프로젝트의 관리 주체와 격리 계약을 먼저 충족**할 때만 설계한다. 특히 Python 인터프리터가 사용 가능하다고 전역 Python 패키지나 전역 Ruff를 프로젝트 의존성 대신 쓰지 않는다. 새 설치는 범위·영향을 제시해 사용자 허가를 받도록 한다.
- **Partial recovery:** 누락·실패한 의존 단계는 중단하되 독립적으로 가능한 단계는 계속 진행하도록 설계한다. 끝까지 준비되지 않은 부분을 완료로 포장하지 않는다.
- **Portable handoff:** 특정 도구의 vendor command를 알고 있어야만 설계할 수 있는 Skill이 아니라, 실제 프로젝트에 맞는 authoritative semantics를 확인하고 최소 실행 변경안을 제시한다.

## Scope and ownership

| Concern | Owner |
| --- | --- |
| 재사용 가능한 lifecycle, 범위·잠금·설치 권한·복구 설계 판단 | 이 Skill의 `SKILL.md` |
| 정확한 tool version 구문, lock/install/upgrade semantics | 실제 tool manager/package manager 공식 계약 |
| repository별 허용 범위, 설치 권한, CI 및 local bootstrap task | 대상 프로젝트의 source config·policy |
| Skill package/discovery/target metadata | 작성 framework와 실제 target/harness |
| 구현 코드, native integration, 테스트와 실행 로그 | 대상 프로젝트의 implementation/verification surface |
| 설계 의도·이식성·변경시 검토해야 할 불변 조건 | 이 유지보수 문서 |

특히 **권한은 스킬에서 생성되지 않는다.** 설계자가 tool-managed 설치를 합리적이라고 평가해도 현재 프로젝트·사용자 권한이 없는 OS/global/user-shared 변경을 실행해도 된다는 뜻은 아니다. `mise`·`uv`·`Rulesync`·`npm`은 적용 예시일 뿐 required dependency가 아니다.

## Durable decisions

1. **설계 Skill은 실행 스크립트가 아니다.** Script 설치·업데이트를 직접 수행하는 것은 사용자와 대상 repository가 별도로 요청·허용하는 작업이다. 일반 dependency update와 CI-only workflow design을 포괄하면 activation이 흐려진다.
1. **Setup은 미지의 최신 버전을 탐색하지 않는다.** 승인된 locked state에 맞추는 작업과 새 버전의 resolve/promote는 별도 intent다. Exact pin, prefix/range, floating Git ref를 동일하게 취급하지 않는다.
1. **'미설치'는 설치 권한이 아니다.** Bootstrap entrypoint가 없으면 그 안에서 자기 자신을 설치할 수 없다. Host prerequisite는 사람에게 경로를 제시한다. 사용자에게 설치 영향 범위를 설명하고 에이전트가 실제 실행하기 전 허가받는 설계를 우선한다. 명확한 하나의 설치 범위는 묶어 승인받을 수 있지만, 허가 없이 manager 공유 cache를 변경하는 것까지 허용하는 것은 아니다.
1. **부분 진척과 준비 완료는 다르다.** 독립 단계의 성공은 유용하지만 필수 의존성 누락 또는 검증 실패를 숨기지 않는다. 겉보기 간단함을 위해 전부 성공/전부 중단 중 하나로 강제하지 않는다.
1. **환경 격리가 재사용보다 우선이다.** Git 같은 독립 호스트 도구는 적합하면 재사용할 수 있으나 Python처럼 런타임과 패키지 환경이 분리되는 경우 인터프리터와 프로젝트 전용 dependency environment를 구분한다. 기존 PATH의 바이너리·전역 site-packages 존재만으로 재현성을 충족했다고 판정하지 않는다.
1. **Native owner 우선.** 이미 tool manager가 잠금, range, update, install, validation을 제공한다면 동일 동작을 custom YAML, wrapper, 범용 framework로 재구현하지 않는다. Wrapper가 필요하면 사전에 관찰된 orchestration/reporting gap을 근거로 한정한다.
1. **가장 작은 deployable package.** 모든 설계에서 함께 필요한 판단은 하나의 `SKILL.md`에 둔다. 분명한 조건부 loading 가치가 생기기 전에는 references나 script를 분할하지 않는다. 이 README는 유지보수 대상이지 runtime resource가 아니다.

## Review / validation

**적용 사례:** 새 개발자 온보딩 + 장기 update, 기존 setup의 무해한 재실행, 허용 major 범위를 지키는 lock refresh, missing Git·Node로 인한 단계별 skip/continued progress, native Skill installer의 사용자 홈 변경 위험.

**비적용 사례:** lockfile의 개별 package 한 건 업데이트, OS에 도구 한 개 설치, CI admission gate만 설계. 이름이 유사한 bootstrap script 관련 task라 해도 lifecycle **설계 또는 리뷰**가 핵심이 아니면 이 Skill을 호출할 이유가 없다.

유지보수 시에는 해당 사례로 description selection과 행동 계약을 별도로 검토한다. Skill `name`과 package path, 배포용 generated route 일치 및 Rulesync structural validation을 확인한다. 정적·의미 검토 결과를 실제 tool execution이나 runtime behavioral eval 통과로 표시하지 않는다.

[Evaluation](evaluation.md)은 positive/near-miss와 behavior의 분리, 공통 Promptfoo entrypoint, 실제 로컬 모델 결과와 남은 capability 한계를 소유한다.

## Repository application

이 저장소의 **개발환경 구축·설치 승인 정책 정본은 [Development Environment](../../development/development-environment.md)**이며, 도구별 실행 안내는 [mise bootstrap 안내](../../references/tooling/mise.md), 실제 실행 로직은 [`development_bootstrap.py`](../../../scripts/development_bootstrap.py)가 소유한다. 이 Skill은 그 저장소 정책을 대체하거나 복제하지 않는다. Exact tool pin 유지, bounded Python update, HOME/hook/projection의 기본 분리는 이 repository의 선택이며 portable Skill의 필수 도구·CLI가 아니다. 해당 runner의 deterministic test success를 Skill activation 또는 runtime behavioral eval 통과로 취급하지 않는다.

## Upstream references

- [Agent Skills Specification](https://agentskills.io/specification) — Skill package, metadata, description
- [mise lockfile](https://mise.jdx.dev/dev-tools/mise-lock.html) — 버전 요청과 resolved version 분리의 tool-specific 사례
- [mise automatic installation](https://mise.jdx.dev/dev-tools/) — task 시작 전 설치의 권한 경계 사례
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) — update와 locked reconcile의 tool-specific 사례

이 원본들은 변화할 수 있다. 그 세부 명령과 옵션을 Skill의 portable invariant로 승격하지 않고, 실제 적용할 때 해당 프로젝트 버전의 공식 문서를 다시 확인한다.
