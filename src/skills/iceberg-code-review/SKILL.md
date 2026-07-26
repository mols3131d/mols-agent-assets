---
name: iceberg-code-review
description: >
  Write Iceberg-style structured code-review reports. Focuses on report format, templates, generation, and validation. Provides built-in review engines that may be changed or replaced when user requirements or model judgment call for it. Does not apply code fixes.
---

# Iceberg Code Review

> [!NOTE]
> 코드 리뷰 결과를 핵심부터 세부 내용까지 단계적으로 보여주는 아이스버그형 보고서 포맷을 제공합니다. 템플릿 기반 문서 생성과 프론트 매터·섹션 구조 검증을 지원하며, 리뷰 엔진은 필요에 따라 교체할 수 있습니다.

## Workflow

```mermaid
flowchart LR
    A[SKILL.md] --> B[Engine selection]
    B --> C[Create details report]
    C --> D[Create summary report]
    D --> E[Validate summary report]
    E --> F[Completion]
```

### Engine selection

- Engine specified → use it.
- Otherwise:
  - Apply relevant other skill/instructions when appropriate.
  - If none -> [matching built-in engine](references/engine-router.md).
- New review area found mid-review → no engine addition. Recommend follow-up in report.

### Create details report

> One review result → one validated detail. Finish before next.

1. Review target with selected engine or skill. Run relevant tests. Keep `PASS`, `FAIL`, `ERROR`, `SKIP` counts.
2. Set `domain` and `detail` slugs: lowercase letters, digits, hyphens.
3. Create detail in `<review_dir>`:

    ```bash
    <PYTHON_EXEC> "<SKILL_DIR>/scripts/create_detail.py" --review-dir "<review_dir>" --domain "<domain>" --detail "<detail>"
    ```

4. Fill verified issue, location, impact, recommendation, verification. Remove template comments and instructions.
5. Validate:

    ```bash
    <PYTHON_EXEC> "<SKILL_DIR>/scripts/validate_detail.py" "<detail_file_path>"
    ```

6. `FAIL: ...` → fix, rerun. Pass → next review result.
7. On the sixth validated detail in a review pass, stop and follow [overtime work](references/workflow-overtime-work.md). Do not begin another review area unless the commander explicitly asks to continue.

### Create summary report

> create `__summary__.md`

1. Create in `<review_dir>`:

    ```bash
    <PYTHON_EXEC> "<SKILL_DIR>/scripts/create_summary.py" --review-dir "<review_dir>"
    ```

2. Read all validated details, if any. Fill reviewed scope, links, and test counts. When no details exist, state that the reviewed scope is clean. Remove template comments and instructions.
3. Validate:

    ```bash
    <PYTHON_EXEC> "<SKILL_DIR>/scripts/validate_summary.py" "<summary_file_path>"
    ```

4. `FAIL: ...` → fix, rerun. Pass → finish.

## Priority

| Emoji | Priority | Description                                                        |
| :---: | :------- | :----------------------------------------------------------------- |
|  🔴   | `p0`     | 즉시 확인 또는 조치해야 함. 진행을 막거나 중대한 영향을 줄 수 있음 |
|  🟠   | `p1`     | 높은 우선순위로 현재 작업 범위에서 처리해야 함                     |
|  🟡   | `p2`     | 일반 우선순위. 계획된 검토·수정 과정에서 처리함                    |
|  🟢   | `p3`     | 낮은 우선순위. 후속 작업이나 여유가 있을 때 처리함                 |
|  🔵   | `p4`     | 참고 목적. 별도 조치 없이 기록을 유지함                            |

When multiple engines, keep higher (`p3 & p1` -> `p1`)

## Suggestions

| Agent Skill | Trigger: On Commanded |
| :--- | :--- |
| `caveman`[^external-agent-skill] | 간결한 문장 구조를 명령 받은 경우 |
| `ponytail`[^external-agent-skill] | 코드 오버 엔지니어링 리뷰를 명령 받은 경우 |

## Boundaries

- 리뷰만 수행
- 리뷰 대상 수정 금지

[^external-agent-skill]: 외부 에이전트 스킬
