---
name: mols-skill-creator
description: Create, review, directly improve, validate, and adapt AI agent skills across OpenAI, Microsoft/GitHub Copilot, Anthropic/Claude, and other compatible environments. Use when creating a new skill, editing or restructuring an existing SKILL.md, repairing degraded intent, tuning a skill for a project or agent runtime, comparing upstream skill-creator patterns, or running an automatic review-fix-revalidate loop.
---

# Mols Skill Creator

기존 Skill 개선을 우선하고, 필요하면 새 Skill을 생성한다. 공식·권위 있는 최신 자료를
근거로 구조를 재구성하되 특정 벤더의 관례를 범용 규칙으로 오인하지 않는다.

## Authority

대상 Skill을 수정할 때 다음 우선순위를 적용한다.

1. 사용자의 현재 명시적 지시
1. 대상 프로젝트·repository의 현재 authority와 maintainer baseline
1. 현재 `./SKILL.md`와 runtime resources
1. 외부 참고 구현과 일반 관례

Maintainer docs는 runtime package contract가 아니다. 프로젝트가 별도 maintainer-doc
surface를 정의하면 그 위치와 authority를 따른다. 이 저장소에서는 필요할 때
`docs/skills/<skill-name>/`을 사용한다.

Directory-based Skill이라는 이유만으로 maintainer docs를 만들지 않는다. 다음과 같이
별도 문서가 실제 훼손·복구 위험을 줄일 때만 검토한다.

- source만으로 purpose, architecture 또는 중요 invariant를 복구하기 어렵다.
- 단순화·refactor에서 intent나 non-goal이 쉽게 훼손될 수 있다.
- durable decision, recovery, migration 또는 compatibility 지식이 필요하다.
- 별도 baseline이 장기 유지보수 비용을 의미 있게 낮춘다.

Runtime이 읽어야 하는 정보는 `./SKILL.md`, `.github/skills/mols-skill-creator/references/`, `.github/skills/mols-skill-creator/scripts/`, `.github/skills/mols-skill-creator/assets/` 등
실제 deployable surface가 소유한다.

## Workflow

### Understand

새 Skill이면 목적, 주요 사용자, 실행 환경, 핵심 산출물과 실제 사용 예를 파악한다.
정보가 충분하면 질문을 반복하지 않는다.

기존 Skill이면 먼저 source maintenance context와 runtime context를 구분한다.

1. 프로젝트가 특정 Skill의 maintainer docs 위치를 정의하고 해당 문서가 실제로 있으면 필요한 것만 읽는다.
1. `./SKILL.md`를 읽는다.
1. `./SKILL.md`가 실제로 참조하는 `.github/skills/mols-skill-creator/references/`, `.github/skills/mols-skill-creator/scripts/`, `.github/skills/mols-skill-creator/assets/`와 다른 runtime resources를 필요한 만큼 읽는다.

그 후 현재 동작, 핵심 의도, 문제, 환경 의존성을 요약한다. Maintainer docs가 없다는
이유만으로 새 documentation hierarchy를 만들지 않는다.

### Research

외부 사실이나 최신 플랫폼 규칙이 결과에 영향을 주면 공식 문서와 1차 자료를
확인한다. 기본 비교 기준은 `./references/upstream-sources.md`를 사용한다.

- 공통 원칙과 벤더 전용 규칙을 분리한다.
- 공식 예제를 그대로 합성하지 말고 대상 목적에 맞게 재구성한다.
- 출처가 오래됐거나 충돌하면 최신성·범위·환경을 명시한다.

### Design

필요한 surface만 설계한다.

- `./SKILL.md`: trigger, core contract, routing
- `.github/skills/mols-skill-creator/references/`: runtime에서 필요할 때만 읽는 상세 지식
- `.github/skills/mols-skill-creator/scripts/`: runtime에서 반복되거나 결정론적이어야 하는 작업
- `.github/skills/mols-skill-creator/assets/`, `templates/`: runtime 결과에 필요한 자원
- project maintainer docs: 복잡성·훼손 위험·durable decision·recovery 필요가 확인될 때만
- evals/tests: 검증 목적과 target contract가 있을 때만

Runtime package와 maintainer documentation을 분리한다. 유지보수 편의를 이유로 runtime
필수 지식을 외부 maintainer docs로 빼지 않고, 반대로 maintainer-only 문서를 runtime
package에 넣지 않는다.

자유도는 작업의 취약성에 맞춘다. 다양한 해법이 유효하면 원칙과 판단 기준을 주고,
오류 비용이 크면 검증된 스크립트와 명시적 제약을 제공한다.

### Implement

승인을 기다리지 않고 승인된 write boundary 안에서 대상 파일을 직접 수정한다.

