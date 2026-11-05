---
title: Rulesync
description: Rulesync 명령·설정·target 지원을 자체 설명 대신 저장소에서 사용하는 공식 Skill과 upstream 문서에서 확인할 때 사용합니다.
---

# Rulesync

Rulesync의 명령, 설정, 파일 형식과 target 동작은 이 문서에 재작성하지 않습니다. 사용법은 이 저장소가 외부 dependency로 사용하는 **[공식 Rulesync Skill](https://github.com/dyoshikawa/rulesync/blob/main/skills/rulesync/SKILL.md)**과 해당 버전의 공식 문서를 따릅니다.

## 사용법 참조

- **Agent:** 네이티브 Skill 탐색에서 `rulesync`를 선택합니다. 발견할 수 없다면 [저장소 Skill route](../../../.agents/route/ROUTE.md)를 따릅니다. 실제 의존성 ref는 [root 설정](../../../rulesync.jsonc)과 [lock](../../../rulesync.lock)에서 확인합니다.
- **CLI 문서:** 공식 Skill이 안내하는 설치된 CLI의 `rulesync docs`를 사용합니다. 웹에서는 [공식 문서](https://rulesync.dyoshikawa.com/)와 [릴리스](https://github.com/dyoshikawa/rulesync/releases)를 확인합니다.

## 이 저장소의 고유 사항

- **버전·설치·인증·검증 진입점:** [프로젝트 Rulesync 운영 안내](../../tools/rulesync.md)
- **작성 원본 선택 및 배치:** [작성 원본과 권한](../source-authority.md)

설정값, CLI 옵션 및 target 지원 범위는 실제 설정과 upstream에서 확인합니다. 이 문서는 별도의 Rulesync 규격이나 운영 절차를 정의하지 않습니다.
