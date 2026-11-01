# Chatbot Bootstrap — Harness Fidelity Findings

## 결론

`mols-chatbot-bootstrap` 개선의 핵심은 라우터 파일을 추가하거나 사전에 자산을 전부 읽게 하는 것이 아니다. **챗봇이 작업에 적용되는 지침과 자산을 선택적으로 발견하고, 선택한 canonical source를 실제로 로드하여 작업에 적용할 수 있는 호환 경로**를 구성하는 것이다.

**목표 확장:** 이것은 최소 요구사항이며, 최종적으로는 **현재 런타임에서 원본 하네스의 정확성·권한 경계를 보존하면서 운영·컨텍스트·도구 비용이 작은 유효한 하네스 구조를 선택·구축**하는 것이 목표다. 단순 연결 성공과 환경별 최적 설계는 다르다. 자세한 설계 후보와 비교 기준은 [architecture options](harness-architecture-options.md)를 따른다.

이 문서는 실행 원본을 복제하지 않는 작업용 판단 기록이다. 실제 Skill 계약은 [SKILL.md](../../src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/SKILL.md)가 소유한다.

## 문제 정의

- 호환성 진입점(`CHATBOT.md` 등)을 읽었다는 사실은 해당 작업에 적용되는 `AGENTS.md`·Rule·Skill을 모두 고려했다는 뜻이 아니다.
- 라우팅 메타데이터(`name`, `description`, `source`)를 확인한 것과 선택한 `SKILL.md`의 **본문을 읽어 적용한 것**은 별개의 단계다.
- 접근 가능한 링크·정적 인덱스의 존재만으로 실행 시 하네스 준수를 검증했다고 판단할 수 없다.
- 실제로 어느 단계가 실패하는지는 대상 챗봇의 호출·로딩·작업 결과로 확인해야 한다. 현재 이 문서는 정적 계약 검토에 근거하며 런타임 재현을 주장하지 않는다.

## 유지할 설계 결정

1. **범용성:** 이 저장소의 디렉터리 구성이나 `route/`와 `.agents/route/`의 구분을 다른 프로젝트의 필수 규칙으로 일반화하지 않는다. 대상의 하네스가 정본이다.
2. **Native first / no-op:** 런타임이 이미 충분한 discovery·loading을 제공한다면 추가 호환 계층을 설치하지 않는다. 부분적 네이티브 지원도 허용한다.
3. **선택적·지연 로딩:** 기본적으로 최소 진입점 및 관련 라우팅 메타데이터만 확인하고, 현재 작업에 관련된 자산의 canonical body만 로드한다. 선택되지 않은 Skill, Rule, Subagent 및 references를 선로드하지 않는다.
4. **선택과 로딩 분리:** route에서 자산을 선택한 뒤 그 source를 읽어야 한다. reference는 해당 Skill 계약이나 현재 작업이 요구할 때만 추가 로드한다.
5. **범위 변경 시 재평가:** 작업 의도, 경로, ref, 대상이 실질적으로 바뀌면 관련 지침과 자산을 다시 선택한다. 변화가 없다면 같은 리비전의 이미 유효하게 로드된 자산을 재사용한다.
6. **저빈도 부트스트랩:** 이 Skill은 일회성·저빈도 호환성 provision/repair 책임을 맡는다. 매 작업의 상시 실행 관리자나 새로운 policy owner가 아니다.
7. **부족한 기능만 대체:** 필수 도구·권한·독립 에이전트 실행이 없는 런타임에서는 가능한 범위와 동등하지 않은 부분을 구분한다. 권한 확대나 미수행 행동의 완료 선언을 금지한다.

## 추가 설계 Findings

- **설계 선택 부재:** 기존 Skill은 '최소한의 호환 경로'를 권장하지만 **네이티브만으로 충분한 경우**, 포인터만 필요한 경우, 선택적 라우팅이 필요한 경우 중 어느 구성이 가장 낮은 비용으로 실제 결과를 내는지 비교·판정하는 지침은 제한적이다.
- **비용 기준 부재:** 정확성·안전만 확보해도 매 요청에 전체 asset catalog를 재검색하거나 많은 Skill 본문을 선로딩하면 실무적인 최적 하네스라고 부를 수 없다. 실제 비용/품질 비교는 아직 실측되지 않았다.
- **Capability와 권한 혼동 위험:** 동일 제품에서도 Chat/Agent/Desktop/API와 account·connector가 달라 runtime 정보만으로는 실행 가능성·authorization을 결정할 수 없다.
- **Skill scope 결정 보류:** 현 bootstrap Skill이 경량 설계 기능까지 소유할지, 독립적으로 사용되는 harness design capability가 별도 Skill을 필요로 하는지는 실제 activation/near-miss와 유지보수 비용을 보고 결정한다.
- **검증 계획:** [평가 전략](harness-evaluation-strategy.md)의 design validity, fidelity, safety, cost, UX를 함께 평가한다. 테스트 전에는 최적성·parity를 `verified`로 부르지 않는다.

## 작업 시 기대하는 연결

```text
runtime의 실제 first-hop
  → 대상 repository의 entrypoint / 적용 지침
  → 작업·경로에 맞는 최소 routing metadata
  → 필요한 자산 선택
  → 선택한 canonical Skill / Rule / Subagent body 로드
  → 해당 작업에 필요한 reference만 추가 로드
  → 계약을 적용해 수행
  → 작업 범위가 실질적으로 바뀌었을 때만 적용 자산 재평가
```

`source` URL을 파악하거나 반환한 것만으로 canonical loading이 끝난 것으로 간주하지 않는다. 반대로 이 흐름을 이유로 전체 목록이나 본문을 일괄 로드하지도 않는다.

## 검증 관점

- **Routing:** 필요 자산을 선택했는가? 관련 없는 자산은 로드하지 않았는가?
- **Loading:** 선택한 자산의 실제 source를 열었는가? 필요한 reference까지 읽었는가?
- **Application:** 해당 계약이 후속 tool/action/output에 반영됐는가?
- **Failure visibility:** 필수 자산을 열지 못했거나 runtime first-hop을 확인할 수 없다면 검증·완료 범위를 정직하게 구분하는가?
- **Efficiency:** 사전 전체 로딩, 불필요한 반복 fetch, 매 tool call 전 재라우팅, 새 generator/CI 강제 도입이 없는가?

이 지표는 **실제 런타임 관찰이 있을 때만** 동작 검증 근거가 된다. 정적 검토로 routing precision이나 실행 성공을 단정하지 않는다.

## 검토에서 제외할 과잉 일반화

- 특정 저장소의 라우팅 파일명·소유권을 범용 필수 계약으로 승격
- 모든 route의 Git ref를 무조건 동일하게 맞추도록 요구
- 전체 Skill/Rule/Reference를 upfront 로드해야 하네스를 준수한다고 해석
- bootstrap Skill 자체를 평상시 작업마다 반드시 호출하도록 설계
- 파일 생성·파서·CI·테스트 수를 늘리는 것을 하네스 충실도 향상과 동일시

## 관련 사항

- 부속 baseline generator의 메타데이터 파싱 실패 시 일부 Skill을 조용히 제외할 가능성은 별도의 구현 품질 이슈이며, 이번 **하네스 준수** 개선의 선행 조건이 아니다.
- [유지보수 범용성 문서 PR #266](https://github.com/mols3131d/mols-agent-assets/pull/266)는 별도 작업이다. 아직 병합되지 않았다면 내용을 이 PR에 기계적으로 복제하거나 종속시키지 않는다.
