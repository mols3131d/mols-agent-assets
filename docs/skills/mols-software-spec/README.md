---
description: 재사용 Software Spec/Test-driven Skill의 산출물·워크플로 분리, 리뷰 복귀, 패키지 스크립트와 다른 작업 관리 자산의 책임 경계를 유지보수할 때 참고합니다.
---

# Software Spec Framework — Maintainer Guide

실행·활성화 계약의 정본은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-software-spec/SKILL.md)이다. 이 문서는 구현 결정의 이유와 유지보수·검증 경계만 보존한다. 관리 저장소의 하네스·인박스·다른 Skill을 외부 소비자의 숨은 실행 전제로 삼지 않는다.

## Architecture Decision

**작업 관리와 소프트웨어 명세·테스트 기반 개발을 두 개의 독립 선택 가능한 Skill로 분리**했다. 이 패키지는 한 소프트웨어 변경의 기대 동작, 검증 가능성, 구현 정합성 및 Review 복귀를 담당한다. 작업 분해·우선순위·백로그·여러 작업의 상태 관리와 인계 자체는 기존 task provider와 별도 Work Management owner에 둔다.

`assets/artifacts.json`은 **산출물 종류**, `assets/workflows/*.json`은 **순서·선행 단계와 복귀 후보**, `references/`는 사람·모델이 이해할 의미, `scripts/flow.py`는 구조·전이 판단의 결정적 subset을 소유한다. 동일한 내용을 별도 정본으로 재정의하지 않는다. 제품 코드·테스트는 프로젝트의 원래 위치에 남고 별도의 진행 상태 DB나 tracker는 만들지 않는다.

## Default and Flexibility

사용자 제안에 따른 기본 워크플로는 Proposal → Research → Plan → Specification → Test Design → Test Implementation → Code Implementation → Review이다. 이는 test-first를 선호하는 **전체 흐름 프리셋**이지 모든 버그 수정이나 기존 구현 검토의 필수 8개 파일을 뜻하지 않는다. `focused.json`은 훨씬 짧은 명세·구현·검토 흐름을 보여준다. Artifact 규격을 변경하지 않고 workflow 순서를 바꾸고 단계 의존성을 검증할 수 있는 것이 핵심이다.

Review에서 목표·근거·스펙·테스트·코드 중 결함 원인을 특정하고 해당 단계로 복귀한다. Workflow의 `after` 의존성으로 후보 재확인 범위를 계산하지만, 모든 downstream 산출물을 자동 수정하거나 유효성 실패로 처리하지 않는다. 테스트가 코드보다 먼저 작성된 정상적인 red 상태와 실제 결함을 구분한다. 또한 Review는 별도 mandatory 문서 타입이 아니다.

## Portable Runtime Boundary

단일 Agent Skill 패키지의 `SKILL.md`가 진입점이며, 파일을 직접 다루는 CLI 환경에서는 Python 표준 라이브러리로 작성된 내부 스크립트를 선택적으로 실행할 수 있다. ChatGPT Chat에서는 연결된 리소스·권한·코드 실행 환경이 동일하다고 보장할 수 없으므로 구조·전이 검사 미실행을 숨기지 않는다. OpenSpec 등 기존 spec store가 있으면 이 Skill 때문에 중복 정본을 생성하지 않는다. 외부 설치·배포·native activation은 실제 소비 환경에서 검증해야 한다.

## Maintenance and Validation

- Artifact 종류/ID 또는 파일명 변경 → 영향받는 Workflow와 기존 소비자·문서 산출물의 이관을 확인한다.
- Workflow 순서/의존 관계 변경 → 결함의 복귀 경로, 재확인 대상, 실제 유지되는 산출물의 범위를 검토한다.
- Script 변경 → [deterministic tests](../../../tests/skills/mols-software-spec/test_flow.py)로 기본·focused 구성, 스키마 실패, spec/test stage 복귀, multi-finding, blocked/candidate complete를 확인한다.
- 모델이 실제로 Skill을 선택하고 올바른 소스·근거를 확인하는지는 별도 **runtime behavior evaluation**으로 다룬다. 정적 구조 테스트와 로컬 Python 실행은 ChatGPT Chat 지원의 증거가 아니다.
- 스크립트와 Skill 경로를 현재 프로젝트에 복제하는 설치·추적 체계를 만들지 않는다. 현재 재사용 작성 원본과 관리 문서는 이 저장소가 소유하나, 외부 프로젝트의 실행 규칙은 그 환경이 소유한다.

## Known Limits

이 첫 구현은 Artifact/Workflow 형식 검증과 Review routing을 제공하며, **스펙 저장소 전체 상태 관리, 코드·테스트 실행, CI 통과 여부 판단, 자동 기록·동기화, 여러 변경 간 의존성 계산**을 구현하지 않는다. 결정적인 실제 검증기는 프로젝트 테스트/CI를 재사용한다. 런타임 설치·Dogfood 및 다중 세션 재개 평가는 별도로 수행해야 한다.
