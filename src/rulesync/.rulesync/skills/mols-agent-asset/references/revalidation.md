# Revalidation

Baseline, prior validation/eval result 또는 이전 revision이 있으면 current snapshot을 fresh하게 다시 확인한다.

## Compare

- baseline asset, result와 revision을 식별한다.
- current target과 baseline의 material delta를 확인한다.
- prior finding과 claim을 current asset에서 다시 검증한다.
- 실제 performance가 claim의 일부이고 runtime을 사용할 수 있으면 필요한 case를 다시 실행한다.
- prior result를 수정하거나 덮어쓰지 않는다.

## States

| State | Meaning |
| --- | --- |
| `resolved` | current evidence에서 prior defect가 더 이상 존재하지 않음 |
| `unresolved` | current evidence에서도 defect가 존재함 |
| `superseded` | architecture 또는 contract 변경으로 prior claim의 기준이 사라짐 |
| `not_retested` | 필요한 runtime, fixture 또는 capability가 없어 다시 확인하지 못함 |
| `new` | current snapshot에서 새로 발견됨 |

Prior `pass`나 `blocked` 상태는 current snapshot에 자동 승계하지 않는다.
