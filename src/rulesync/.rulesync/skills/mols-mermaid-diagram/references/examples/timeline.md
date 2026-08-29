# Timeline

> Timeline syntax와 version-specific feature 지원은 target renderer와 Mermaid 공식 문서를 확인한다.

사건의 duration보다 **ordered periods, milestones와 era grouping**이 중요하면 `timeline`을 사용한다. Mermaid Timeline의 period는 date type이 아니라 text이며, renderer가 날짜를 parse·sort하거나 시간 간격을 scale로 계산하지 않는다.

## Basic: Ordered Milestones

```mermaid
timeline
    title Release history
    2024 : Baseline published
    2025 : Validation added
    2026 : Recovery workflow introduced
```

Source order가 rendered chronology를 소유한다. 실제 날짜가 있는 source를 timeline으로 옮길 때는 먼저 source facts를 시간순으로 정렬·검증하고, renderer가 잘못된 순서를 교정해 줄 것으로 기대하지 않는다.

Visual spacing도 elapsed time에 비례하지 않는다. `2024 → 2025`와 `2025 → 2030`이 비슷한 간격으로 보이더라도 같은 duration을 뜻하지 않는다.

## Period Granularity And Same-Period Events

같은 temporal bucket에 여러 사실이 실제로 속할 때 한 period 아래 여러 event를 둘 수 있다.

```mermaid
timeline
    title Reliability program history
    2024-02 : Baseline measured
            : Two source failures observed
    2024-05 : Contract gaps confirmed
    2024-07 : Data contract adopted
    2025-04 : Validation rollout started
            : Tier-1 sources covered first
    2026-01 : Automated recovery enabled
```

같은 period 아래의 여러 event는 **co-located facts**일 뿐이다.

- event의 위아래 순서만으로 causality, dependency, approval chain 또는 within-period chronology를 주장하지 않는다.
- 서로 다른 날짜에 일어난 사실을 compact하게 보이기 위해 하나의 period로 합치지 않는다.
- month → quarter → year처럼 source granularity를 낮춰야 한다면 질문에 필요한 수준인지 확인하고, 해석에 영향을 주는 aggregation은 드러낸다.
- within-period order가 중요하면 더 세밀한 period를 사용하거나 sequence/flowchart 같은 다른 type을 검토한다.

## Sections Are Contiguous Grouping

`section`은 독립적인 parallel lane이 아니라 **뒤따르는 period들을 다음 section 전까지 묶는 contiguous grouping**이다. Era, release generation, contiguous phase처럼 chronology와 함께 이어지는 구간에 사용한다.

```mermaid
timeline
    title Reliability program evolution
    section Discovery
        2024-02 : Baseline measured
        2024-05 : Contract gaps confirmed
    section Decision
        2024-07 : Data contract adopted
        2025-01 : Reconciliation selected
    section Delivery
        2025-04 : Validation rollout
        2025-09 : Recovery API released
    section Operations
        2026-01 : First automated recovery
        2026-06 : Policy revised
```

Owner, team, workstream처럼 시간이 지나며 반복해서 등장하는 category를 section별로 모으기 위해 실제 chronology를 재정렬하지 않는다. 같은 section label을 나중에 다시 열어 recurring lane처럼 사용하지도 않는다. Category가 interleave되면 section을 줄이거나 separate timelines, table 또는 질문에 더 직접적인 다른 representation을 사용한다.

## Decision History Without Invented Causality

Timeline은 decision history를 보여줄 수 있지만 **decision rationale나 evidence 관계를 edge로 표현하지 않는다.** Evidence와 decision이 서로 다른 시점에 존재하면 각각 실제 period에 둔다.

```mermaid
timeline
    title Project decision history
    section Evidence
        2025-01 : Source schema reviewed
        2025-03 : Reconciliation failures observed
    section Decision
        2025-04 : Quality gate approved
    section Delivery
        2026-02 : Recovery API released
```

Source가 `evidence → decision` 관계를 명시적으로 뒷받침한다면 companion prose나 별도 relationship-oriented diagram으로 그 관계를 설명한다. 과거 evidence를 나중 milestone 아래 두 번째 event로 옮겨 같은 시점에 발생한 것처럼 보이게 하지 않는다.

## Direction And Viewport

Mermaid v11.14+는 `LR`과 `TD` direction을 지원한다. Direction은 presentation choice이며 source order와 chronology를 바꾸지 않는다.

```mermaid
timeline TD
    title Release history
    2024 : Baseline published
    2025 : Validation added
    2026 : Recovery workflow introduced
```

Portrait reading viewport에서 LR이 과도하게 넓어지면 target renderer가 지원할 때 `TD`를 우선 검토한다. 오래된 renderer에 unsupported direction을 억지로 넣지 않고 LR, split 또는 fallback을 사용한다.

## Choosing Timeline Versus Other Types

- **Timeline**: ordered milestones, periods, eras와 contiguous grouping이 핵심일 때.
- **Gantt**: duration, overlap, start/end date, dependency 또는 proportional time axis가 핵심일 때.
- **Sequence / Flowchart**: message order, process transition, causality 또는 branching relationship이 핵심일 때.
- **Table**: exact timestamps, sortable records, recurring categories 또는 비교 가능한 여러 fields가 핵심일 때.

Timeline의 visual gap이나 section layout으로 duration, overlap, causality 또는 parallel ownership을 암시하지 않는다.

## Renderer-Sensitive Review

Timeline은 syntax validity와 temporal fidelity를 따로 검증한다.

1. rendered period 순서가 source chronology와 일치하는가.
1. period granularity를 줄이면서 distinct events를 같은 시점으로 합치지 않았는가.
1. same-period event를 causal/dependency chain처럼 읽히게 만들지 않았는가.
1. section 때문에 interleaved chronology가 재정렬되거나 같은 section이 lane처럼 재사용되지 않았는가.
1. LR/TD 선택이 target renderer에서 지원되고 portrait viewport에서 읽을 수 있는가.
1. long period/event label과 여러 same-period events가 clipping이나 과도한 vertical growth를 만들지 않는가.

문제가 있으면 styling으로 숨기기보다 label 축약, period granularity 조정, section 축소, direction 변경 또는 diagram split을 먼저 검토한다.

## Rules

- Period text를 date parser나 automatic sorter처럼 취급하지 않는다.
- Source order를 chronology와 일치시킨다.
- Visual distance를 elapsed duration으로 해석하지 않는다.
- Same-period events는 co-location만 의미하며 causality·dependency를 만들지 않는다.
- Section은 contiguous grouping이며 recurring category를 위한 parallel lane이 아니다.
- Evidence, decision과 consequence의 실제 시점을 보존한다.
- duration, overlap, dependency 또는 proportional time scale이 중요하면 Timeline 대신 더 직접적인 type을 사용한다.

## Portable Fallback

Target renderer가 Timeline이나 필요한 direction을 지원하지 않으면 source order와 의미 있는 section grouping을 보존하는 ordered list 또는 table로 전환한다. Duration·overlap이 중요한 경우에는 의미를 보존할 수 있을 때 Gantt를 사용하며, Timeline의 visual spacing을 fallback에서 실제 time scale처럼 재현하지 않는다.
