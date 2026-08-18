# HMDA Data Development Dashboard

> **Snapshot:** 2026-08-03
> **Current Focus:** Grain alignment와 notebook runtime 검증 보강

## Development Progress

| Capability | Implementation Status | Implementation Progress | Verification Status | Verification Progress |
| --- | :---: | --- | :---: | --- |
| Core EDA Evidence | 🟢 Implemented | `██████████ 5/5` | 🟢 Passing | `██████████ 8/8` |
| Numeric Summary | 🟢 Implemented | `██████████ 4/4` | 🟡 Partial | `███████░░░ 3/4` |
| Grain Alignment | 🟡 In Progress | `███████░░░ 3/4` | 🔴 Failing | `███████░░░ 3/4` |
| Notebook Runtime | 🟡 In Progress | `███░░░░░░░ 1/3` | ⚪ Unverified | `░░░░░░░░░░ 0/2` |
| **Total** | **🟡 In Progress** | **`████████░░ 13/16`** | **🔴 Failing** | **`███████░░░ 14/18`** |

## Implementation Gaps

| Capability | # | Remaining Requirement |
| --- | :---: | --- |
| Grain Alignment | 1 | Raw aggregate와 dbt mart 결과 자동 비교 |
| Notebook Runtime | 1 | Valid input runtime smoke 구현 |
| Notebook Runtime | 2 | Malformed input runtime smoke 구현 |

## Verification Gaps

| Capability | # | Remaining Verification |
| --- | :---: | --- |
| Numeric Summary | 1 | ⚪ 극단 경계값 조합 미검증 |
| Grain Alignment | 1 | 🔴 dbt mart aggregate 비교 실패 |
| Grain Alignment | 2 | ⚪ null grain 경로 미검증 |
| Notebook Runtime | 1 | ⚪ Valid input runtime 미검증 |
| Notebook Runtime | 2 | ⚪ Malformed input runtime 미검증 |

## Risks / Blockers

| Area | Risk / Blocker | Impact |
| --- | --- | --- |
| Grain Alignment | Mart 계약이 변경 중임 | 구현과 integration 검증이 다시 깨질 수 있음 |

## References

- OpenSpec capability specifications
- pytest and runtime validation artifacts
