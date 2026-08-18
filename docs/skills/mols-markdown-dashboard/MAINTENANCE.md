# Maintenance

## Change Protocol

1. `baseline/DIRECTIVE.md`를 읽고 관련 Requirement와 Decision ID를 식별한다.
1. 변경이 기존 directive의 본래 목적·요구사항·결정사항을 바꾸면 코드보다 baseline directive를 먼저 수정한다.
1. Example YAML, rendered Markdown와 tests를 함께 수정한다.
1. Project와 domain 예제를 모두 렌더링한다.
1. 3개 핵심 표의 열과 의미가 유지되는지 확인한다.
1. 통합 품질 게이트를 실행한다.
1. 변경 후 `REVIEW-LOOPS.md` 또는 별도 review artifact에 판단을 남긴다.

이 디렉터리와 `baseline/`은 source maintenance/recovery용 non-runtime surface다. Runtime 동작이 이 문서를 읽어야만 정상 작동하도록 만들지 않는다.

## Quality Gate

Skill 구현 루트 `.agentsmesh/skills/mols-markdown-dashboard/`에서 실행한다.

```bash
uv sync --all-groups
uv run python scripts/check_quality.py
```

통합 스크립트는 다음을 순서대로 실행한다.

```text
ruff check
→ ruff format --check
→ ty check
→ rumdl check
→ compileall
→ pytest
→ example YAML/Markdown drift check
```

하나라도 실행할 수 없거나 실패하면 release를 통과로 기록하지 않는다.

## Render Examples

Skill 구현 루트에서 실행한다.

```bash
uv run python scripts/render_dashboard.py render \
  examples/project-dashboard.yml \
  -o examples/project-dashboard.md

uv run python scripts/render_dashboard.py render \
  examples/domain-dashboard.yml \
  -o examples/domain-dashboard.md
```

## Recovery Checklist

스킬이 후속 에이전트 수정으로 훼손됐을 때 `baseline/DIRECTIVE.md`와 다음 항목을 대조한다.

| Check | Expected |
| --- | --- |
| Project row unit | Domain |
| Domain row unit | Capability |
| Main columns | Implementation status/progress, Verification status/progress |
| Gap rows | 한 gap당 한 행, item별 번호 재시작 |
| YAML status | Emoji 없는 stable code |
| Rendered status | Emoji + English label |
| Progress aggregation | Numerator와 denominator 합산 |
| Core renderer | PyYAML + dataclasses/StrEnum + Jinja2 |
| Markdown check | pyromark parser 호출 |
| Unknown fields | 경로와 함께 즉시 실패 |
| Output write | Atomic replace |
| Example integrity | YAML 재렌더 결과와 Markdown 일치 |
| Default visuals | Core tables only; charts conditional |

## Refactoring Rules

- Public YAML schema를 바꿀 때 schema version을 올린다.
- Formatting 변경을 semantic 변경과 같은 commit에서 섞지 않는다.
- Helper를 지나치게 일반화하지 않는다.
- `dict[str, Any]`는 loader boundary에만 두고 내부에는 dataclass를 사용한다.
- Optional dependency fallback으로 validation을 조용히 건너뛰지 않는다.
- 오류에는 가능한 한 YAML field path를 포함한다.
- 외부 품질 도구가 실행되지 않았으면 문서에 그 사실을 보존한다.
