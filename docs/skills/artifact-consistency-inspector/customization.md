# Customization Guide

이 문서는 `artifact-consistency-inspector`의 maintainer-only customization contract다.
Runtime package의 일부가 아니며 Skill 실행이 이 문서에 의존해서는 안 된다.

## Safe to change

- Skill `name`과 `description`
- README wording과 invocation examples
- report title과 description wording
- `author` value 또는 placeholder policy
- default language
- output filename prefix와 target abbreviation
- auto loop upper bounds
- report section headings
- ZIP usage conditions
- optional report front matter fields
- scenario inventory와 test-report wording

External ZIP과 report filename은 자유롭게 변경할 수 있다. Download-folder collision과
cache ambiguity가 중요하면 timestamp suffix를 유지한다.

## Rule-source customization

- `rule_sources`는 repository-specific locator나 selector를 사용할 수 있다.
- 사용자가 지정한 list order는 해당 run의 authority다.
- Auto-discovery signal은 domain에 맞게 확장할 수 있지만 하나의 universal source-type precedence를 hard-code하지 않는다.
- source selector를 rename하면 `SKILL.md`, `references/rule-sources.md`, examples와 tests를 함께 갱신한다.

## Preserve

- Skill root `SKILL.md`
- read-only repository access
- repository 또는 repository-host state mutation 금지
- fixed project layout 또는 directory assumption 금지
- compact `Observed difference / References / Potential impact` finding structure
- unresolved finding에만 `Why unresolved`
- inspection workflow 안의 adversarial counterevidence check
- bounded absence 없이 verified omission을 주장하지 않음
- revision을 silent하게 섞지 않음
- rule source가 충돌할 때 authority를 silent하게 선택하지 않음
- `verified`와 `unresolved` 구분
- `no-verified-findings`를 overall consistency guarantee로 확대하지 않음
- downloadable Markdown 또는 필요한 ZIP delivery

## Rename behavior

- external ZIP: 자유롭게 rename 가능
- internal root folder: package references와 tests를 함께 갱신하면 rename 가능
- `README.md`, `references/*.md`: `SKILL.md`의 relative reference를 함께 갱신하면 rename 가능
- `SKILL.md`: filename과 Skill root 위치를 보존
- report output: rename 가능; timestamp suffix는 권장

## Front matter changes

Field를 추가할 수 있지만 다음을 지킨다.

- free-text value는 quote한다.
- machine field는 body state와 일치한다.
- secret과 temporary internal path는 제외한다.
- samples, tests, README와 report-format rule을 함께 갱신한다.
