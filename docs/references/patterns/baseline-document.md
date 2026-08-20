# Baseline Document

자산이 개발·튜닝 과정에서 훼손되거나 변질되어도 **원래 의도와 본질을 복원할 수 있게 하는 recovery baseline** 패턴입니다.

## Purpose

현재 구현이나 일시적 상태와 별개로, 자산이 무엇을 위해 존재하고 무엇을 잃으면 안 되는지 장기적으로 보존합니다.

## Core

- Baseline은 목적, 본질, 원칙, 주요 요구와 결정처럼 쉽게 잃어버리면 안 되는 내용을 보존합니다.
- 일반적인 구현 변경이나 정리 작업에 맞춰 자동으로 동기화하지 않습니다.
- 현재 구현이 baseline과 다르면 구현을 자동으로 정답으로 보지 않고 의도된 변경인지 확인할 수 있어야 합니다.
- Baseline 자체의 변경은 자산의 본질이나 장기 의도를 바꾸는 **의도적인 결정**으로 취급합니다.

## Typical Forms

권장되는 간단한 형태는 `baseline.md`, 내용이 커졌을 때의 형태는 `baseline/README.md`를 entrypoint로 하는 directory입니다.

```text
<asset-docs>/
├─ baseline.md

# or

<asset-docs>/
└─ baseline/
   ├─ README.md
   └─ ...
```

Project가 다른 구조를 사용할 수는 있지만, baseline의 entrypoint와 보호 성격은 쉽게 식별할 수 있어야 합니다.

## Recommended Contents

- 목적과 비전
- 본질과 핵심 원리
- 주요 원칙과 요구
- 중요한 결정과 rationale
- 장기 목표와 protected invariant

필요한 항목만 선택하고, 자산의 복구에 실제로 도움이 되는 내용에 집중합니다.

## Protection

`baseline.md` 또는 `baseline/README.md` 같은 baseline entrypoint에는 **함부로 편집하면 안 되는 보호 문서임을 명시합니다.**

일반 구현 변경에 맞춰 baseline을 자동 수정하지 않고, 목적·본질·원칙·중요 결정 자체를 바꾸려는 경우에만 변경 의도와 근거를 확인하도록 할 수 있습니다. 구체적인 승인 절차나 변경 workflow는 각 repository가 정합니다.

## Extensions

Baseline이 커지면 주제별 파일로 나누고 entrypoint에서 연결할 수 있습니다. 분할하더라도 하나의 recovery baseline으로 이해할 수 있게 유지합니다.

## Boundary

- 작업 로그, 일시적 상태, 세부 구현 기록을 baseline의 주된 내용으로 삼지 않습니다.
- Baseline은 runtime source나 현재 구현 문서를 대체하지 않습니다.
- 이 패턴은 특정 승인 절차, 파일 구조, 버전 관리 방식을 강제하지 않습니다.

핵심은 **자산의 원래 의도와 본질을 복구할 수 있는 보호된 기준점**을 유지하는 것입니다.
