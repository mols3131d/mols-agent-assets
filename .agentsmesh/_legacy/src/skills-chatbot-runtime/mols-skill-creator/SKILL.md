---
name: mols-skill-creator
description: Create, review, directly improve, validate, and adapt AI agent skills across OpenAI, Microsoft/GitHub Copilot, Anthropic/Claude, and other compatible environments. Use when creating a new skill, editing or restructuring an existing SKILL.md, repairing degraded intent, tuning a skill for a project or agent runtime, comparing upstream skill-creator patterns, or running an automatic review-fix-revalidate loop.
---

# Mols Skill Creator

기존 스킬 개선을 우선하고, 필요하면 새 스킬을 생성한다. 공식·권위 있는 최신 자료를 근거로 구조를 재구성하되 특정 벤더의 관례를 범용 규칙으로 오인하지 않는다.

## Authority

대상 Skill source package를 수정할 때 다음 우선순위를 적용한다.

1. 사용자의 현재 명시적 지시
1. `.docs/baseline/*`의 durable preservation baseline
1. `.docs/WORKING.md` 같은 현재 maintainer state
1. 현재 `SKILL.md`와 runtime resources
1. 외부 참고 구현과 일반 관례

`.docs/`는 **non-runtime maintainer surface**다. 대상 Skill runtime이 이 파일을 읽어야 정상 동작하도록 설계하지 않는다.

Directory-based source package에서는 다음 관행을 사용한다.

- `.docs/baseline/`: 본래 purpose/essence, requirements, invariants, major decisions, recovery directives
- `.docs/WORKING.md`: 필요할 때만 두는 mutable maintainer state
- `references/`, `scripts/`, `assets/`: runtime에서 실제 필요할 때 사용하는 non-dot resources

`DIRECTIVE.md`, `intent.md`, `requirements.md`, `decisions.md`는 baseline의 예시 파일명이지 필수 schema가 아니다. 기존 package에 명확한 baseline이 있다면 그것을 존중한다. Flat single-file Skill에는 내부 `.docs/`를 강제하지 않는다.

## Workflow

### Understand

새 Skill이면 목적, 주요 사용자, 실행 환경, 핵심 산출물과 실제 사용 예를 파악한다. 정보가 충분하면 질문을 반복하지 않는다.

기존 directory-based Skill이면 먼저 source maintenance context와 runtime context를 구분한다.

1. `.docs/baseline/*`가 있으면 본래 목적·요구사항·결정사항을 확인한다.
1. `.docs/WORKING.md`가 있으면 현재 maintainer state를 확인한다.
1. `SKILL.md`를 읽는다.
1. `SKILL.md`가 실제로 참조하는 `references/`, `scripts/`, `assets/`와 다른 runtime resources를 필요한 만큼 읽는다.

그 후 현재 동작, 핵심 의도, 문제, 환경 의존성을 요약한다. Dot directory가 없다는 이유만으로 새 maintenance hierarchy를 만들 필요는 없다.

### Research

외부 사실이나 최신 플랫폼 규칙이 결과에 영향을 주면 공식 문서와 1차 자료를 확인한다. 기본 비교 기준은 `references/upstream-sources.md`를 사용한다.

- 공통 원칙과 벤더 전용 규칙을 분리한다.
- 공식 예제를 그대로 합성하지 말고 대상 목적에 맞게 재구성한다.
- 출처가 오래됐거나 충돌하면 최신성·범위·환경을 명시한다.

### Design

필요한 surface만 설계한다.

- `SKILL.md`: trigger, core contract, routing
- `references/`: runtime에서 필요할 때만 읽는 상세 지식
- `scripts/`: runtime에서 반복되거나 결정론적이어야 하는 작업
- `assets/`: runtime 결과에 복사·변형할 템플릿과 자원
- `.docs/`: non-runtime human/maintainer documentation
- `.docs/baseline/`: durable preservation/recovery baseline
- `.evals/`, `.tests/`: non-runtime evaluation/development material로 사용할 수 있음

**Dot-prefixed directory(`.*`)는 non-runtime surface**라는 repository-local convention을 지킨다. 실행 중 필요한 문서를 `.docs/`로 보내지 않는다. 그런 정보는 `SKILL.md` 또는 `references/` 같은 runtime surface가 소유한다.

자유도는 작업의 취약성에 맞춘다. 다양한 해법이 유효하면 원칙과 판단 기준을 주고, 오류 비용이 크면 검증된 스크립트와 명시적 제약을 제공한다.

### Implement

승인을 기다리지 않고 대상 파일을 직접 수정한다.

