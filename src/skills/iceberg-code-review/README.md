# Iceberg Code Review

코드 리뷰 결과의 포맷을 정의하고, 템플릿과 검증 도구를 제공하는 Agent Skill입니다.

- 리뷰 대상과 목적은 외부 컨텍스트가 결정합니다.
- 코드 수정은 수행하지 않습니다.
- 결과는 Markdown 문서로 생성하고 검증합니다.

## Review Engines

- 코드 이해
- 코드 구현
- 코드 품질
- 코드 운영
- 코드 위험

모든 결과는 `priority`(`p0`–`p4`)로 처리 우선순위를 표현합니다.

## Structure

| 경로 | 역할 |
| :--- | :--- |
| `SKILL.md` | 실행 규칙과 참조 라우팅 |
| `references/` | 워크플로우, 리뷰 엔진, 명령 문서 |
| `assets/templates/` | 요약·상세 결과 템플릿 |
| `scripts/` | 생성·검증 스크립트 |
