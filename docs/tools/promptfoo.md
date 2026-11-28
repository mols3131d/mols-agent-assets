---
title: Promptfoo
description: Promptfoo의 평가 재현용 버전 고정, 저장소 runner의 기본 환경과 데이터·모델·비용 예외를 확인할 때 사용합니다.
---

# Promptfoo

Promptfoo는 Agent Asset의 model/runtime 평가에 사용합니다. 실행 진입점은 [`mise.toml`](../../mise.toml)의 `eval` task, CLI pin과 환경 기본값은 [`promptfoo_run.py`](../../scripts/agent_assets/promptfoo_run.py), 평가 조건은 [`evals/promptfoo/`](../../evals/promptfoo/)가 소유합니다.

## 실행

`mise run eval`은 저장소 평가 설정 하나와 명시적인 model·provider·grader 선택을 받습니다. 실행 예제, 인증, suite별 지원 범위는 평가 문서에 있습니다. 모델·grader 실행은 사용자 요청에 따르며 CI, bootstrap, hook, check 및 세션 진단은 deterministic 검증을 실행합니다. [평가 실행 설정](../../evals/README.md#promptfoo-provider-selection)

## 버전과 실행 환경

- Runner는 Promptfoo `0.126.0`과 Node `22.22.0` 이상을 요구합니다. 저장소 mise는 Node `26.13.0`을 고정합니다. Codex를 선택한 경우에만 native SDK와 연결된 CLI `0.169.1`을 같은 npm 실행 환경에서 해석합니다.
- Runner는 telemetry, update check, remote generation 및 sharing을 끕니다. Promptfoo 상태 디렉터리는 프로젝트 `.tmp/promptfoo`에 두고, 생성 설정과 Codex 작업 디렉터리는 임시 경로에 둡니다. Suite 설정은 캐시·기본 결과 저장을 끕니다.
- Python fixture generator와 assertion은 runner의 Python을 사용합니다. Ollama 요청 제한과 Codex 실행의 case 제한은 별도로 설정합니다. 원격 provider의 데이터 전송·비용은 평가 선택에 따릅니다.
- CLI·provider·model 변경은 config·assertion 호환성, fixture smoke, 실제 모델 결과를 각각 확인합니다. [Evaluation](../development/evaluation.md)

## 권장 버전 정책

**Exact**를 유지합니다. 동일한 평가를 비교할 때 CLI 버전, 평가 데이터, provider·model과 grader 조건을 구분할 수 있어야 하기 때문입니다. 버전 전환은 `promptfoo_run.py`에서 명시적으로 수행하고 별도 평가 검증으로 확인합니다. mise의 범위 추적이나 자동 `latest`로 이 pin을 대체하지 않습니다.

## 상세 안내

- [Promptfoo reference](../development/tooling/promptfoo.md): config·provider·grading·data boundary의 공식 source
- [Official documentation](https://www.promptfoo.dev/docs/intro/) · [Releases](https://github.com/promptfoo/promptfoo/releases)