- 핵심 절차는 명령형으로 작성한다.
- frontmatter의 `description`에 기능과 구체적 trigger를 함께 쓴다.
- `./SKILL.md`에는 자주 필요한 경로만 남기고 세부 runtime context는 직접 링크된 reference로 분리한다.
- 동일한 정보는 가능한 한 한 곳에서 authoritative하게 소유한다.
- 새 directory-based Skill 생성 시 `./scripts/init_skill.py` 또는 `.github/skills/mols-skill-creator/assets/templates/`를 활용할 수 있다.
- 대상의 고유한 구조·환경·사용자 지시는 공식 예제보다 우선한다.
- package 내부 human-facing 문서가 있으면 runtime-required인지 maintainer-only인지 먼저 분류한다. Runtime material은 package runtime surface에 남기고, maintainer material은 프로젝트가 정의한 선택적 docs surface로 이동할 수 있다.

### Validate

수정 후 전체 품질을 검증한다.

1. 존재하는 maintainer baseline의 purpose·requirements·invariants·decisions 보존
1. trigger 정확도와 누락·과활성 위험
1. 실행 가능성, 도구·경로·명령의 현실성
1. 구조와 progressive disclosure
1. KISS, DRY, 불필요한 토큰 비용
1. 파일 간 용어·규칙·링크 일관성
1. 대상 환경 호환성과 벤더 종속성 격리
1. 기존 유효 기능의 회귀 여부
1. 보안과 사용자 기대의 일치
1. runtime-required resource가 maintainer-only surface에 의존하지 않는지 확인
1. maintainer-only docs가 runtime payload에 불필요하게 포함되지 않는지 확인

`python ./scripts/validate_skill.py <target-skill>`을 실행할 수 있으면 실행한다. 스크립트
검증은 의미 검증을 대체하지 않는다.

### Improve Loop

검증 실패 시 원인을 진단하고 자동 수정한 뒤 재검증한다.

- 기본 최대 반복: 3회
- 같은 실패가 반복되면 접근 방식을 바꾼다.
- 외부 의존성, 권한 부족, 상충하는 인간 지시처럼 자동 해결할 수 없는 문제만 blocked로 남긴다.
- 통과 기준을 낮춰 성공으로 꾸미지 않는다.

### Record

프로젝트가 maintainer state 문서를 실제로 사용하고 현재 상태를 보전할 가치가 있을 때만
갱신한다. 문서가 없으면 작업했다는 이유만으로 새로 만들지 않는다.

유지할 수 있는 내용:

- 현재 해석과 구조
- 발견된 주요 문제
- 적용한 핵심 변경
- 검증 결과와 남은 blocker
- durable baseline 승격 후보

삭제 후보:

- 단순 작업 로그
- 이미 무효화된 임시 판단
- 반복되는 과거 설명
- 복구·재검토 가치가 불명확한 기록

본래 목적·요구사항·결정사항을 의도적으로 바꾸지 않았다면 baseline을 기계적으로
갱신하지 않는다. 변경이 필요하면 사용자의 명시적 지시와 기존 authority를 확인한다.

### Package

Runtime package에는 실행에 필요한 surface만 포함한다. Cache, VCS metadata, 임시 파일,
project-external maintainer docs는 runtime payload가 아니다.

`python ./scripts/package_skill.py <target-skill> --output <directory>`를 사용할 수 있다.
패키징 결과에 runtime-required `./SKILL.md`, references/scripts/assets 등을 포함하고
non-runtime cache/temporary surface는 제외한다.

## Modes

### Create

새 Skill을 최소 구조로 초기화한다. 기본 initializer는 runtime `./SKILL.md`만 만들고,
실제 필요가 확인된 runtime resource를 이후 추가한다. Maintainer docs는 프로젝트 기준과
복잡성·훼손 위험을 확인한 뒤 별도로 만들며 기본 scaffold가 아니다.

### Review and Improve

기존 Skill의 의도와 동작을 분석하고 직접 수정한다. 변경 전보다 나아졌다는 근거를
평가 사례, 정적 검증, 대표 실행 또는 명시적 품질 비교로 남긴다.

### Tune

프로젝트·에이전트·플랫폼 제약을 조사하고 공통 코어와 환경별 adapter를 분리한다.
환경 전용 규칙을 전체 Skill의 불변 조건으로 승격하지 않는다.

## References

- 공식 비교 기준과 원문 링크: `./references/upstream-sources.md`
- 전체 품질 판단 기준: `./references/quality-model.md`
- 멀티환경 튜닝 원칙: `./references/platform-compatibility.md`
- 대표 평가 사례가 source package에 있다면 non-runtime eval surface로 취급한다.
- `https://github.com/microsoft/skills/tree/main/.github/skills/skill-creator`를 비교 참고한다.

## Output

기본 응답은 수정 결과, 검증 상태, 주요 변경, blocker, 생성된 파일 경로만 간결하게
제시한다. 긴 분석은 필요한 maintainer surface가 실제로 있을 때만 기록하고 채팅에
반복하지 않는다.