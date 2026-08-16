# Intent

이 문서는 `rulesync-agent-assets`가 시간이 지나도 보존해야 하는 목적과 범위를 정의한다.
Normative invariant는 `requirements.md`, 설계 이유와 재검토 조건은 `decisions.md`가 소유한다.
Rulesync CLI 세부사항이나 특정 프로젝트의 현재 파일 배치는 이 문서의 관심사가 아니다.

## Purpose

하나의 명확한 source authority를 유지하면서 agent customization asset을 여러 coding-agent
harness에서 사용할 수 있게 한다. 변환 mechanics는 Rulesync에 위임하고, Skill은 어떤
source를 어떤 범위와 안전 조건 아래 재사용·생성·이식할지를 조정한다.

## Goals

1. Rulesync canonical source에서 여러 harness로 fan-out하는 경로와 하나의 native harness를
   source로 유지하며 다른 harness로 bridge하는 경로를 모두 first-class로 지원한다.
2. Target이 기존 source를 실제로 발견하고 필요한 의미를 지원한다는 근거가 있으면 불필요한
   변환과 중복 asset 생성을 피한다.
3. Caller와 repository가 정한 source authority를 보존하고, 요청된 target과 asset 범위만
   최소한으로 다룬다.
4. 파일 생성 성공과 runtime semantic compatibility를 구분하고 확인된 gap과 validation
   evidence를 드러낸다.
5. Harness별 parsing, mapping과 serialization은 Rulesync upstream에 맡기고 경쟁 compiler를
   중복 구현하지 않는다.

## Scope

이 Skill의 범위는 Rulesync가 지원하는 cross-harness agent customization asset의 재사용,
생성, 변환과 그 결과 검증이다. 대표 asset category는 rules, subagents, skills, commands,
hooks, permissions, checks와 MCP configuration이다.

Project-local 작업을 기본 경계로 본다. User-global configuration은 caller가 명시적으로
요구한 별도 범위다.

이 Skill은 orchestration layer다. Source resolution, route selection, target scope, mutation
safety, compatibility evidence와 validation을 소유한다. Format parsing, normalization,
harness mapping과 serialization은 Rulesync가 소유한다.

## Non-goals

- 모든 harness를 포괄하는 새 canonical schema를 발명하지 않는다.
- Rulesync의 parser, serializer 또는 compatibility matrix를 복제하지 않는다.
- 모든 repository에 `.rulesync/`를 source of truth로 강제하지 않는다.
- native harness source를 canonical workflow로 자동 migration하지 않는다.
- 경로나 포맷 유사성만으로 direct reuse의 호환성을 추정하지 않는다.
- target의 표현력 차이를 숨기거나 완전 호환으로 과장하지 않는다.
- 변환을 이유로 source asset을 몰래 rename, copy, relocate 또는 normalize하지 않는다.
- install, upgrade, cleanup, deletion 또는 global configuration mutation을 부수 효과로
  수행하지 않는다.
- 특정 프로젝트의 source preference나 파일 배치를 generic Skill의 본질로 승격하지 않는다.

이 목적이나 범위를 의도적으로 바꾸는 수정은 단순 refactor가 아니다. 같은 변경에서
requirements와 decisions를 함께 검토하고 contract change로 취급한다.
