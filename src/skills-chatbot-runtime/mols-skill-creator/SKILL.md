---
name: mols-skill-creator
description: Create, review, directly improve, validate, and adapt AI agent skills across OpenAI, Microsoft/GitHub Copilot, Anthropic/Claude, and other compatible environments. Use when creating a new skill, editing or restructuring an existing SKILL.md, repairing degraded intent, tuning a skill for a project or agent runtime, comparing upstream skill-creator patterns, or running an automatic review-fix-revalidate loop.
---

# Mols Skill Creator

기존 스킬 개선을 우선하고, 필요하면 새 스킬을 생성한다. 공식·권위 있는 최신 자료를 근거로 구조를 재구성하되 특정 벤더의 관례를 범용 규칙으로 오인하지 않는다.

## Authority

작업 시작 시 대상 스킬의 파일을 확인하고 다음 우선순위를 적용한다.

1. 사용자의 현재 명시적 지시
1. `docs/DIRECTIVE.md`
1. `docs/WORKING.md`
1. 현재 `SKILL.md`와 부속 자산
1. 외부 참고 구현과 일반 관례

모든 대상 스킬에 `docs/DIRECTIVE.md`와 `docs/WORKING.md`를 둔다.

- `DIRECTIVE.md`: 인간 주도의 규범적 기준선이다. 사용자가 명시적으로 요청한 경우에만 수정한다.
- `WORKING.md`: 에이전트 주도의 현재 작업 기준선이다. 의미 있는 작업마다 정리해서 갱신한다.

충돌 시 상위 권위를 따른다. 해결할 수 없는 충돌은 숨기지 말고 `WORKING.md`에 기록한다.

## Workflow

### Understand

새 스킬이면 목적, 주요 사용자, 실행 환경, 핵심 산출물과 실제 사용 예를 파악한다. 정보가 충분하면 질문을 반복하지 않는다.

기존 스킬이면 먼저 다음을 읽는다.

1. `docs/DIRECTIVE.md`
1. `docs/WORKING.md`
1. `SKILL.md`
1. 직접 참조된 `references/`, `scripts/`, `assets/`, 평가 자산

그 후 현재 동작, 핵심 의도, 문제, 환경 의존성을 요약한다.

### Research

외부 사실이나 최신 플랫폼 규칙이 결과에 영향을 주면 공식 문서와 1차 자료를 확인한다. 기본 비교 기준은 `references/upstream-sources.md`를 사용한다.

- 공통 원칙과 벤더 전용 규칙을 분리한다.
- 공식 예제를 그대로 합성하지 말고 대상 목적에 맞게 재구성한다.
- 출처가 오래됐거나 충돌하면 최신성·범위·환경을 명시한다.

### Design

다음 기준으로 필요한 자산만 설계한다.

- `SKILL.md`: 트리거와 핵심 실행 흐름
- `references/`: 필요할 때만 읽을 상세 지식
- `scripts/`: 반복되거나 결정론적이어야 하는 작업
- `assets/`: 생성 결과에 복사·변형할 템플릿과 자원
- `docs/`: 인간 의도와 에이전트 작업 상태
- `evals/`: 대표 사용 사례와 회귀 기준

자유도는 작업의 취약성에 맞춘다. 다양한 해법이 유효하면 원칙과 판단 기준을 주고, 오류 비용이 크면 검증된 스크립트와 명시적 제약을 제공한다.

### Implement

승인을 기다리지 않고 대상 파일을 직접 수정한다.

- 핵심 절차는 명령형으로 작성한다.
- frontmatter의 `description`에 기능과 구체적 trigger를 함께 쓴다.
- `SKILL.md`에는 자주 필요한 경로만 남기고 세부 내용은 직접 링크된 reference로 분리한다.
- 동일한 정보는 한 곳에서만 소유한다.
- 새 스킬 생성 시 `scripts/init_skill.py` 또는 `assets/templates/`를 활용한다.
- 대상의 고유한 구조·환경·사용자 지시는 공식 예제보다 우선한다.

### Validate

수정 후 전체 품질을 검증한다.

1. `DIRECTIVE.md`의 목적·요구사항·불변 조건 보존
1. trigger 정확도와 누락·과활성 위험
1. 실행 가능성, 도구·경로·명령의 현실성
1. 구조와 progressive disclosure
1. KISS, DRY, 불필요한 토큰 비용
1. 파일 간 용어·규칙·링크 일관성
1. 대상 환경 호환성과 벤더 종속성 격리
1. 기존 유효 기능의 회귀 여부
1. 보안과 사용자 기대의 일치
1. 패키징 완전성 — `docs/` 포함

`python scripts/validate_skill.py <target-skill>`을 실행할 수 있으면 실행한다. 스크립트 검증은 의미 검증을 대체하지 않는다.

### Improve Loop

검증 실패 시 원인을 진단하고 자동 수정한 뒤 재검증한다.

- 기본 최대 반복: 3회
- 같은 실패가 반복되면 접근 방식을 바꾼다.
- 외부 의존성, 권한 부족, 상충하는 인간 지시처럼 자동 해결할 수 없는 문제만 blocked로 남긴다.
- 통과 기준을 낮춰 성공으로 꾸미지 않는다.

### Record

작업 종료 전 `docs/WORKING.md`를 현재 상태 중심으로 갱신한다.

유지:

- 현재 해석과 구조
- 발견된 주요 문제
- 적용한 핵심 변경
- 검증 결과와 남은 blocker
- `DIRECTIVE.md` 승격 후보

삭제:

- 단순 작업 로그
- 이미 무효화된 임시 판단
- 반복되는 과거 설명
- 복구·재검토 가치가 불명확한 기록

애매하면 삭제한다. 아카이브 가치가 명확한 주요 항목만 남긴다.

`DIRECTIVE.md`는 사용자 요청 없이 갱신하지 않는다. 변경이 필요하면 `WORKING.md`의 승격 후보로 제안한다.

### Package

완료된 스킬을 패키징할 때 `docs/`를 반드시 포함한다.

`python scripts/package_skill.py <target-skill> --output <directory>`를 사용할 수 있다. 캐시, 임시 파일, 기존 패키지는 제외한다.

## Modes

### Create

새 디렉터리를 만들고 최소 구조를 초기화한다. 실제 필요가 확인된 자산만 추가한다.

### Review and Improve

기존 스킬의 의도와 동작을 분석하고 직접 수정한다. 변경 전보다 나아졌다는 근거를 평가 사례, 정적 검증, 대표 실행 또는 명시적 품질 비교로 남긴다.

### Tune

프로젝트·에이전트·플랫폼 제약을 조사하고 공통 코어와 환경별 adapter를 분리한다. 환경 전용 규칙을 전체 스킬의 불변 조건으로 승격하지 않는다.

## References

- 공식 비교 기준과 원문 링크: `references/upstream-sources.md`
- 전체 품질 판단 기준: `references/quality-model.md`
- 멀티환경 튜닝 원칙: `references/platform-compatibility.md`
- 대표 평가 사례: `evals/cases.json`
- `https://github.com/microsoft/skills/tree/main/.github/skills/skill-creator` 반드시 이 스킬을 참고해라.

## Output

기본 응답은 수정 결과, 검증 상태, 주요 변경, blocker, 생성된 파일 경로만 간결하게 제시한다. 긴 분석은 스킬 자산에 기록하고 채팅에 반복하지 않는다.
