# Working

이 문서는 에이전트 주도의 현재 작업 기준선이다. 작업 로그가 아니라 다음 개선에 필요한 현재 상태만 유지한다.

## Current State

- 상태: initial release candidate
- 핵심 모드: create, review-and-improve, tune
- 권위 구조: user instruction → DIRECTIVE → WORKING → implementation → upstream conventions
- 패키징: `docs/` 포함
- 개선 루프 기본 상한: 3회

## Current Structure

- `SKILL.md`: 핵심 워크플로와 모드
- `docs/DIRECTIVE.md`: 인간 기준선
- `docs/WORKING.md`: 에이전트 기준선
- `references/upstream-sources.md`: 공식 비교 출처
- `references/quality-model.md`: 전체 품질 검증 기준
- `references/platform-compatibility.md`: 멀티환경 분리 원칙
- `scripts/init_skill.py`: 새 스킬 최소 구조 생성
- `scripts/validate_skill.py`: 구조·frontmatter·링크 정적 검증
- `scripts/package_skill.py`: `docs/` 포함 ZIP 생성
- `assets/templates/`: 대상 스킬 필수 문서 템플릿
- `evals/cases.json`: 대표 회귀 사례

## Validation

- 구조 검증: PASS — 필수 파일, frontmatter, 상대 링크 검사
- 자체 패키징 검증: PASS — `docs/` 포함 ZIP 생성
- 생성 smoke test: PASS — 샘플 스킬 초기화·검증·패키징
- 필수 문서 누락 negative test: PASS — 검증 실패 확인
- 의미 검토: OpenAI·Microsoft·Anthropic의 공통 원칙과 벤더 전용 규칙을 분리함

## Promotion Candidates

현재 없음.

## Blockers

현재 없음.
