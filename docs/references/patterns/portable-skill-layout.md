# Portable Skill Layout

일반 project repository에서 Skill을 **portable하고 tuning하기 쉬운 source workspace**로 관리하는 패턴입니다.

## Layout

```text
<skill>/
├─ SKILL.md
├─ references/
├─ scripts/
├─ assets/
├─ README.md
├─ .docs/
├─ .tests/
└─ .eval/
```

## Boundary

- `SKILL.md`, `references/`, `scripts/`, `assets/` → runtime에 필요한 surface
- `README.md`, `.docs/`, `.tests/`, `.eval/` → runtime과 무관한 development / maintenance / evaluation surface
- Dot-prefixed maintainer surface가 없으면 Skill runtime behavior가 달라져서는 안 됩니다.

## README

`README.md`는 최소 entrypoint로만 사용합니다.

```md
# <skill-name>

- Runtime → `SKILL.md`
- Maintainer docs → `.docs/`
- Tests → `.tests/`
- Evals → `.eval/`
```

세부 규칙이나 설계 내용을 README에 복제하지 않습니다.

## Why

Skill directory 전체를 복사하면 runtime source뿐 아니라 유지보수·검증·평가 context도 함께 이동합니다. 그래서 일반 application/project repository에서 Skill을 독립적으로 개발하고 project별로 tuning하기 쉽습니다.

반대로 repository 자체가 많은 Agent Asset을 중앙 관리하는 경우에는 docs/tests/evals를 repository-level surface로 분리하는 편이 더 적합할 수 있습니다.

Dot-prefix는 packaging exclusion을 자동 보장하지 않습니다. 배포 시 maintainer-only surface를 제외하는 책임은 사용하는 tool이나 packaging workflow가 가져야 합니다.
