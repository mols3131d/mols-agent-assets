# Self-Contained Change

Status: **strong candidate**

## Idea

Change의 크기를 line count나 file count보다 **하나의 독립적으로 이해·검증·통합 가능한 변화인지**를 중심으로 판단하는 것을 고려합니다.

작은 change 자체가 목적은 아닙니다. Change가 너무 크면 reasoning, review, rollback과 conflict cost가 커지고, 반대로 지나치게 잘게 쪼개면 의미를 이해하기 어렵거나 중간 상태가 불완전해질 수 있습니다.

## Core Question

> 이 change 하나만 보아도 무엇을 왜 바꾸는지 이해할 수 있고, 관련 검증을 수행한 뒤 repository에 안전하게 통합할 수 있는가?

## Typical Characteristics

Self-contained한 change는 상황에 따라 다음 성질을 가질 수 있습니다.

- 하나의 설명 가능한 목적이나 behavior change를 중심으로 합니다.
- 필요한 production code와 직접 관련된 test를 함께 포함합니다.
- 중간 merge state가 build, runtime 또는 user experience를 불필요하게 깨뜨리지 않습니다.
- reviewer가 미래 change를 미리 알아야만 현재 change를 이해할 필요가 없습니다.
- 잘못된 경우 독립 rollback이 비교적 이해하기 쉽습니다.

## Splitting Signals

다음은 change를 나눌지 다시 볼 신호가 될 수 있습니다.

- feature change와 큰 structural refactoring이 함께 섞여 review 의도가 흐려집니다.
- 서로 다른 failure mode와 verification path를 가진 변화가 한 PR에 묶여 있습니다.
- 한 부분을 review하려면 아직 구현되지 않은 다음 change를 가정해야 합니다.
- rollback 시 unrelated change까지 함께 되돌려야 합니다.
- diff가 크다는 사실보다 reviewer나 agent가 하나의 coherent mental model을 유지하기 어렵습니다.

## When Not to Split

다음처럼 함께 있어야 의미가 분명한 경우에는 억지로 분리하지 않을 수 있습니다.

- 새 API와 최소 사용 예가 함께 있어야 design intent를 평가할 수 있습니다.
- schema change와 그 schema를 소비하는 최소한의 compatibility change가 함께 있어야 repository가 작동합니다.
- 분리하면 각 intermediate change가 dead code나 invalid state를 만듭니다.
- 서로 강하게 결합된 production behavior와 test를 떼면 verification이 약해집니다.

## Possible Responses

- behavior change 전에 독립 refactoring이 필요하다면 먼저 structural change만 분리할 수 있습니다.
- 큰 feature는 end-to-end로 의미가 유지되는 vertical slice로 나눌 수 있는지 봅니다.
- dependency가 있는 여러 change는 stack할 수 있지만 각 단계가 이해 가능한 상태인지 확인합니다.
- split 자체가 더 큰 temporary complexity를 만든다면 하나의 coherent change를 유지하는 편이 나을 수 있습니다.

## Limits

- migration, generated code update, large mechanical rename처럼 본질적으로 큰 diff가 생기는 작업이 있습니다.
- line count는 review cost의 대략적인 신호일 수 있지만 conceptual size와 일치하지 않습니다.
- 너무 작은 change를 강제하면 coordination overhead와 integration overhead가 늘 수 있습니다.
- agent throughput이 높다는 이유만으로 merge gate를 약하게 하는 문제는 별도의 repository workflow 판단입니다.

## Relationship to Existing Patterns

이 후보는 code/module structure보다 **change boundary**를 다루므로 `workflow/`가 더 자연스러운 primary owner일 가능성이 있습니다. 다만 change decomposition은 software design과 강하게 연결되므로 category를 승격 전에 다시 검토합니다.

## Promotion Questions

- Google의 Small CL guidance를 단순 요약하는 수준을 넘어 reusable pattern으로 재구성할 수 있는가?
- `small PR`이 아니라 `coherent change boundary`라는 core가 충분히 독립적인가?
- agentic workflow에서 높은 throughput과 correction cost 변화가 이 pattern을 어떻게 수정하는지 별도 조사해야 하는가?

## Research Notes

- Google Engineering Practices는 적절한 CL 크기를 line count보다 one self-contained change로 설명하고, related test와 working intermediate state를 강조합니다.
- 최신 agent harness 사례도 긴 작업을 smaller work unit으로 분해하는 이점과, model capability가 올라가면 불필요한 harness decomposition을 다시 줄여야 한다는 점을 함께 보여줍니다.
