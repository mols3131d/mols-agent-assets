---
title: uv and Python
description: uv·Python의 관리 경계, 버전 선택과 프로젝트 가상환경, Python 개발 도구의 설정·갱신 예외를 확인할 때 사용합니다.
---

# uv and Python

uv는 Python 인터프리터와 프로젝트 패키지를 관리합니다. uv 실행파일 버전은 [`mise.toml`](../../mise.toml), Python은 [`.python-version`](../../.python-version)과 [`pyproject.toml`](../../pyproject.toml), 의존성 선택은 [`uv.lock`](../../uv.lock)이 소유합니다.

## 기본 설정과 예외

[공통 원칙](README.md#공통-원칙)에 따라 최신 안정 uv·Python·패키지를 우선 검토합니다. Python은 프로젝트 요구조건과 dependency 지원이 확인된 버전을 선택하며, 문서에서 최신 버전 숫자를 별도로 관리하지 않습니다.

- uv는 resolver·명령 호환성을 확인한 exact pin을 사용합니다. Python은 mise에 중복 선언하지 않습니다.
- 패키지는 프로젝트 `.venv`에 격리합니다. 활성화된 외부 venv나 시스템·사용자 site-packages로 프로젝트 의존성을 대신하지 않습니다.
- bootstrap은 Python 자동 다운로드를 끄고 `.python-version`의 interpreter를 먼저 준비하게 합니다. 일반 uv 사용 전체의 기본값을 바꾼다는 의미는 아닙니다.
- `setup`은 `--locked`로 기존 잠금을 재현하며, `update`만 `pyproject.toml`의 constraint 안에서 `uv lock --upgrade`를 수행합니다. 범위 확대와 Python 자체의 버전 변경은 별도로 검토합니다.
- bootstrap은 `--all-groups`로 개발·테스트 도구까지 준비합니다. CI와 개별 task는 `--no-default-groups`와 필요한 group을 명시해 실행 범위를 좁힙니다.

## Python 개발 도구

Ruff·pytest는 별도 전역 CLI가 아니라 uv의 `dev`·`test` group에 둡니다. 최신 안정 릴리스를 검토하되 실제 실행 버전은 `uv.lock`으로 재현합니다. 의존성 갱신은 `setup`이 아니라 명시적 `update`와 diff 검토에서 처리합니다.

Ruff는 `pyproject.toml`의 lint 선택(`F`, `E`, `I`)과 import 정렬 설정을 적용합니다. pytest는 같은 파일의 import mode·Python path·test 경로를 사용합니다. 기본값과 다른 선택은 이 native 설정이 정본이며 일반 명령은 [Formatting](../development/formatting.md)과 [Testing](../development/testing.md)을 따릅니다.

## Official Sources

- [uv projects](https://docs.astral.sh/uv/concepts/projects/) · [Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [Ruff configuration](https://docs.astral.sh/ruff/configuration/)
- [pytest configuration](https://docs.pytest.org/en/stable/reference/customize.html)
