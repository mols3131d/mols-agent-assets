---
description: 세션 단절·에이전트 교체 후 Git 커밋 메시지와 스냅샷에서 작업 상태·검증·다음 시작점을 복구하려는 경우 참고하는 체크포인트 패턴입니다.
---

# Session Recovery Checkpoint Commits

커밋에 코드가 남아도 변경 이유, 검증 한계, 다음 확인 지점은 diff에서 드러나지 않을 수 있습니다. **의미 있는 커밋의 메시지에 이런 단서를 필요한 만큼 남기면** 세션이 끊기거나 작업자가 바뀌어도 재탐색 비용을 줄일 수 있습니다.

이 패턴은 **기록된 커밋에서 작업 재개 단서를 찾는 방식**으로, 세션 전체나 미커밋 작업까지 복원하지는 못합니다.

## When to Use

- **적합:** 이미 독립적으로 검토할 만한 변경을 커밋하고 있고, 다음 작업자가 diff만으로 알기 어려운 판단이나 검증 범위가 있습니다.
- **다른 수단이 적합:** 코드 변경 없이 작업 상태만 남기거나, 여러 커밋에 걸친 목표·의존성·진행 상황을 지속적으로 갱신해야 합니다. 이때는 PR·작업 기록 또는 [Durable Progress Handoff](durable-progress-handoff.md) 같은 별도 인계 수단을 고려합니다.

## Core

- **좋은 커밋 우선:** 커밋은 의미 있게 완결된 변경을 담아 이해·검토·되돌리기 쉬워야 합니다. 복구를 위해 변경을 억지로 나누거나 미완료 상태를 통합 가능한 변경으로 포장하지 않습니다.
- **차이만 기록:** 제목과 본문은 변경 내용과 이유를 설명하고, 복구 맥락은 Git diff·기존 본문·PR·명세에 없는 정보만 보완합니다. 중요한 결정, 검증 한계, 후속 조건처럼 다시 알아내기 비싼 정보에 집중합니다.
- **컨텍스트 최적화:** 다음 사람이 **적은 토큰 비용**으로 읽고 **적은 추론 비용**으로 재개 지점을 판단할 수 있게 중복을 줄입니다. 다만 짧게 쓰느라 필요한 근거와 불확실성을 생략하지 않습니다.
- **현재 상태 우선:** 메시지의 검증·계획은 해당 커밋 당시의 기록입니다. 재개할 때는 현재 코드, ref, 작업 공간과 검증 근거를 대조합니다.

## Sample Commit Message

샘플의 제목 형식은 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)를 참고했을 뿐, 이 규약의 채택이나 준수를 전제하지 않습니다. 실제 형식은 적용하는 프로젝트가 정합니다.

```text
<type>[optional scope][!]: <description>

[optional body]

[optional continuation context: only what the body does not cover]

[optional footer(s)]
```

`continuation context`는 필드나 스키마가 아닌 **본문에 없는 재개 단서의 작성 힌트**입니다. 기존 본문에 합칠 수 있고, 중복·불필요하면 생략합니다. Footer도 프로젝트에서 사용할 때만 둡니다.

간단한 변경에는 제목만으로 충분합니다.

```text
fix(auth): reject expired access tokens
```

검증 한계와 후속 확인이 중요한 경우에는 본문에 자연스럽게 남깁니다.

```text
refactor(auth): separate token expiry policy

Keep expiry rules independent of HTTP middleware so policy
tests do not require HTTP request setup.

Token policy unit tests passed locally; middleware integration
remains unverified. Confirm the request schema before adding
integration tests.
```

## Typical Use

1. **기록:** 커밋할 diff와 수행한 검증 범위를 확인한 뒤, 메시지에 없는 중요한 판단·제약·후속 조건만 보완할 수 있습니다. 미실행 검사를 통과로 적지 않으며 커밋 자체의 SHA는 메시지에 미리 넣지 않습니다.
2. **재개:** 올바른 작업·저장소·브랜치/PR과 현재 working tree를 먼저 확인하고, 해당 작업의 커밋을 찾아 메시지와 스냅샷을 읽습니다. 그 커밋이 반드시 HEAD인 것은 아닙니다. 이후 변경 및 외부 계약과 대조하고 필요한 검증을 거쳐 다음 행동을 결정합니다.

다른 실행 환경에서 재개하려면 해당 커밋이 **조회 가능한 원격 ref에 게시**되어 있어야 합니다.

## Limits

- **체크포인트 이전의 공백:** 커밋 이후 미커밋 변경이나 폐기된 로컬 상태까지 복구하지는 못합니다. 남아 있는 변경은 다른 작업자의 소유 여부를 확인하고 보존해야 합니다.
- **이력의 지속성:** amend·rebase·branch 삭제 또는 [Squash Merge](https://docs.github.com/en/pull-requests/reference/pull-request-merges)로 중간 커밋을 찾기 어려워질 수 있습니다. 오래 보존할 결정은 PR·명세 등 지속적인 소유 위치에 옮깁니다.
- **기록의 신뢰성:** 과거의 검사 결과나 후속 제안은 현재의 사실·지침·실행 권한이 아닙니다. 변경된 ref·계약·환경에 맞춰 확인하고, 다른 작업자의 변경을 덮어쓰지 않습니다.
- **정보 노출:** 커밋 메시지는 공유·영구 보존될 수 있습니다. 비밀정보, 개인정보, 내부 대화나 공개하면 안 되는 내용을 넣지 않습니다.

## Boundary

이 패턴은 **코드 스냅샷에 인접한 커밋 메시지를 재개 단서로 활용하는 선택지**입니다. 긴 작업의 전체 상태나 agent 간 동시 작업 조정, Git 커밋 규약·권한은 다루지 않습니다. 이들은 별도 작업 기록과 적용 대상 프로젝트의 규칙이 소유합니다.
