# Adoption

Tach를 처음 도입하거나 architecture baseline을 세우고, source-root/module modeling 또는 incremental adoption을 다룰 때만 읽는다.

## Establish the Model

- Architecture rule을 만들기 전에 source-root resolution과 module boundary가 실제 Python import model을 올바르게 표현하는지 확인한다.
- 현재 import graph는 initial evidence나 migration seed로 사용할 수 있지만 intended architecture 자체로 고정하지 않는다.
- `tach sync`처럼 현재 imports에서 dependency configuration을 제안·갱신하는 결과는 bootstrap aid다. 생성된 관계를 각각 검토하고 code가 이미 사용한다는 이유만으로 허용하지 않는다.
- Existing violation은 intended architecture의 증거가 아니다. Core contract에 따라 implementation violation, modeling/configuration error, intended contract change, unclear intent로 분류한다.

## Stage Enforcement

- 처음부터 모든 현재 관계를 허용해 green baseline을 만드는 것보다, 의도와 근거가 명확한 boundary부터 contract로 고정한다.
- Incremental adoption이 필요하면 unchecked, exclude, ignore 또는 다른 relaxation을 사용할 수 있지만, 의도적으로 좁은 범위와 명확한 이유를 유지한다.
- 아직 enforcement 밖에 있는 relationship을 checked된 것으로 취급하지 않는다. Coverage 확대는 별도 architecture change로 판단한다.
- Baseline 정리 과정에서 unrelated architecture debt를 함께 고치지 않는다.

## Validate

- Source-root나 module modeling을 바꿨다면 새 violation을 architecture 문제로 해석하기 전에 model이 의도한 imports를 관찰하는지 다시 확인한다.
- Passing validation은 현재 checked scope만 증명한다. Incremental adoption에서 남겨 둔 unchecked/excluded/ignored scope를 숨기지 않는다.
- External package dependency declaration까지 adoption scope에 포함된다면 architecture boundary validation과 별도 evidence로 검증할 필요가 있는지 판단한다.

## Boundary

설치 절차, command option, configuration schema의 full reference는 이 문서가 소유하지 않는다. Version-sensitive detail이 결정에 필요할 때 현재 authoritative Tach source를 확인한다.
