---
title: Promptfoo
description: Promptfoo의 평가 재현용 버전 고정, 저장소 runner의 기본 환경과 데이터·모델·비용 예외를 확인할 때 사용합니다.
---

# Promptfoo

Promptfoo는 Agent Asset의 model/runtime 평가에 사용합니다. 실행 진입점은 [`package.json`](../../package.json), CLI pin과 환경 기본값은 [`promptfoo_run.py`](../../scripts/agent_assets/promptfoo_run.py), 평가 조건은 [`evals/promptfoo/`](../../evals/promptfoo/)가 소유합니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 최신 안정 릴리스를 검토하되 **비교 가능한 평가 조건**을 우선합니다. runner가 선택한 CLI 버전과 최소 Node 요구조건을 따르며, 같은 평가 중에 `latest`로 교체하지 않습니다. Promptfoo는 mise 관리 CLI 7종과 별도의 runner pin입니다.

- runner는 telemetry·update check·remote generation·sharing을 끄는 값을 기본으로 제공합니다. `setdefault` 기반이므로 이미 지정한 환경값을 강제로 덮어쓰는 보안 통제가 아닙니다. 민감한 평가에서는 실제 환경과 provider를 확인합니다.
- 상태·log·cache는 기본적으로 프로젝트 `.tmp/promptfoo` 아래에 둡니다. 다른 경로를 명시했다면 그 설정이 적용됩니다.
- Python adapter는 실행 중인 Python을, runtime model과 grader는 runner의 기본값 또는 명시한 환경값을 사용합니다. 외부 API·모델 다운로드·hosted 기능의 사용 권한이나 비용 승인을 자동으로 부여하지 않습니다.
- cache와 결과 쓰기는 각 task의 인자를 따릅니다. 모든 task가 `--no-cache`·`--no-write`를 사용한다고 가정하지 않습니다.

CLI·provider·model을 갱신하면 config·assertion 호환성과 결과 변화를 구분해 확인합니다. deterministic test와 model 평가의 증거 수준은 [Evaluation](../development/evaluation.md)이 소유합니다.

## 권장 버전 정책

**Exact**를 유지합니다. 동일한 평가를 비교할 때 CLI 버전, 평가 데이터, provider·model과 grader 조건을 구분할 수 있어야 하기 때문입니다. 버전 전환은 `promptfoo_run.py`에서 명시적으로 수행하고 별도 평가 검증으로 확인합니다. mise의 범위 추적이나 자동 `latest`로 이 pin을 대체하지 않습니다.

## 상세 안내

- [Promptfoo reference](../development/tooling/promptfoo.md): config·provider·grading·data boundary의 공식 source
- [Official documentation](https://www.promptfoo.dev/docs/intro/) · [Releases](https://github.com/promptfoo/promptfoo/releases)
