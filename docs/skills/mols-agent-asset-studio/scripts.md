# Agent Asset Studio 스크립트

`agent-asset-studio`는 자산 scaffold, 정적 검증, route index 관리, Routing Skill 변환을 `scripts/`의 Python 도구로 자동화한다. 명령은 Skill root에서 실행한다.

## `init_asset.py`

Agent, Rule, Skill 디렉터리를 표준 구조로 생성한다.

```bash
python3 scripts/init_asset.py <name> \
  --type <skill|rule|agent> \
  --path <parent-directory>
```

주요 option:

| Option | 역할 |
| --- | --- |
| `--description <text>` | Frontmatter `description` 지정 |
| `--resources <list>` | `scripts,references,assets` 등 resource 디렉터리 생성 |
| `--examples` | 선택한 resource에 교체용 예시 파일 생성 |
| `--routing-skill` | root `INDEX.csv`와 `workflows/`를 사용하는 Routing Skill 생성 |
| `--dry-run` | 파일을 만들지 않고 생성 계획만 JSON으로 출력 |

Routing Skill 생성:

```bash
python3 scripts/init_asset.py data-engineering \
  --type skill \
  --path <parent-directory> \
  --routing-skill \
  --description "Use when handling data ingestion, transformation, or quality workflows."
```

생성 구조:

```text
data-engineering/
├── SKILL.md
├── INDEX.csv
└── workflows/
```

`INDEX.csv`는 빈 header로 시작한다.

```csv
id,use_when,avoid_when,entrypoint
```

## `validate_asset.py`

기존 Agent, Rule, Skill의 구조와 기본 품질을 검사하고 JSON 결과를 출력한다.

```bash
python3 scripts/validate_asset.py <asset-directory> --type <skill|rule|agent>
```

공통 검사:

- 필수 Frontmatter와 허용 field
- 이름 형식과 폴더명 일치
- Skill `description`의 activation signal
- 본문 500 lines 초과 여부

Routing Skill 추가 검사:

- root `INDEX.csv`와 `workflows/` 존재
- `id,use_when,avoid_when,entrypoint` schema 일치
- route ID의 kebab-case 및 중복 여부
- `use_when`, `avoid_when` 누락 여부
- entrypoint가 `workflows/` 내부의 안전한 상대 경로인지 확인
- entrypoint 파일 존재 여부
- `workflows/` 아래 nested `SKILL.md` 금지

종료 상태:

- Error가 없으면 exit code `0`, JSON `status: pass`
- Error가 있으면 exit code `1`, JSON `status: fail`
- Warning은 결과에 포함되지만 실패로 처리하지 않음

## `update_index.py`

Routing Skill의 `INDEX.csv`를 생성하고 route를 `id` 기준으로 추가·갱신하는 내부 모듈이다. 현재 독립 CLI가 아니며 `init_asset.py`와 `routerize_skills.py`가 함수로 호출한다.

핵심 동작:

- index가 없으면 표준 header로 생성
- 기존 index의 schema가 다르면 덮어쓰지 않고 실패
- 동일한 `id`는 갱신하고 새 `id`는 추가

Route 조건은 keyword 목록이 아니라 실제 사용자 intent를 설명해야 한다.

## `routerize_skills.py`

여러 기존 Skill을 하나의 shallow Routing Skill로 이동한다.

```bash
python3 scripts/routerize_skills.py \
  --mode <lite|full> \
  --target <routing-skill-directory> \
  <source-skill-1> <source-skill-2>
```

| Mode | 결과 |
| --- | --- |
| `lite` | Source 전체를 `workflows/<id>/`로 이동하고 `SKILL.md`를 `WORKFLOW.md`로 변환 |
| `full` | 본문을 `workflows/<id>.md`로 평탄화하고 resource를 target에 병합 |

`full` mode는 resource 이름이 충돌하면 source Skill ID를 붙이고 workflow의 상대 경로를 갱신한다.

변환 결과:

```text
routing-skill/
├── SKILL.md
├── INDEX.csv
├── workflows/
├── references/   # 필요한 경우
├── scripts/      # 필요한 경우
└── assets/       # 필요한 경우
```

주의:

- Source Skill을 복사하지 않고 이동한다. 버전 관리 또는 백업 상태에서 실행한다.
- 생성된 `use_when`, `avoid_when`은 초기값이다. 실제 사용자 intent와 near-miss에 맞게 수정한다.
- 관련 없는 trigger, permission, ownership, release lifecycle을 가진 Skill은 합치지 않는다.
- 변환 후 `validate_asset.py`로 target을 검증한다.
