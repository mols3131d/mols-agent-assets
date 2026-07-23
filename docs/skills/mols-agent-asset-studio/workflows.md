# Mols Agent Asset Studio Workflow Modules

`mols-agent-asset-studio`는 root `INDEX.csv`에서 사용자 intent를 분류하고, 선택된 `workflows/*.md`만 읽는다. 이 파일은 기존 경로 호환을 위해 `sub-skills.md`라는 이름을 유지하지만, 현재 구조의 정확한 용어는 **Workflow Module**이다.

```text
mols-agent-asset-studio/
├── SKILL.md
├── INDEX.csv
└── workflows/
    ├── agent-skill.md
    ├── asset-naming.md
    ├── compress.md
    └── routerize-skills.md
```

## Routing 방식

`INDEX.csv` schema:

```csv
id,use_when,avoid_when,entrypoint
```

Router는 다음 순서로 동작한다.

1. 사용자 요청의 outcome, asset type, target path, constraint를 확인한다.
2. `avoid_when`과 일치하는 route를 제거한다.
3. `use_when`을 기준으로 요청을 충족하는 최소 route set을 선택한다.
4. 선택된 exact `entrypoint`만 읽는다.
5. Workflow가 요구하는 reference와 script만 추가로 사용한다.
6. 선택된 모든 Workflow의 validation을 통과한 뒤 완료한다.

Keyword 중복만으로 route하지 않으며 `workflows/`를 scan해 module을 찾지 않는다. 여러 route는 요청이 실제로 여러 작업을 포함할 때만 선택한다.

## Route 요약

| Route | 사용 조건 | 제외 조건 | Entrypoint |
| --- | --- | --- | --- |
| `agent-skill` | Skill 생성, 개선, 평가, 검증 | Naming-only, compression-only, 여러 Skill 통합 | `workflows/agent-skill.md` |
| `asset-naming` | 자산 이름 제안·검증·변경이 주 작업 | 이름 변경이 부수적인 content 작업 | `workflows/asset-naming.md` |
| `compress` | 명시된 단일 agent asset 압축 | 광범위한 디렉터리, code formatting, target 없음 | `workflows/compress.md` |
| `routerize-skills` | 관련된 여러 기존 Skill 통합 | 단일 일반 Skill 생성, naming-only, 무관한 Skill 편집 | `workflows/routerize-skills.md` |

## `agent-skill`

하나의 Skill을 생성, 개선, 평가, 검증한다.

주요 절차:

1. Create, Improve, Evaluate mode를 결정한다.
2. `rg`, `wc`, scaffold, validator 같은 결정적 command를 먼저 사용한다.
3. Skill의 job, trigger, output, near-miss exclusion을 정의한다.
4. 필요한 최소 구조만 사용한다.
5. 공통 workflow는 `SKILL.md`, 상세 지식은 `references/`, 반복 로직은 `scripts/`, 출력 재료는 `assets/`에 둔다.
6. 검증과 수정을 반복한다.

핵심 validation:

- Frontmatter `name`, `description`과 폴더명 일치
- 올바른 요청과 near-miss에 대한 activation boundary
- 500 lines 이하의 집중된 `SKILL.md`
- 모든 resource 경로와 script 실행 조건 확인
- 중복 규칙, 빈 디렉터리, nested discoverable `SKILL.md` 제거

새 Routing Skill architecture가 필요하면 먼저 `references/routing-skill-structure.md`를 읽는다.

## `asset-naming`

이름 결정이 주 작업일 때만 사용한다.

1. 새 자산인지 기존 자산인지 확인한다.
2. 기존 자산 rename은 사용자가 명시적으로 요청했는지 확인한다.
3. `references/naming-convention.md`를 읽는다.
4. Domain과 job을 식별하는 가장 짧은 이름을 선택한다.
5. Rename을 적용했다면 내부 reference를 갱신한다.

Skill 폴더와 Frontmatter `name`은 일치해야 하며 이름은 lowercase letters, numbers, single hyphens만 사용한다.

## `compress`

명시된 단일 자연어 agent asset의 token 비용을 줄인다.

보존 대상:

- Frontmatter, heading, code block, inline code
- Command, path, URL, API name
- Version, number, 안전 제약과 실행 순서

제거 대상:

- Filler, hedging, 중복 규칙
- 같은 의미의 반복 예시
- Table이나 code block을 다시 설명하는 prose

편집 전 `<filename>.original.md`를 만들고 의미, trigger, exclusion, safety가 유지되는지 검증한다. Target이 불명확하거나 broad directory인 경우 중단한다. 외부 전송은 명시적 허가 없이 금지한다.

## `routerize-skills`

동일한 domain과 top-level trigger를 공유하는 여러 Skill을 shallow Routing Skill로 통합한다.

두 migration mode를 제공한다.

- `lite`: Source를 `workflows/<id>/WORKFLOW.md`와 격리 resource로 유지
- `full`: Workflow를 `workflows/<id>.md`로 평탄화하고 공통 resource 디렉터리에 병합

완료 조건:

- Root `SKILL.md`, `INDEX.csv`, `workflows/` 존재
- `id,use_when,avoid_when,entrypoint` schema와 고유 ID
- 모든 entrypoint가 Skill 내부에 존재
- `workflows/` 아래 nested `SKILL.md` 없음
- Clear, near-miss, multi-workflow, ambiguous 요청에 대한 route 검증

Source Skill의 permission, ownership, trigger, release lifecycle이 다르면 통합하지 않는다. Filesystem 변환은 `scripts/routerize_skills.py`, 구조 검증은 `scripts/validate_asset.py`를 사용한다.
