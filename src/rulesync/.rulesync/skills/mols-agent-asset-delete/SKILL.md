---
name: mols-agent-asset-delete
description: >-
  Delete or retire a managed Agent Asset, such as a Skill, Rule, agent,
  subagent, prompt, or related runtime resource, with impact-aware cleanup
  of its source, consumers, references, and validation assets. Use when
  the intended outcome is removing an agent-facing capability or its
  canonical source. Not for ordinary file cleanup, a simple rename, or
  uninstalling an externally owned dependency from one consumer.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Agent Asset Deletion

Agent Asset을 **의도한 범위에서 완전히 제거하거나 안전하게 은퇴**시키는 작업을 조율한다. 삭제 명령 자체보다 소유권, 실제 소비 관계, 파생물과 검증 가능한 종료 상태를 다룬다. 경로·도구·권한·검증 명령은 대상 프로젝트와 작성 프레임워크가 소유한다.

## 적용 경계

- 요청이 작성 원본이나 agent-facing capability의 제거인지, 한 소비 환경의 설치 해제인지, 이름 변경·대체·일시적 비활성화인지 먼저 구분한다. 설치 해제나 단순 rename만 요구되면 이 워크플로를 확대 적용하지 않는다.
- 파일·디렉터리의 존재, route 등재, lock 항목, 실제 설치·실행은 서로 다른 사실이다. 이름만 같다는 이유로 별개의 자산을 동일하게 취급하지 않는다.
- 요청과 프로젝트 지침이 허용하는 경계에서만 변경한다. 외부 저장소·계정·공유 배포물의 수정 권한을 현재 저장소 접근 권한에서 추론하지 않는다.

## 삭제 워크플로

1. **대상 확정** — repository/workspace, ref, canonical owner, 자산 식별자·별칭, 제거 목표와 수정 가능한 범위를 확인한다. source·설치 사본·생성물·외부 dependency·과거 기록을 분리하고 기존 작업 상태를 보존한다.
2. **영향 추적** — 대상의 owned files와 supporting resources, 대상이 의존하는 항목, 대상을 참조·실행하는 소비자를 찾는다. 경로와 이름뿐 아니라 선택 route, config/lock, imports, 다른 Agent Asset, commands/automation, tests/evals/fixtures, 예제와 문서에서 **현재 유효한 참조**를 확인한다. 외부 소비자는 관찰 가능한 범위와 미확인 범위를 구분한다.
3. **처리 결정** — 각 영향 항목을 `삭제 / 소비자 이관·수정 / 유지 / 차단·인계`로 판정한다. 아직 필요한 소비자가 있으면 대체 경로와 이전 범위가 확인된 뒤 제거한다. 단순히 검색 결과가 없다는 이유로 사용자가 없다고 단정하지 않는다. 필요성이 입증되지 않은 archive·tombstone·deprecated stub는 만들지 않는다.
4. **변경 범위 고정** — 실행 전 source 및 참조별 변경·검증 계획을 세우고, 파괴적 외부 작업·복구가 어려운 삭제는 정확한 대상과 별도 승인 요구를 확인한다. 공유 파일에서는 해당 자산의 계약만 제거한다. 불명확한 소유권, 필요한 외부 이관 권한 또는 영향 분석의 핵심 근거가 없으면 위험 변경을 중단하거나 안전한 범위만 수행한다.
5. **제거와 정리** — 의존 소비자의 이관·연결 수정 후 canonical source와 전용 resources를 제거한다. source-owned route/config/dependency·lock, 테스트/평가 fixture와 문서의 낡은 연결을 필요한 범위에서 정리한다. 생성 결과는 소유 generator로 갱신하고 별도 정본처럼 수동 관리하지 않는다. 다른 기능이 공유하는 테스트·참고 자료는 남긴다.
6. **잔여 영향 검증** — 원래 식별자·별칭·경로와 실제 사용 경로를 다시 탐색하고, 변경된 구문·route·dependency·생성물·tests를 프로젝트의 공식 수단으로 점검한다. 남아 있는 과거 기록과 의도된 migration 안내는 잔여 버그로 취급하지 않는다. 정적 근거와 실제 runtime 동작 증거를 구별한다.

## 종료 조건과 인계

- 완료는 제거 대상이 요청한 범위에서 처리되고, 영향을 받는 **현재 소비자**와 문서·검증 자산이 의도한 상태이며, 수행한 검증의 근거가 제시될 때만 주장한다.
- 보고에는 `제거 / 이관·수정 / 의도적으로 유지`한 항목, 미확인 소비 범위, 실행하지 못한 검증과 잔여 위험을 구분한다. 불필요한 전체 삭제 로그나 archive를 새로 남기지 않는다.
- 삭제를 막는 소비자·승인·도구·호환성 문제가 남으면 그 장애와 다음 결정 지점을 인계한다. 일부 파일을 지웠다는 이유로 전체 삭제 성공으로 보고하지 않는다.

## 책임 경계

자산 설계·의미 검토·평가는 해당 전문 자산과 대상 계약에, 설치·동기화는 설치 메커니즘에, branch·PR·merge는 해당 저장소 정책에 맡긴다. 이 Skill은 보편적인 영향 분석과 안전한 제거 순서만 소유하며 특정 저장소의 디렉터리 구조, 명령, 승인을 새로 정의하지 않는다.
