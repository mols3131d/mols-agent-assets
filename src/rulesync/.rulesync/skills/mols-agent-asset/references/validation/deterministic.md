# Deterministic Validation

결정론적 검증은 같은 입력에 대해 안정적으로 같은 판정을 낼 수 있는 계약을 검사한다.

## Validate

대표 대상은 다음과 같다.

- schema, frontmatter, required field와 allowed value
- 필수 파일, path, reference 존재 여부와 package integrity
- parser, compiler, formatter, framework validator의 성공·실패
- selector, glob, config처럼 syntax와 구조가 명시적으로 정의된 값
- canonical source에서 생성한 projection과 committed/generated result의 drift
- deterministic script의 exit code, output contract, 금지된 mutation

## Mechanism

가장 authoritative하고 좁은 기존 mechanism을 우선한다. Source framework validator가 충분하면 같은 규칙을 별도 script나 test에 복제하지 않는다.

새 executable check는 반복해서 필요하고, failure 비용이 의미 있으며, observable output만으로 값싸고 안정적으로 판정할 수 있을 때만 추가한다. 사람이 의미를 해석해야 하는 성질을 억지 문자열 검사로 고정하지 않는다.

## Result

- 판정 가능한 check는 `pass` 또는 `fail`로 기록한다.
- 필요한 executable capability가 없으면 `not_run`으로 남긴다.
- 규격의 source가 불명확하면 임의의 schema를 만들지 않고 `unknown`으로 남긴다.
- 결정론적 검증의 성공은 설계 적합성이나 실제 behavior 성능을 증명하지 않는다.
