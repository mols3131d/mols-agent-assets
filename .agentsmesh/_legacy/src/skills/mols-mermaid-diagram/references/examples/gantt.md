# Gantt

작업 기간과 dependency가 핵심이면 `gantt`를 사용한다.

```mermaid
gantt
    title Migration plan
    dateFormat  YYYY-MM-DD
    section Preparation
    Inventory      :done, inventory, 2026-08-01, 2d
    Backfill       :active, backfill, after inventory, 3d
    section Verification
    Reconciliation :verify, after backfill, 2d
```

## Advanced: Milestones And Parallel Work

작업의 완료 여부만 보여주는 대신 milestone과 병렬 작업을 분리하면, critical path와 병렬화 가능 구간을 읽을 수 있다.

```mermaid
gantt
    title Release readiness
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d
    section Foundation
    Contract locked     :milestone, contract, 2026-08-05, 0d
    Schema migration    :migration, after contract, 4d
    Fixture preparation :fixtures, after contract, 3d
    section Validation
    Unit checks         :checks, after migration, 2d
    Data reconciliation :reconcile, after migration, 3d
    section Release
    Go-live review      :review, after checks reconcile, 1d
    Release             :milestone, release, after review, 0d
```

## Improvement: Separate Decision Gates From Work

개선된 Gantt는 사람이 승인해야 하는 decision gate를 일반 task와 구분한다. gate를 dependency로 연결하면 무엇이 완료되어야 다음 작업을 시작할 수 있는지 명확해진다.

```mermaid
gantt
    title Backfill package
    dateFormat  YYYY-MM-DD
    section Prepare
    Inventory       :inventory, 2026-08-01, 2d
    Dry run         :dryrun, after inventory, 2d
    Approval gate   :milestone, approval, after dryrun, 0d
    section Execute
    Backfill        :backfill, after approval, 3d
    Validate        :validate, after backfill, 2d
    Publish report  :report, after validate, 1d
```
