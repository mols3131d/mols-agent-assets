# Iceberg Code Report

> **Status: Alpha**
>
> 내부 시험과 dogfooding을 위한 초기 버전입니다. Workflow, config schema, 출력 형식은 호환성 보장 없이 변경될 수 있습니다. 생성된 report는 공유하기 전에 사람이 확인해야 합니다.

코드베이스의 목적, 핵심 component, 실행 흐름, 상태 변경, 외부 경계를 설명하는 Markdown report를 만드는 agent skill입니다. 현재 코드의 이해를 돕는 데 집중하며 product code는 수정하지 않습니다.

## 사용법

사용법을 문서에서 직접 찾지 말고 agent에게 아래 명령을 전달합니다.

```text
/iceberg-code-report --help
```

Agent가 가능한 작업부터 보여주고 workflow, 입력, 기본값, 결과, 제한으로 단계적으로 안내합니다. 원하는 항목을 선택해 대화를 이어가면 됩니다. 전체 사용법을 한 번에 출력하지 않으며 실제 작업을 요청하기 전에는 파일이나 config를 변경하지 않습니다.

## 주요 결과

- 코드베이스 전체 구조를 설명하는 `__summary__.md`
- 요청한 component의 상세 문서
- Config와 기준시에 따라 생성된 report directory
- 코드와 테스트에 근거한 file·line link

## Alpha 제한

- 의미 기반 routing 사례가 아직 자동 test로 고정되지 않았습니다.
- Report 품질은 repository의 코드, 테스트, 문서 완성도에 영향을 받습니다.
- 복잡한 동적 호출이나 외부 runtime 동작은 코드만으로 확정하지 못할 수 있습니다.
- Template과 workflow 계약이 변경될 수 있습니다.
- 생성 결과의 기술적 정확성과 링크를 사람이 최종 확인해야 합니다.

설계 결정은 [`decision.md`](decision.md)에서 확인할 수 있습니다. Agent 실행 규칙과 상세 사용법은 agent가 skill 자산에서 직접 읽습니다.
