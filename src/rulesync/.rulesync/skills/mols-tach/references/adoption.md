# Adoption

Tach를 처음 도입하거나 baseline과 incremental adoption을 설계할 때만 읽는다.

## Establish the Baseline

- 현재 import graph는 initial evidence나 migration seed로 사용할 수 있지만 intended architecture 자체로 고정하지 않는다.
- `tach sync`처럼 현재 imports에서 dependency configuration을 제안·갱신하는 결과는 bootstrap aid다. 생성된 관계는 각각 검토하고 code가 이미 사용한다는 이유만으로 허용하지 않는다.
- Existing violation은 intended architecture의 증거가 아니다. Core contract의 mismatch classification으로 먼저 판단한다.

## Stage Enforcement

- 모든 현재 관계를 허용해 green baseline을 만드는 것보다 의도와 근거가 명확한 boundary부터 contract로 고정한다.
- Incremental adoption에 unchecked, exclude, ignore 또는 다른 relaxation이 필요하면 범위와 이유를 명확히 제한한다.
- Enforcement 밖에 남겨 둔 relationship은 checked된 것으로 취급하지 않는다. Coverage 확대는 별도 architecture change로 판단한다.

## Validate

- Adoption 과정에서 source-root나 module modeling을 바꿨다면 새 violation을 architecture 문제로 해석하기 전에 의도한 imports가 관찰되는지 다시 확인한다.
- External package dependency declaration까지 adoption scope에 포함되면 별도 validation evidence가 필요한지 판단한다.

## Boundary

설치 절차, command option과 configuration schema의 full reference는 소유하지 않는다. Version-sensitive detail이 결정에 필요하면 현재 authoritative Tach source를 확인한다.
