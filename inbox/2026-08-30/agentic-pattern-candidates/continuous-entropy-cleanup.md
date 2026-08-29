# Continuous Entropy Cleanup

Status: **exploratory candidate**

## Idea

Repository에서 반복적으로 증식하는 작은 drift나 low-grade inconsistency가 있다면, 큰 정리 작업까지 방치하기보다 **작고 반복 가능한 cleanup으로 확산 비용을 낮추는 방식**을 고려할 수 있습니다.

이 후보의 핵심은 cleanup automation 자체가 아니라, 새로운 작업이 기존의 좋지 않은 pattern을 복제하면서 debt가 compounding되는 문제를 다루는 것입니다.

## Typical Signals

- 비슷한 helper나 workaround가 계속 새로 생깁니다.
- deprecated pattern이 새로운 code에서도 반복됩니다.
- 같은 naming, validation, dependency 문제를 review에서 계속 지적합니다.
- cleanup을 미룰수록 future change가 더 많은 legacy shape를 따라가야 합니다.
- agent나 generator가 repository의 existing example을 그대로 복제하면서 좋지 않은 pattern을 빠르게 증폭합니다.

## Possible Responses

문제가 반복된다면 다음을 비교할 수 있습니다.

- 가장 먼저 exemplar와 canonical path를 고쳐 future copy target을 개선합니다.
- 객관적인 invariant라면 lint나 structural check로 전환할 수 있는지 봅니다.
- 작은 mechanical cleanup을 normal change와 함께 처리해도 review noise가 낮은지 봅니다.
- recurring scan이나 automated refactor가 실제 maintenance cost를 낮추는 영역인지 확인합니다.
- debt inventory가 필요하다면 실제 action으로 이어지는 최소한의 tracker만 유지합니다.

## Avoiding Cleanup Theater

정리 activity 자체를 목표로 삼지 않습니다.

- 단순 formatting이나 cosmetic uniformity만 위해 architecture를 흔들지 않습니다.
- 실제 change cost를 줄이지 않는 일관성 작업은 우선순위를 낮춥니다.
- cleanup job을 만들기 위해 새로운 rule과 dashboard를 계속 추가하지 않습니다.
- 자동화가 false positive와 review burden을 더 크게 만들면 단순한 opportunistic cleanup이 나을 수 있습니다.

## Limits

- 어떤 inconsistency는 실제로 local variation이 필요한 결과일 수 있습니다.
- active migration 중에는 temporary duplication이나 mixed pattern이 자연스러울 수 있습니다.
- cleanup frequency가 높다고 debt가 낮아지는 것은 아닙니다. root cause가 architecture나 ownership에 있다면 별도 개선이 필요합니다.
- agent-generated repository 사례에서 특히 잘 보이는 현상을 모든 repository의 기본 운영 규칙으로 일반화하면 안 됩니다.

## Relationship to Other Candidates

반복 drift의 원인이 stable invariant 위반이라면 `Executable Architecture Invariants`가 더 직접적인 대응일 수 있습니다. 이 후보는 invariant로 만들기 어려운 broader entropy와 gradual cleanup cadence를 다루는 쪽에 가깝습니다.

`Self-Contained Change`와도 연결될 수 있지만, cleanup을 항상 별도 PR로 분리해야 한다는 규칙을 만들지는 않습니다.

## Promotion Questions

- 이 내용이 단순한 `boy scout rule`, tech-debt management 또는 housekeeping의 재서술에 그치지 않는가?
- agentic coding의 높은 replication speed가 독립 pattern을 정당화할 만큼 중요한 차이를 만드는가?
- recurring automation을 권장하지 않으면서도 실용적인 core를 설명할 수 있는가?
- `Executable Architecture Invariants`에 흡수하는 편이 더 단순하지 않은가?

## Research Notes

- OpenAI의 agent-first repository 사례는 agents가 repository의 기존 pattern을 복제해 suboptimal pattern까지 빠르게 증식시키는 문제를 설명하고, small recurring cleanup과 mechanical golden principles를 일종의 garbage collection처럼 운영한 사례를 공유합니다.
