# Platform Compatibility

## Core and Adapter

범용 코어에는 목적, 권위, 워크플로, 품질 기준만 둔다. 다음 항목은 환경 adapter로 취급한다.

| Concern | Examples |
| --- | --- |
| Metadata | 지원 frontmatter 필드, UI metadata 파일 |
| Discovery | 스킬 경로, trigger 해석 방식 |
| Tools | tool 이름, connector, MCP, shell 제약 |
| Execution | subagent, background task, approval 모델 |
| Packaging | archive 형식, 포함·제외 규칙 |
| Evaluation | 제공되는 harness, viewer, token metric |

## Tuning Procedure

1. 대상 런타임의 공식 스펙과 실제 저장소 구조를 확인한다.
1. 현재 스킬의 공통 코어와 환경 종속 규칙을 표시한다.
1. 환경 전용 규칙을 `references/platform-<name>.md`, script 옵션 또는 작은 metadata 파일로 격리한다.
1. 다른 환경의 동작을 깨지 않는지 회귀 검증한다.
1. `WORKING.md`에 현재 지원 범위와 알려진 차이를 남긴다.

## Compatibility Rule

최소 공통분모만을 목표로 기능을 약화하지 않는다. 공통 의도는 유지하고 환경별 표현과 실행 경로를 분리한다.
