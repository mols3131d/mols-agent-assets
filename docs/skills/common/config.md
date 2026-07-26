---
title: '에이전트 스킬 Config 권장 사항들'
description: '에이전트 스킬 Config 권장 사항들을 정리한 문서.'
tags:
    - 'agent-asset'
    - 'agent-skill'
---

# Skill Config — Common Recommendations

> [!IMPORTANT]
> **공통 권장**만. 스킬 정책이 더 구체하면 **스킬 우선**.

## Priority

| Priority | Path |
| :---: | :--- |
| 1 | `<workspace>/.configs/<config>` |
| 2 | `~/.agents/skills/<skill-name>/.configs/<config>` |
| 3 | default. (코드/스키마 내장) |

- `<config>`: 스킬이 정한 파일 경로. (`<skill-name>/<config-file>` or `<skill-name>.<ext>`)

## Optional override

> [!WARNING]
>
> - 에이전트 워크플로우로는 컨텍스트 오염이 된다.
> - 스크립트 위주의 스킬에서만 사용해야한다.
> - 에이전트 스킬에 스크립트는 위험할 수 있다. 트레이드 오프를 잘 고려해야한다.

스킬이 지원할 때만. 위에서 고른 base config에, 스킬이 정한 방식(주로 스크립트)으로 덮어쓴다.

권장 소스: `<target_folder>/.configs/<config>` (작업 대상 루트). target 없거나 project와 같으면 생략.
