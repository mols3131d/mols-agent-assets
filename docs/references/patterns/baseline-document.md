# Baseline Document

자산이 개발·튜닝 과정에서 훼손되거나 변질되어도 **원래 의도와 본질을 복원할 수 있게 하는 recovery baseline** 패턴입니다.

## Layout

```text
<asset-docs>/
├─ baseline.md
└─ baseline/
   └─ ...
```

작으면 `baseline.md`, 내용이 커지면 `baseline/`을 사용합니다.

## Contents

Baseline에는 현재 구현 상태가 아니라 쉽게 잃어버리면 안 되는 핵심을 남깁니다.

- 목적과 비전
- 본질과 핵심 원리
- 주요 원칙과 요구
- 중요한 결정과 rationale
- 장기 목표와 protected invariant

## Boundary

- 작업 로그, 일시적 상태, 세부 구현 기록은 baseline에 누적하지 않습니다.
- 현재 구현이 baseline과 다르면 구현을 정답으로 가정하지 않고 의도된 변경인지 먼저 확인합니다.
- 핵심 의도를 바꾸는 변경은 baseline도 함께 갱신합니다.
- Baseline은 runtime source를 대체하지 않습니다. 목적은 **복원·검토·튜닝 기준점**을 제공하는 것입니다.
