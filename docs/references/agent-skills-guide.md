# 좋은 Agent Skill 설계 가이드

Agent Skill은 **특정 영역의 지식과 반복 가능한 절차를 에이전트가 필요할 때 불러 쓰게 만드는 경량 패키지**다. 좋은 Skill은 많은 정보를 담은 문서가 아니라, 올바른 요청에서 활성화되어 필요한 지침만 제공하고 결과를 검증하는 실행 단위다.

## 1. 핵심 원리

```text
Discovery              Activation               Execution
name + description  →  선택된 SKILL.md 로드  →  필요한 resource만 사용
```

이 **Progressive Disclosure** 구조는 초기 context와 token을 줄이고 관련 없는 지침의 간섭을 막는다.

- Discovery: 모든 Skill의 `name`, `description`만 노출
- Activation: 요청과 일치하는 Skill의 `SKILL.md` 로드
- Execution: 필요한 `references/`, `scripts/`, `assets/`만 사용

Skill은 반복 작업, 프로젝트 고유 규칙·API·schema, 엄격한 결과 형식, 비자명한 예외가 있을 때 만든다. 단순한 일회성 요청이나 모델이 이미 잘하는 일반 작업에는 만들지 않는다.

## 2. 좋은 Skill의 조건

| 기준 | 좋은 상태 |
| --- | --- |
| Scope | 하나의 일관된 영역과 사용자 목적을 다룬다. |
| Trigger | 필요한 요청에서 켜지고 유사한 다른 요청에서는 꺼진다. |
| Knowledge | 실제 trace, 교정, runbook, schema, 장애에서 추출했다. |
| Workflow | 기본 경로, 분기, 중단 조건이 구체적이다. |
| Context | 공통 핵심만 항상 읽고 세부 정보는 조건부로 읽는다. |
| Control | 위험한 단계만 엄격히 통제하고 나머지는 재량을 준다. |
| Validation | 완료 조건과 실패 복구 방법이 있다. |

> 이 지침이 없어도 에이전트가 안정적으로 잘한다면 삭제한다.

## 3. 기본 구조와 규격

```text
my-skill/
├── SKILL.md          # 필수: metadata, workflow, 제약, routing
├── references/       # 상세 절차, API, schema, 예외
├── scripts/          # 반복적이고 결정적인 실행 로직
└── assets/           # template, sample, 출력 재료
```

```markdown
---
name: pdf-processing
description: Extract and merge PDF content. Use for structured extraction or combined PDF output. Do not use for general document writing.
---

# PDF Processing

## Workflow

1. Inspect inputs and the requested output.
2. Select the smallest matching operation.
3. Load only resources required by that operation.
4. Execute, validate, and report the output path.

## Validation

- Confirm every requested input was processed.
- Confirm the output opens and contains the expected content.
```

필수 metadata:

- `name`: 1–64자, `a-z0-9-`, 앞뒤·연속 `-` 금지, 폴더명과 일치
- `description`: 1–1024자, capability, 사용 조건, 주요 제외 조건 명시

선택 metadata는 `license`, `compatibility`(최대 500자), `metadata`, `allowed-tools`가 있다. 모든 경로는 Skill root 기준 상대 경로를 사용한다. `SKILL.md`는 핵심 지침에 집중하고 500 lines, 약 5,000 tokens 미만을 권장한다.

## 4. 만드는 순서

### 1) 실제 지식 수집

성공한 작업 순서, 사용자 교정, 실제 patch, runbook, schema, post-mortem에서 반복되는 판단과 실패 지점을 찾는다. 일반 지식을 다시 설명하지 않는다.

### 2) 경계 정의

다음에 한 문장씩 답한다.

- 어떤 사용자 결과를 만드는가?
- 언제 사용하고 언제 사용하지 않는가?
- 독립된 trigger, permission, 배포 주기가 필요한 기능이 섞였는가?

공통 trigger와 workflow를 공유하면 하나의 Skill 안에서 route한다. 목적이나 권한이 다르면 Skill을 나눈다.

### 3) `description` 작성

활성화 전에는 `description`만 보인다. 내부 구현이 아니라 사용자 intent를 쓴다.

```text
Use this skill when [사용자 목적과 상황].
Do not use it when [겹치기 쉬운 제외 조건].
```

정확한 keyword가 없는 간접 요청도 포괄하되, 단어가 겹치는 near-miss는 제외한다. `Helps with data`처럼 넓고 모호한 표현은 피한다.

### 4) 실행 가능한 workflow 작성

`SKILL.md`에는 모든 실행에 공통인 내용만 둔다.

- 기본 실행 순서와 입력 요구사항
- 중요한 분기와 중단 조건
- 반드시 지킬 constraint와 비자명한 gotcha
- 실패 복구와 완료 validation
- resource를 읽거나 script를 실행할 정확한 조건

