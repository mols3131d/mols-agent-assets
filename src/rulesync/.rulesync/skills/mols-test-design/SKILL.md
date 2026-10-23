---
name: mols-test-design
description: >-
  Design or review software tests for observable behavior, failure paths, and regression
  risk. Use when selecting tests, oracles, levels and isolation, or reviewing
  test validity, cross-component coupling, flakiness, mocking and gaps.
  Also apply to a material test-design subtask within coding work, but not to ordinary
  implementation, test-runner debugging, module redesign, CI gates or agent/LLM evaluation
  when independent test-design judgment is not requested.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mols Test Design

중요한 software behavior를 **실제로 구분하고 보호할 수 있는 최소한의 테스트**를 설계하거나, 기존 테스트가 그 목적을 달성하는지 검토한다. 테스트 수·coverage·기법 자체가 목표는 아니다.

## Design Judgment

적용되는 요구사항과 repository contract, 기존 test·failure evidence를 먼저 확인한다. 모든 단계나 출력 양식을 매번 강제하지 않고 현재 질문의 중요한 판단만 수행한다.

1. **Protect the contract** — 사용자·consumer가 관찰할 동작, 요청된 산출물·연결 경로, 불변식, 변경 영향과 실패 비용을 식별한다. 위험이 큰 미검증 계약부터 보호하되 기존 검증이 충분하거나 추가 테스트가 의미 있는 결함 구별·수용 근거를 늘리지 않으면 테스트를 더 만들지 않는다.
2. **Ground the oracle** — 성공·실패를 구별할 관찰점과 기대값을 명세, 외부 계약, 확정된 예시, 신뢰할 만한 기준 동작 또는 독립적인 성질에서 도출한다. **현재 구현을 정답의 유일한 근거로 삼지 않는다.** 가능한 경우 올바른 동작은 수용하고 중요한 잘못된 동작은 거부하는지 양방향으로 확인한다. 명세·기준 동작이 불명확하거나 충돌하면 임의로 기대값을 확정하지 말고 gap 또는 가정을 드러낸다.
3. **Discriminate failures** — 대표 정상·경계·예외·회귀 사례 중 중요한 결함을 구별할 최소 집합을 고른다. *어떤 현실적인 잘못된 구현이 이 검증에서 실패해야 하는가?*를 따져, 실행만 하는 테스트·동어반복 assertion·구현 세부에 과적합된 기대값을 경계한다.
4. **Choose the observation boundary** — 로컬 순수 동작에는 좁은 test를, 실제 의존성·상태·권한·API 계약·사용자 흐름이 핵심일 때는 해당 경계를 관찰하는 integration·contract·end-to-end 검증을 고려한다. 각 작업자가 다른 컴포넌트의 비공개 구현을 몰라도 자기 책임 범위를 변경·검증할 수 있도록, 가능하면 소유한 동작과 안정된 소비자·제공자 계약을 검증한다. 내부 호출 순서나 자료구조를 타 컴포넌트 테스트에 고정해 연쇄 수정을 유발하는지 살피되, 실제 호환성·트랜잭션·사용자 흐름에 필요한 경계 검증은 제거하지 않는다. 가장 싼 충분한 수준을 택하며 테스트 피라미드나 고정된 테스트 배합을 강제하지 않는다.
5. **Check reliability and cost** — fixture와 상태 격리, mocking의 충실도, 시간·순서·병렬성·외부 환경으로 인한 flakiness, 중복, 진단 용이성과 유지보수 비용을 함께 판단한다. 작업자가 관련 결과를 관찰하고 실패 조건을 통제·재현할 수 있는지, 공유 상태·fixture나 다른 소유자의 내부 변경 때문에 불필요하게 실패·공동 수정되는지도 본다. 관찰·제어가 불가능하면 필요한 최소 테스트 가능성 개선이나 소유자 결정을 제안하되 아키텍처를 임의로 바꾸지 않는다. Mock 자체를 금지하지 않고, 보호할 실제 상호작용을 가리는지를 본다.

## Stronger Evidence When It Pays

- 테스트가 실패하거나 기대값·기준 구현이 의심스러우면 제품 결함, 테스트·oracle 결함, fixture·runner·환경 결함을 구분한 뒤 수정 대상을 결정한다. 필요하면 [Oracle validation](references/oracle-validation.md)을 읽는다. 단순하고 근거가 확실한 사례에는 추가로 로드하지 않는다.
- 버그 수정이라면 가능한 경우 **수정 전 의도한 이유의 실패 → 수정 후 성공 → 관련 기존 동작 보존**을 검증한다. 테스트 통과만으로 요청된 기능 전체나 산출물의 완성을 선언하지 않는다.
- 일반 불변식이 명확하면 property-based 또는 metamorphic test를, 신뢰 가능한 비교 대상이 있으면 differential test를, 중요한 결함이 기존 테스트를 통과할 위험이 크면 작은 mutation/fault-injection 실험을 고려한다.
- 강한 검증 기법도 oracle 자체를 정당화하지 못한다. 고위험·불확실성을 줄이는 가치가 실행·유지 비용보다 클 때만 추가한다.
- 독립 근거가 중요하지만 별도 에이전트, strict TDD 순서, 도구 설치나 전체 suite 실행은 보편적인 전제 조건이 아니다.

## Evidence and Handoff

설계 판단과 **실제로 실행·관찰한 결과**를 구분한다. 실행 가능하고 현재 작업에 포함되면 프로젝트의 기존 도구·실행 경로로 확인하되, 직접 실행할 수 없으면 검증 가능한 테스트 시나리오·oracle·실행 방법과 미확인 사항을 제공한다. 정적 검토나 가정한 결과를 PASS로 표현하지 않는다.

결과는 규모에 비례해 제시한다. 핵심 계약, 우선할 테스트/관찰값, 필요한 test boundary, 기존 evidence와 남은 gap을 명확히 하되 단순한 요청에 보고서나 테이블을 강제하지 않는다.

## Boundary

이 Skill은 **software test selection, oracle, design sufficiency and quality**에 대한 판단을 소유한다. 일반적인 코드 구현·디버깅, 모듈 아키텍처 자체의 재설계, test runner 운영, CI trigger·merge admission, 에이전트/LLM의 routing·behavior evaluation 체계, 저장소별 정책은 소유하지 않는다. 해당 업무에서는 적용되는 프로젝트·도구·전문 owner를 우선하며, 이 Skill은 테스트 설계가 실질적인 하위 문제일 때만 보조한다. 다른 Skill, vendor, 언어, 프레임워크 또는 저장소 파일에 의존하지 않는다.
