# Cynefin Diagram

> Mermaid v11.16.0+의 `cynefin-beta` 문법이다.

문제를 Clear, Complicated, Complex, Chaotic, Confusion domain으로 분류하고 대응 방식을 선택할 때 사용한다.

## Basic: Classify Work

```mermaid
cynefin-beta
    title Data Platform Decisions

    complex
        "Discover a new data product"
        "Investigate emergent user behavior"

    complicated
        "Tune distributed query performance"

    clear
        "Rotate an expired credential"
        "Run a documented backfill"

    chaotic
        "Stop active data corruption"

    confusion
        "Unclassified production anomaly"
```

## Advanced: Incident Movement And Learning Between Domains

Advanced example은 각 domain의 현재 work와 domain 사이의 movement를 함께 보여준다. transition label은 상태 변화의 evidence나 action을 설명한다.

```mermaid
cynefin-beta
    title Incident Sensemaking And Learning Loop

    complex
        "Probe unknown failure mode"
        "Run safe recovery experiments"

    complicated
        "Analyze repeated pattern"
        "Review architecture constraint"

    clear
        "Apply codified runbook"
        "Execute verified rollback"

    chaotic
        "Contain active corruption"
        "Disable unsafe publisher"

    confusion
        "Conflicting telemetry"

    confusion --> chaotic : "Impact confirmed"
    confusion --> complex : "Safe probe defined"
    chaotic --> complex : "Impact stabilized"
    complex --> complicated : "Repeatable pattern identified"
    complicated --> clear : "Runbook and guardrail verified"
    clear --> complicated : "Exception breaks the rule"
    clear --> chaotic : "Control failure causes collapse"
```

이 예시는 domain별 work, evidence-driven transitions, learning loop와 collapse risk를 결합한다.

## Rules

- domain 이름은 fixed keyword다.
- Confusion에는 가능한 한 적은 항목만 둔다.
- transition은 서로 다른 domain 사이에만 사용한다.