```markdown
If the API returns a non-200 response, read `references/api-errors.md`.
For destructive migrations, read `references/migration-safety.md` and produce a dry-run plan before mutation.
```

`필요하면 references를 확인한다`처럼 load condition이 없는 지시는 쓰지 않는다.

### 5) Resource 분리

| 내용 | 위치 |
| --- | --- |
| 모든 실행의 공통 workflow와 제약 | `SKILL.md` |
| 긴 설명, domain 절차, API, schema | `references/` |
| 반복 parsing, 변환, 검증 | `scripts/` |
| template, sample, image | `assets/` |
| 한 번이면 끝나는 단순 명령 | `SKILL.md`에 직접 작성 |

파일을 나눠도 시작할 때 전부 읽으면 Progressive Disclosure가 아니다. 각 resource의 load condition을 `SKILL.md`에 명시한다.

### 6) 통제 수준 조정

- 방법이 다양함: 목표와 완료 조건만 고정
- 선호 경로가 있음: 기본 절차와 parameter 제공
- 파괴적·보안·순서 의존 작업: 명령, 순서, 승인, 검증을 엄격히 고정

여러 선택지를 나열하기보다 안전한 기본 경로 하나를 제공한다.

## 5. Script 설계

반복적이거나 복잡한 로직은 Markdown으로 설명하지 말고 검증된 script로 만든다.

- dependency version과 runtime을 고정한다.
- interactive prompt 없이 flag, stdin, env var로 입력받는다.
- 누락되거나 모호한 입력은 즉시 거부한다.
- `--help`에 목적, 인자, 기본값, 예시, exit code를 담는다.
- stdout에는 JSON/CSV 결과, stderr에는 log와 warning을 출력한다.
- 재실행 가능한 idempotent 동작을 선호한다.
- mutation에는 `--dry-run`, 파괴적 작업에는 `--force`를 제공한다.
- 오류별 exit code와 다음 조치를 제시하고 출력 크기를 제한한다.

## 6. 검증과 개선

### Trigger 검증

1. 실제 사용자 문장으로 `query`, `should_trigger` 쌍을 만든다.
2. Positive에는 keyword 없는 간접 요청을 넣는다.
3. Negative에는 단어는 겹치지만 목적이 다른 near-miss를 넣는다.
4. typo, 실제 경로, 구어체, 긴 맥락을 포함한다.
5. 고정된 60% train / 40% validation으로 나눈다.
6. 비결정성을 고려해 query당 3회 이상 실행한다.
7. 약 5회 이내 개선 후 validation이 가장 좋은 버전을 고른다.
8. 새로운 holdout query로 최종 확인한다.

```text
trigger_rate = 활성화 횟수 / 전체 실행 횟수
```

False Negative는 scope를 넓힐 신호이고 False Positive는 경계를 좁힐 신호다. 실패 문구를 `description`에 그대로 복사하지 말고 실패한 intent를 반영한다.

### 실행 검증

실제 요청에 Skill을 적용하고 최종 답변뿐 아니라 전체 trace를 본다.

- 반복 재시도 → 모호한 단계와 오류 복구 수정
- 불필요한 파일 로드 → resource routing 구체화
- 결과 편차 → template, script, validation 강화
- 불필요한 지침 → 삭제

## 7. 피해야 할 설계

- 일반 지식을 장황하게 반복한다.
- 모든 domain과 예시를 거대한 `SKILL.md`에 넣는다.
- 시작할 때 `references/` 전체를 읽는다.
- resource의 존재만 알리고 읽을 조건은 쓰지 않는다.
- 선택지만 나열하고 기본 경로를 정하지 않는다.
- 검증 없이 파일 생성이나 명령 실행으로 완료 처리한다.
- 실제 실행 없이 문서 검토만으로 품질을 판단한다.

## 8. 완성 체크리스트

- [ ] 하나의 일관된 사용자 목적을 다룬다.
- [ ] `name`, 폴더명, metadata 규격이 맞는다.
- [ ] `description`만으로 사용·제외 조건을 판단할 수 있다.
- [ ] 실제 작업과 실패 사례에서 지식을 추출했다.
- [ ] 기본 workflow, 분기, 중단, 복구, 완료 조건이 명확하다.
- [ ] 위험한 단계의 순서와 승인 조건을 엄격히 정의했다.
- [ ] 상세 정보와 반복 로직을 적절한 resource로 분리했다.
- [ ] 각 resource의 load condition과 상대 경로가 명확하다.
- [ ] script가 non-interactive, idempotent하며 안전한 기본값을 가진다.
- [ ] Positive, near-miss Negative, holdout query로 trigger를 검증했다.
- [ ] 실제 실행 trace에서 불필요한 지침과 retry 원인을 제거했다.
- [ ] validator와 Skill 고유 validation을 통과했다.

## 참고 자료

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
