# Semantic Validation

의미론적 검증은 **의도한 설계와 행동 계약이 현재 instruction과 구조에 제대로 표현되어 있는지** 판정한다.

## Establish the contract

검증 전에 무엇을 준수해야 하는지 먼저 식별한다. 사용자·프로젝트 요구, canonical design, source/target contract, accepted owner가 기준이 될 수 있다. 현재 자산의 문구만 다시 읽고 스스로를 기준으로 삼는 순환 검증은 피한다.

기준의 일부를 구조에서 추론해야 하면 그 부분은 `inferred`로 남기고 명시된 계약처럼 다루지 않는다.

## Validate

필요한 범위에서 다음을 본다.

- responsibility와 decision owner가 의도와 일치하는가
- activation, applicability, scope와 negative boundary가 intended use를 표현하는가
- source, target, repository, asset authority가 섞이지 않았는가
- required behavior, prohibited behavior, exception, failure와 completion condition이 충분히 표현됐는가
- delegation, capability, handoff, result contract가 설계된 책임 경계를 보존하는가
- reusable core와 local/target delta가 의도한 portability를 유지하는가
- 중요한 safety·permission boundary가 optional routing이나 암묵적 관행에 숨어 있지 않은가

## Boundary

Semantic Validation은 설계가 얼마나 좋은지 자유롭게 탐색하는 Review가 아니다. 계약 자체가 잘못됐거나 더 나은 설계가 필요해 보이면 그 문제는 Review finding으로 분리한다.

또한 계약이 잘 표현됐다는 사실만으로 실제 runtime에서 높은 성공률로 작동한다고 주장하지 않는다. 실제 선택·호출은 Routing Eval, 선택 이후 행동과 결과는 Behavior Eval이 소유한다.
