---
description: 재사용 Software Spec/Test-driven Skill의 산출물·워크플로 분리, 리뷰 복귀, 패키지 스크립트와 다른 작업 관리 자산의 책임 경계를 유지보수할 때 참고합니다.
---

# Software Spec Framework — Maintainer Guide

실행·활성화 계약의 정본은 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-spec-stdd/SKILL.md)이다. 이 문서는 구현 결정의 이유와 유지보수·검증 경계만 보존한다. 관리 저장소의 하네스·인박스·다른 Skill을 외부 소비자의 숨은 실행 전제로 삼지 않는다.

## Architecture Decision

**작업 관리와 소프트웨어 명세·테스트 기반 개발을 두 개의 독립 선택 가능한 Skill로 분리**했다. 이 패키지는 한 소프트웨어 변경의 기대 동작, 검증 가능성, 구현 정합성 및 Review 복귀를 담당한다. 작업 분해·우선순위·백로그·여러 작업의 상태 관리와 인계 자체는 기존 task provider와 별도 Work Management owner에 둔다.

`assets/artifacts.json`과 `assets/templates/`는 **산출물 종류와 최소 문서 구조**, `assets/workflows/*.json`은 **순서·선행 단계와 복귀 후보**, `references/`는 사람·모델이 이해할 의미를 소유한다. `scripts/flow.py`는 읽기 전용 Workflow/Review 검사를, `scripts/store.py`는 명세의 현재 기준값과 완료된 변경의 안전한 병합·아카이브를 지원한다. 동일한 내용을 별도 정본으로 재정의하지 않는다. 제품 코드·테스트는 프로젝트의 원래 위치에 남고 별도의 진행 상태 DB나 tracker는 만들지 않는다.

## Default and Flexibility

사용자 제안에 따른 기본 워크플로는 Proposal → Research → Plan → Specification → Test Design → Test Implementation → Code Implementation → Review이다. 이는 test-first를 선호하는 **전체 흐름 프리셋**이지 모든 버그 수정이나 기존 구현 검토의 필수 8개 파일을 뜻하지 않는다. `focused.json`은 훨씬 짧은 명세·구현·검토 흐름을 보여준다. Artifact 규격을 변경하지 않고 workflow 순서를 바꾸고 단계 의존성을 검증할 수 있는 것이 핵심이다.

Review에서 목표·근거·스펙·테스트·코드 중 결함 원인을 특정하고 해당 단계로 복귀한다. Workflow의 `after` 의존성으로 후보 재확인 범위를 계산하지만, 모든 downstream 산출물을 자동 수정하거나 유효성 실패로 처리하지 않는다. 테스트가 코드보다 먼저 작성된 정상적인 red 상태와 실제 결함을 구분한다. 또한 Review는 별도 mandatory 문서 타입이 아니다.

## Domain Spec Store and Change Completion

기본 Spec Root는 `spec/`를 **제안**하며 기존 프로젝트 owner가 있으면 그 경로를 우선한다. `changes/<change-id>/`는 진행 중인 **한 소프트웨어 변경**의 제안·조사·계획·테스트 설계와 domain delta를 보관한다. `specs/<domain-path>/spec.md`는 현재 제품이 지켜야 하는 장기 **도메인 정본 스펙**이다. `domain-path`는 예컨대 `payments/refunds/validation`처럼 여러 계층을 허용한다.

Review PASS와 실제 검증 근거를 확인한 뒤 `changes/<change-id>/specs/<domain-path>/spec.md`의 ADDED/MODIFIED/REMOVED 요구사항을 해당 도메인 정본에 병합하고 원본 변경을 `changes/archive/<date>-<change-id>/`에 보존한다. 수정되지 않은 요구사항은 보존한다. `base-sha256`은 변경이 기초로 삼은 정본 내용을 고정해 동시 변경을 무단 덮어쓰지 않도록 한다. 도메인 전체 삭제는 이 버전에서 금지하며 명시적 처리 정책을 별도로 결정한다.

CLI에서는 `store.py archive ... --review ...`가 변경 미리보기를 제공하고 `--apply`를 별도로 명시해야 실제 정본 수정·아카이브가 실행된다. 참조한 Review/CI 근거의 진위는 스크립트가 검증하지 않으며, 소비 프로젝트의 실제 테스트와 승인 절차를 따르는 책임은 남는다. GitHub Chat runtime에서는 원격 파일의 현재 SHA·연결 계정·실제 쓰기 성공을 확인해야 한다. 자세한 정본 계약은 [Spec Store](../../../src/rulesync/.rulesync/skills/mols-spec-stdd/references/spec-store.md)에 둔다.

## Portable Runtime Boundary

단일 Agent Skill 패키지의 `SKILL.md`가 진입점이며, 파일을 직접 다루는 CLI 환경에서는 Python 표준 라이브러리로 작성된 내부 스크립트를 선택적으로 실행할 수 있다. ChatGPT Chat에서는 연결된 리소스·권한·코드 실행 환경이 동일하다고 보장할 수 없으므로 구조·전이 검사 미실행을 숨기지 않는다. OpenSpec 등 기존 spec store가 있으면 이 Skill 때문에 중복 정본을 생성하지 않는다. 외부 설치·배포·native activation은 실제 소비 환경에서 검증해야 한다.

## Maintenance and Validation

- Artifact 종류/ID 또는 파일명 변경 → 영향받는 Workflow와 기존 소비자·문서 산출물의 이관을 확인한다.
- Workflow 순서/의존 관계 변경 → 결함의 복귀 경로, 재확인 대상, 실제 유지되는 산출물의 범위를 검토한다.
- Script 변경 → [Workflow deterministic tests](../../../tests/skills/mols-spec-stdd/test_flow.py)와 [Spec Store tests](../../../tests/skills/mols-spec-stdd/test_store.py)로 단계 복귀, 중첩 도메인 병합, stale baseline, 다중 도메인 사전 검증, Review 결과, 아카이브 충돌을 확인한다.
- [Behavior eval cases](../../../evals/skills/mols-spec-stdd/cases.json)는 spec-driven 요청의 활성화, 작업 관리·일상 코딩·단독 테스트 리뷰의 비활성화, Review 복귀 및 ChatGPT 실행 제약을 확인하기 위한 대표 사례다. **Fixture를 추가한 사실은 실제 모델 평가 통과를 뜻하지 않는다.**
- 모델이 실제로 Skill을 선택하고 올바른 소스·근거를 확인하는지는 별도 **runtime behavior evaluation**으로 다룬다. 정적 구조 테스트와 로컬 Python 실행은 ChatGPT Chat 지원의 증거가 아니다.
- 스크립트와 Skill 경로를 현재 프로젝트에 복제하는 설치·추적 체계를 만들지 않는다. 현재 재사용 작성 원본과 관리 문서는 이 저장소가 소유하나, 외부 프로젝트의 실행 규칙은 그 환경이 소유한다.

## Known Limits

이 구현은 Artifact/Workflow 형식 검증·Review routing과 변경 delta를 도메인 정본에 병합·아카이브하는 **명시적 완료 작업**을 제공한다. 그러나 **제품 코드·테스트 실행, CI 통과 여부 판단, 여러 변경 간 의존성 계산·스케줄링, 전역 진행 상태 DB, 동시 archive의 트랜잭션 보장**은 구현하지 않는다. 결정적인 실제 검증기는 프로젝트 테스트/CI를 재사용한다. 런타임 설치·Dogfood 및 다중 세션 재개 평가는 별도로 수행해야 한다.