- 핵심 절차는 명령형으로 작성한다.
- frontmatter의 `description`에 기능과 구체적 trigger를 함께 쓴다.
- `SKILL.md`에는 자주 필요한 경로만 남기고 세부 runtime context는 직접 링크된 reference로 분리한다.
- 동일한 정보는 가능한 한 한 곳에서 authoritative하게 소유한다.
- 새 directory-based Skill 생성 시 `scripts/init_skill.py` 또는 `assets/templates/`를 활용할 수 있다.
- 대상의 고유한 구조·환경·사용자 지시는 공식 예제보다 우선한다.
- 기존 `docs/`가 있으면 각 파일이 runtime-required인지 maintainer-only인지 먼저 분류한 뒤, runtime material은 `references/` 등으로, maintainer material은 `.docs/`로 이동한다.

### Validate

수정 후 전체 품질을 검증한다.

1. `.docs/baseline/*`가 존재하면 본래 목적·요구사항·불변조건·결정사항 보존
1. trigger 정확도와 누락·과활성 위험
1. 실행 가능성, 도구·경로·명령의 현실성
1. 구조와 progressive disclosure
1. KISS, DRY, 불필요한 토큰 비용
1. 파일 간 용어·규칙·링크 일관성
1. 대상 환경 호환성과 벤더 종속성 격리
1. 기존 유효 기능의 회귀 여부
1. 보안과 사용자 기대의 일치
1. runtime-required resource가 dot directory에 숨어 있지 않은지 확인
1. runtime packaging에서 dot directory가 제외되는지 확인

`python scripts/validate_skill.py <target-skill>`을 실행할 수 있으면 실행한다. 스크립트 검증은 의미 검증을 대체하지 않는다.

### Improve Loop

검증 실패 시 원인을 진단하고 자동 수정한 뒤 재검증한다.

- 기본 최대 반복: 3회
- 같은 실패가 반복되면 접근 방식을 바꾼다.
- 외부 의존성, 권한 부족, 상충하는 인간 지시처럼 자동 해결할 수 없는 문제만 blocked로 남긴다.
- 통과 기준을 낮춰 성공으로 꾸미지 않는다.

### Record

`.docs/WORKING.md`가 해당 package의 관행으로 사용되고 현재 작업 상태를 보전할 가치가 있을 때만 갱신한다.

유지할 수 있는 내용:

- 현재 해석과 구조
- 발견된 주요 문제
- 적용한 핵심 변경
- 검증 결과와 남은 blocker
- baseline 승격 후보

삭제 후보:

- 단순 작업 로그
- 이미 무효화된 임시 판단
- 반복되는 과거 설명
- 복구·재검토 가치가 불명확한 기록

본래 목적·요구사항·결정사항을 의도적으로 바꾸지 않았다면 `.docs/baseline/*`는 변경하지 않는다. 변경이 필요하면 사용자의 명시적 지시와 기존 authority를 확인한다.

### Package

Runtime package에는 **dot-prefixed directory를 포함하지 않는다.** `.docs/`, `.evals/`, `.tests/` 등은 source/maintenance surface이며 runtime payload가 아니다.

`python scripts/package_skill.py <target-skill> --output <directory>`를 사용할 수 있다. 패키징 결과에 runtime-required `SKILL.md`, references/scripts/assets 등은 포함하고 non-runtime dot directory와 cache/temporary files는 제외한다.

## Modes

### Create

새 디렉터리를 만들고 최소 구조를 초기화한다. 실제 필요가 확인된 runtime resource만 추가한다. Directory-based source package의 initializer는 `.docs/baseline/`과 optional maintainer state를 만들 수 있지만 이는 runtime bundle과 분리한다.

### Review and Improve

기존 Skill의 의도와 동작을 분석하고 직접 수정한다. 변경 전보다 나아졌다는 근거를 평가 사례, 정적 검증, 대표 실행 또는 명시적 품질 비교로 남긴다.

### Tune

프로젝트·에이전트·플랫폼 제약을 조사하고 공통 코어와 환경별 adapter를 분리한다. 환경 전용 규칙을 전체 Skill의 불변 조건으로 승격하지 않는다.

## References

- 공식 비교 기준과 원문 링크: `references/upstream-sources.md`
- 전체 품질 판단 기준: `references/quality-model.md`
- 멀티환경 튜닝 원칙: `references/platform-compatibility.md`
- 대표 평가 사례가 source package에 있다면 non-runtime eval surface로 취급한다.
- `https://github.com/microsoft/skills/tree/main/.github/skills/skill-creator`를 비교 참고한다.

## Output

기본 응답은 수정 결과, 검증 상태, 주요 변경, blocker, 생성된 파일 경로만 간결하게 제시한다. 긴 분석은 필요한 source maintenance 자산에 기록하고 채팅에 반복하지 않는다.
