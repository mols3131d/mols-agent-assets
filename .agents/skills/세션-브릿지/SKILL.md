---
name: "세션 브릿지 (Session-Bridge)"
description: "마크다운(MD)을 활용한 세션 간 연결 및 작업 관리 프로토콜."
---

# 세션 브릿지 (Session Bridge)

> 에이전트 세션의 연속성을 보장합니다.

> **대상 파일 (TARGET_FILE)**: `.agents/brain/session-bridge.md`

## 활성화 (Activation)

- **세션 종료 시**: 달성된 변경 사항(Deltas)을 요약하고 다음 에이전트를 위한 전환점(Pivot)을 정의합니다.
- **세션 시작 시**: `TARGET_FILE`을 로드하여 논리적 흐름을 복구합니다.

## Execution Protocol

정보 손실이 없는 고밀도 구조로 `TARGET_FILE`을 유지 관리합니다:

```markdown
# Session-Bridge

- Intent: [High-level goal]
- Status: [DONE | PARTIAL | BLOCKED]

## Narrative

- [Event / Change] -> [Reasoning / Intent]

## Todo

### Done

- [Task]: [Description]

### Current

- [Task]: [Description]

### Pending

- [Task]: [Description]

## Hurdles

- [Issue]: [Description/Impact]
```

## 핵심 원칙 (Core Principles)

1. **상대 경로**: 프로젝트 루트를 기준으로 한 상대 경로를 사용합니다 (시작 슬래시 제외).
2. **변경분 중심 (Delta-Only)**: 현재 활성화되어 있거나 방금 변경된 사항만 기록합니다. 중복은 배제합니다.
3. **KISS/DRY**: 산문 형태 대신 간결한 불렛 포인트와 체크박스를 사용합니다. 극단적인 미니멀리즘을 지향합니다.
4. **의도 중심 (Intent-Centric)**: 모든 변경 사항에는 `-> [이유/의도]`가 포함되어야 합니다.
5. **단일 소스**: `TARGET_FILE`은 다음 세션을 위한 절대적인 상태 참조 기준입니다.
