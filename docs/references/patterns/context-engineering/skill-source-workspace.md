---
description: Skill runtime source와 maintainer docs·tests·eval context를 한 source workspace에서 함께 보존·이동해야 할 때 참고하는 pattern으로, runtime surface와 maintainer-only surface의 경계를 다룹니다.
---

# Skill Source Workspace

일반 project repository에서 Skill runtime source와 maintainer context를 함께 관리하여 **재사용·이동·조정하기 쉬운 source workspace**를 구성하는 패턴입니다.

## Purpose

Skill runtime source와 유지보수·검증·평가 context를 한 Skill 경계 안에 함께 두어, directory 전체를 옮기거나 수정할 때 필요한 context도 같이 보존합니다.

## Core

- Runtime에 필요한 source와 maintainer-only surface를 같은 Skill directory 안에서 구분합니다.
- `README.md`는 Skill의 최소 entrypoint/router로 사용하고 세부 내용을 중복 소유하지 않습니다.
- Maintainer-only surface의 존재나 부재가 Skill runtime semantics를 바꾸지 않아야 합니다.

## Typical Layout

```text
<skill>/
├─ SKILL.md
├─ references/
├─ scripts/
├─ assets/
├─ README.md
├─ .docs/
├─ .tests/
└─ .eval/
```

`references/`, `scripts/`, `assets/`와 dot-prefixed directory는 필요한 것만 둘 수 있습니다. `.docs/`, `.tests/`, `.eval/`은 runtime과 분리하고 싶은 development / maintenance / evaluation surface의 대표적인 선택지입니다.

`README.md`는 보통 다음처럼 최소한의 entry 기능만 맡습니다.

```md
# <skill-name>

- Runtime → `SKILL.md`
- Maintainer docs → `.docs/`
- Tests → `.tests/`
- Evals → `.eval/`
```

## Options

- 작은 Skill은 사용하지 않는 directory를 생략할 수 있습니다.
- 필요하면 maintainer-only surface를 추가하거나 이름을 project 관행에 맞게 조정할 수 있습니다.
- 많은 Agent Asset을 중앙 관리하는 repository에서는 docs/tests/evals를 repository-level surface로 분리하는 방식이 더 적합할 수 있습니다.

## Considerations

- Dot-prefix는 packaging exclusion을 자동 보장하지 않습니다. 배포 도구나 workflow가 maintainer-only surface를 어떻게 다루는지 확인합니다.
- README가 커져 별도 설계·운영 문서를 대신하기 시작하면 entrypoint 책임을 넘어선 것인지 검토합니다.
- 이 패턴의 핵심은 고정된 directory 목록이 아니라 **Skill과 함께 이동 가능한 runtime/maintainer context의 경계**입니다.
- Portability는 이 패턴이 얻을 수 있는 결과 중 하나이지 Skill의 분류나 이 패턴의 적용 조건이 아닙니다.

## Boundary

이 패턴은 `.docs/`, `.tests/`, `.eval/` 안의 구체적인 문서·테스트·평가 방식이나 packaging 규격 자체를 정의하지 않습니다.
