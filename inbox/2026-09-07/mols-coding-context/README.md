# `mols-coding-context` 설계 번들

이 번들은 coding context를 **core + language add-on** 구조로 설계하기 위한 조사·설계 자료다.

## 결론

```text
code-facing task
→ mols-coding-context

Python semantics가 material
→ mols-coding-context
 + mols-coding-context-python
```

- `mols-coding-context`는 main/core다.
- `mols-coding-context-python`은 Python add-on이다.
- Add-on은 core를 대체하지 않고 language-specific delta만 추가한다.
- Add-on은 해당 언어가 repository에 존재한다는 이유가 아니라 **현재 active work에 그 언어의 semantics가 material한지**로 선택한다.
- 다른 Skill family와 직접 dependency/reference를 만들지 않는다.

이 구조는 향후 다른 언어가 필요해질 때 같은 모양으로 확장할 수 있다.

```text
mols-coding-context
mols-coding-context-python
mols-coding-context-<language>   # evidence가 생긴 경우에만
```

언어별 add-on을 미리 만들지는 않는다.

## 설계 원칙

- **Core first** — generic engineering judgment는 core가 한 번만 소유한다.
- **Delta only** — language add-on은 core 내용을 반복하지 않는다.
- **Frontmatter first** — Skill 선택 전에 필요한 applicability와 near-miss는 canonical `SKILL.md` frontmatter가 소유한다.
- **Materiality** — Skill 선택과 개별 rule 적용 모두 현재 task에 material한지 본다.
- **KISS / DRY** — router, dependency chain, duplicated guidance를 만들지 않는다.
- **Deterministic owner first** — formatter, linter, type checker, tests, SAST가 안정적으로 판정할 수 있는 항목을 prose로 복제하지 않는다.

## 문서 책임

| 문서 | 책임 |
| --- | --- |
| [research.md](research.md) | repository와 외부 evidence |
| [design.md](design.md) | core/add-on architecture와 ownership |
| [migration.md](migration.md) | 기존 `coding-context` 교체 계획 |
| [evaluation.md](evaluation.md) | routing/behavior 검증 기준 |

정확한 Skill frontmatter와 실행 instruction의 canonical owner는 다음 두 파일이다.

- `src/rulesync/.rulesync/skills/mols-coding-context/SKILL.md`
- `src/rulesync/.rulesync/skills/mols-coding-context-python/SKILL.md`

Inbox 문서는 이를 복제하지 않고 설계 이유와 migration/evaluation 근거만 소유한다.

## Scope

이번 작업에서 직접 다루는 것은 다음뿐이다.

- `coding-context`의 후속 core인 `mols-coding-context`
- Python-specific add-on인 `mols-coding-context-python`
- 두 Skill의 routing/behavior evaluation과 migration 근거

기존 `mols-clarify-code`, `mols-code-comprehension-refactor`, `mols-clarify-runtime`과 다른 Skill family는 유지한다.

## Migration 방향

```text
coding-context
→ mols-coding-context

Python-material task
→ + mols-coding-context-python
```

기존 `coding-context`는 신규 core가 routing/behavior gate를 통과한 뒤에만 삭제한다.
