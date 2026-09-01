---
description: 저장소의 deterministic test 설계, PR Gate와 merge를 차단하는 테스트 근거를 확인할 때 사용하는 정책입니다.
---

# Testing

Testing은 이 repository가 구현한 **실행 가능한 동작**을 deterministic하게 검증합니다. Repository 상태의 구조·파생 계약은 [Validation](validation.md)이 소유합니다.

## Run

```bash
mise run test
```

Generator, sync, validator, adapter처럼 repository-owned behavior를 검증합니다. Test file 배치는 [Repository Layout](repository-layout.md)이 소유합니다.

현재 설정값이나 upstream schema를 그대로 복제하는 snapshot test는 두지 않습니다. 변경 가능한 config, 문서 표현과 외부 contract는 각각의 owner가 소유합니다.

CI와 Git hook에서 project Python을 사용할 때는 `uv.lock`을 암묵적으로 갱신하지 않는 `--locked` 실행을 사용합니다.

## PR Gate

`main` 대상 PR은 `PR Gate`에서 `tests/` 전체를 실행합니다. Workflow-level path filter를 두지 않고, repository에는 write-back하지 않습니다.

PR Gate는 다음 작업을 반복하지 않습니다.

- [Formatting](formatting.md)
- [Validation](validation.md)
- [Evaluation](evaluation.md)
