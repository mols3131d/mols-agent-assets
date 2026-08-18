# Re-validation

## Purpose

이전 validation result 또는 asset revision이 있을 때 current snapshot을 fresh하게 검증한다.

## Procedure

- Baseline asset, result와 revision을 식별한다.
- Current target과 baseline의 material delta를 확인한다.
- Prior finding의 claim을 current asset에서 다시 검증한다.
- Current runtime이 있으면 필요한 case를 다시 실행한다.
- Prior result를 수정하거나 덮어쓰지 않는다.

## Delta States

| State | Meaning |
| --- | --- |
| `resolved` | current evidence에서 prior defect가 더 이상 존재하지 않음 |
| `unresolved` | current evidence에서도 defect가 존재함 |
| `superseded` | architecture 또는 contract 변경으로 prior claim의 기준이 사라짐 |
| `not_retested` | 필요한 runtime, fixture 또는 access가 없어 다시 확인하지 못함 |
| `new` | current snapshot에서 새로 발견됨 |

Prior `pass`는 current snapshot에 자동 승계되지 않는다. Prior `blocked`도 current condition이 해소됐는지 fresh하게 확인한다.
