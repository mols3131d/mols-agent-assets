---
name: agent-asset-optimize
description: 사용 시점: 모델의 효율성과 안전성을 극대화하기 위해 하나 이상의 에이전트 자산을 최적화하고자 할 때. 제외 대상: 자산의 동작 방식, 안전성 한계, 또는 워크스페이스 외부 파일을 수정할 때.
---

# 에이전트 자산 최적화 (Optimize Agent Asset)

## Goal (목표)

모델 효율성과 안전성을 극대화하기 위해 하나 이상의 에이전트 자산(스킬, 워크플로우, 레퍼런스)을 최적화합니다.

## When to Use (사용 시점)

에이전트 자산의 동작 방식을 변경하지 않고 크기 압축, 구조 리팩토링 또는 형식 정리를 수행할 때 이 워크플로우를 사용합니다.

## Instructions (지침)

- 핵심 최적화 철학은 [references/zen-of-agent-assets.md](../references/zen-of-agent-assets.md)를 읽으십시오.
- 자세한 산문(prose) 압축 규칙은 [references/agent-asset-compress.md](../references/agent-asset-compress.md)를 읽으십시오.
- 구조 및 유효성 검사에는 `scripts/validate_asset.py`를 사용하십시오.
- 동작을 변경하거나 안전 범위를 위반하는 최적화를 수행하기 전에 중단하십시오.
- 대상 자산이 유효한 마크다운 또는 자연어 파일이 아닌 경우 중단하십시오.
- 명시적인 권한 없이 활성 워크스페이스의 일부가 아닌 파일을 압축하거나 수정하지 마십시오.

## Workflow: 에이전트 자산 최적화 (Optimize Agent Asset)

### Arguments from Context (컨텍스트 인자)

- 대상 자산 경로
- 희망하는 최적화 결과 (크기 압축, 구조 리팩토링, 형식 정리)

### Procedure (절차)

1. [references/zen-of-agent-assets.md](../references/zen-of-agent-assets.md) 및 [references/agent-asset-compress.md](../references/agent-asset-compress.md)를 읽습니다.
2. 최적화 전략을 선택합니다:
   - **크기 감소**: [references/agent-asset-compress.md](../references/agent-asset-compress.md)의 규칙을 적용하여 미사여구, 모호한 표현 및 중복된 문장을 제거합니다.
   - **구조 정렬**: 깊은 디렉터리를 단일화하고, 빈 뼈대 생성을 피하며, `zen-of-agent-assets`에 따라 수동적인 논리를 공유 레퍼런스로 추출합니다.
   - **서식 및 링크**: 모든 상호 참조가 명시적인 경로와 링크를 사용하는지 확인하고, 마크다운 린트 경고를 해결합니다.
3. 수정하기 전에 `references/agent-asset-backup.md`에 정의된 백업 프로토콜을 따르십시오.
4. 동작을 보존하는 최소한의 변경 사항을 적용합니다. 대대적인 재작성은 피하십시오.
5. `python3 scripts/validate_asset.py`를 사용하여 수정된 자산을 검증합니다.

### Validation (검증)

- 의미, 능력, 트리거 및 안전 제약 조건이 완전히 보존되어야 합니다.
- 코드 블록, 명령 및 숫자 구성이 원본과 동일하게 유지되어야 합니다.
- 정밀도를 잃지 않으면서 전체 컨텍스트 크기(행 수, 토큰 수)가 줄어들어야 합니다.
- 모든 내부 및 상대 링크가 올바르게 확인되어야 합니다.
