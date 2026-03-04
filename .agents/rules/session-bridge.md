---
trigger: model_decision
description: Protocol for session-bridging via narrative context and entry points.
---

# Session-Bridge Protocol

- **Objective**: 세션 간 휘발성 맥락(Narrative) 전수 및 연속성 확보.
- **Protocol**:
  - **Zero-Base**: 정보 가치가 낮거나 이미 확정된 데이터는 기록하지 않음.
  - **Delta Only**: 현재 세션의 고유한 논리적 흐름과 특잇값에 집중.
- **Structure**:
  1. **Narrative**: 세션의 논리적 흐름, 설계 의도, 미해결 마찰(Hurdles).
  2. **Entry Point**: 다음 세션 시작 시 즉시 실행할 구체적 액션.
- **Lifecycle**: 세션 종료 시 작성(Write), 새 세션 시작 시 참조 후 초기화(Clear).
