---
description: 저장소의 deterministic test 설계와 repository-owned executable behavior의 검증 근거를 확인할 때 사용하는 정책입니다.
---

# Testing

Testing은 이 repository가 구현한 **실행 가능한 동작**을 deterministic하게 검증합니다. Repository 상태의 구조·파생 계약은 [Validation](validation.md)이, test evidence를 언제 blocking으로 실행할지는 [Continuous Integration](ci.md)이 소유합니다.

## Run

```bash
mise run test
```

Generator, sync, validator, adapter처럼 repository-owned behavior를 검증합니다. Test file 배치는 [Repository Layout](repository-layout.md)이 소유합니다.

현재 설정값이나 upstream schema를 그대로 복제하는 snapshot test는 두지 않습니다. 변경 가능한 config, 문서 표현과 외부 contract는 각각의 owner가 소유합니다.

Generator의 parsing, ordering, failure behavior와 output semantics는 deterministic test로 검증할 수 있습니다. 반면 canonical source에서 다시 만든 committed projection이 최신인지 확인하는 책임은 [Validation](validation.md)과 CI의 projection gate에 둡니다. Projection freshness가 generic test diff에만 숨어 원인을 찾기 어렵게 만들지 않습니다.

CI와 Git hook에서 project Python을 사용할 때는 `uv.lock`을 암묵적으로 갱신하지 않는 `--locked` 실행을 사용합니다.

## Evidence Boundary

Deterministic test success는 해당 repository-owned executable behavior의 검증 근거입니다. Structural validation, projection freshness, semantic routing과 live runtime behavior까지 검증했다고 확대 해석하지 않습니다.

`PR Gate`의 stage order, blocking boundary, trigger와 local hook의 관계는 [Continuous Integration](ci.md)이 소유합니다.
