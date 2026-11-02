---
description: 이 저장소의 Agent Asset 신설·개선·리뷰·평가·제공·폐기·문서 작업에서 상황에 맞는 절차와 기존 하네스·전문 자산을 선택하는 정본입니다.
---

# Agent Asset Workflows

이 문서는 **이 저장소가 관리하는 자산 작업의 상황별 연결**을 소유한다. 기술 지식은 전문 Skill과 공식 도구가, 상태·완료 판정은 [Agent Asset Lifecycle](agent-asset-lifecycle.md)이 소유한다. 이 저장소 밖의 소비 프로젝트에 이 절차를 적용하지 않는다.

## 작업 선택

현재 ref·대상·요청 결과를 [`AGENTS.md`](../../AGENTS.md)와 [작성 원본과 권한](source-authority.md)에서 확인한다. [저장소 전용 Skill](../../.rulesync/skills/repository-agent-asset-workflow/SKILL.md)은 작업의 상황을 아래 항목에 연결할 뿐, 기존 authority나 전문 기술을 대체하지 않는다.

| 상황 | 연결할 작업과 전문 소유자 |
| --- | --- |
| 신규·외부 자산 이식 | [신설·이식](#신설이식), `mols-agent-asset` design, 작성 원본·외부 dependency 정책 |
| 기존 자산 개선·타깃 적응 | [개선·튜닝](#개선튜닝), `mols-agent-asset` improve/tune |
| 품질 리뷰·검증·평가 | [리뷰·검증·평가](#리뷰검증평가), `mols-agent-asset` review/validate/eval |
| 배포 route·설치·소비 연결 | [제공·사용](#제공사용), `mols-agent-asset-find`, Rulesync·lock·route |
| rename·deprecation·삭제 | [은퇴·삭제](#은퇴삭제), 실제 소비자와 문서·fixture |
| 문서 개선·문서만 변경 | [문서 작업](#문서-작업), `mols-documentation`·문서 정책 |
| 중단·인계·복잡한 반복 | [인계](#인계), Lifecycle 및 필요 시 `mols-loops` |

워크플로는 단일 고정 파이프라인이 아니다. 필요한 절차만 조합하고, 반복 개선이 필요한 경우에만 `mols-loops`를 사용한다.

## 신설·이식

기존 owner로 해결할 수 있는지 확인하고, 외부 자산이면 **dependency 사용과 작성 권한 인수** 중 하나를 [Source Authority](source-authority.md)에서 결정한다. `mols-agent-asset`의 common/type design을 적용하고 [Agent Asset Design](agent-assets/README.md)을 참조한다. 재사용 원본과 이 저장소의 직접 사용은 별개다. 필요할 때만 [Rulesync](tooling/rulesync.md) 작성 규격을 검토한다. 구현 뒤에는 [문서 영향](#문서-영향-판정)과 [검증](#검증과-완료)을 확인한다.

## 개선·튜닝

현재 자산의 책임·활성화·소비자와 기존 계약을 확인하고 `mols-agent-asset`의 improve 또는 tune 및 유형별 reference를 선택한다. 작성 원본만 변경하고 중복 projection을 직접 수정하지 않는다. 지원 대상·API·사용법이 바뀌면 문서·예제·eval fixture에 미치는 영향을 함께 검토한다. 무관한 자산의 일괄 정규화는 하지 않는다.

## 리뷰·검증·평가

`mols-agent-asset`의 review, validate, eval은 각기 다른 claim이다. [Validation](validation.md)과 [Testing](testing.md)은 구조·저장소 동작, [Evaluation](evaluation.md)은 실제 agent 행동 근거를 소유한다. 정적 리뷰를 runtime 성능으로 주장하지 않는다. 읽기 전용 리뷰에서 코드 변경을 자동 실행하지 않으며, 수정 요청이 추가되면 해당 변경 절차로 이동한다.

## 제공·사용

`mols-agent-asset-find`로 발견·설치·동기화를 다루되 실행 전에 현재 연결과 권한을 확인한다. `src/` 정본, 외부 제공용 `route/`, 저장소 작업용 `.agents/route/`, 실제 설치·lock 상태를 혼동하지 않는다. 생성물은 소유 generator와 [Validation](validation.md)에 따라 동기화·검증하며 새 독립 정본을 만들지 않는다.

## 은퇴·삭제

원본뿐 아니라 실제 소비자, dependent asset, route, lock, 예제, 평가 fixture, 문서와 이전 경로를 범위 내에서 확인한다. 사용 중인 소비자와의 연결을 끊는 변경은 명시적 범위·권한을 확인하고 수행한다. 불필요한 archive나 흔적 보존을 기본으로 만들지 않는다. 필요한 마이그레이션과 문서 영향 확인을 완료하지 못하면 [Lifecycle](agent-asset-lifecycle.md)에 따라 인계한다.

## 문서 작업

문서의 독자·내용·구조는 `mols-documentation`이 담당한다. [Documentation](../documentation/README.md), [Asset Maintainer Documentation](../documentation/asset-maintainer-documentation.md)으로 정본 위치를 정하며, Markdown의 기계적 formatting은 `mols-markdown-maintenance`와 [Formatting](formatting.md)에 위임한다. 문서를 고쳤다는 이유로 자산 실행 의미를 암묵적으로 바꾸지 않는다.

## 문서 영향 판정

**작성 원본의 신설·변경·삭제**에서는 수정 파일만 보고 끝내지 않는다. 사용법·행동·설계 결정·지원 대상·폐기 안내가 독자에게 필요하면 정본 또는 유지보수 문서를 **함께 갱신**한다. 필요 없으면 기존 문서로 충분한지, 해당 문서가 없는 것이 적절한지 판단하고 PR·인계에 짧게 남긴다. 새 README의 무조건 생성은 요구하지 않는다.

`.inbox/`는 조사·draft·handoff를 위한 비정본 공간이다. 장기적으로 필요한 지식은 적절한 owner 문서로 채택해야 한다. 인박스 갱신만으로 문서 반영을 완료한 것으로 판단하지 않는다.

## 검증과 완료

원본이 바뀌었다면 [Lifecycle](agent-asset-lifecycle.md)의 문서·근거 종료 조건을 확인한다. 정적 source, 문서 인덱스, route와 Rulesync projection은 기존 `mise run generated validate`, `mise run rulesync-validate` 및 PR Gate 등에서 필요한 부분만 검증한다. 행동 평가는 [Evaluation](evaluation.md)을 따른다. PR·승인·Merge는 [GitHub](github.md), [CI](ci.md), [Git](vcs-git.md)의 권한과 근거에 맡긴다.

## 인계

권한·도구·정보 부족이나 미완료 검증으로 중단하면 **현재 ref, 완료·남은 범위, 근거, 차단 조건, 다음 시작점**만 남긴다. PR과 `.inbox/`는 상황에 따라 선택하는 working surface이며 이력을 전부 복제하지 않는다. 인계가 승인을 대체하거나 다음 수행자에게 새 권한을 부여하지 않는다.
