---
name: write-summary
description: 코드와 테스트를 근거로 report bundle의 __summary__.md를 작성한다.
---

# Write Report Summary

## Goal

현재 코드의 목적, 구조, 책임, 핵심 실행 흐름을 한 문서에서 먼저 이해하게 한다.

## Required Inputs

- `report_dir`: 기존 report directory. 없으면 `create-dir`를 먼저 실행한다.
- `report_target`: file 또는 directory. 기본값은 current working directory.
- `focus`: 선택. 기본값은 핵심 진입점과 실행 경로.
- `audience`: 선택. 기본값은 해당 기술에 익숙한 주니어 개발자.

## Procedure

1. `<skill-root>/templates/__summary__.md`를 `<report_dir>/__summary__.md`의 기반으로 사용한다.
2. 프로젝트 안내 문서, package manifest, 진입점, source tree를 확인한다.
3. 핵심 진입점에서 저장소·외부 시스템·최종 출력까지 대표 호출 흐름을 추적한다.
4. 핵심 component를 책임, 입력, 출력, 직접 dependency, 상태 변경 기준으로 정리한다.
5. 테스트에서 사용법, 계약, 예외 경계를 확인하고 필요한 최소 검증만 실행한다.
6. Overview, System Map, Core Components, Core Execution Walkthroughs, Code Reading Guide, Understanding Notes를 작성한다.
7. detail 문서가 없으면 Core Components의 link placeholder를 일반 symbol·file link로 바꾼다.
8. placeholder와 작성 지침 주석을 제거하고 file·line link를 실제 코드와 대조한다.

## Validation

1. 아래 command가 exit code `0`을 반환해야 한다.

   ```bash
   <PYTHON_EXEC> "<skill-root>/scripts/validate_report.py" "<report_dir>/__summary__.md" --type summary --project-root "<project_root>"
   ```

- `<report_dir>/__summary__.md`가 존재한다.
- walkthrough가 실제 호출 순서와 일치하고 주요 주장에 유효한 file·line link가 있다.
- 확인하지 못한 내용은 `미확인` 또는 `추론`으로 표시했다.
- 불필요한 주변 모듈, 중복 설명, 평가성 권고를 제거했다.

## Stop Conditions

- 코드나 설정을 수정하지 않는다.
- 기존 `__summary__.md`를 덮어쓸 권한이 명확하지 않으면 중단한다.
