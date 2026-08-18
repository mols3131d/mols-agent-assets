# Working

이 문서는 `mols-skill-creator`의 현재 maintainer state다. 작업 로그가 아니라 다음 개선에 실제로 필요한 현재 상태만 유지한다.

## Current State

- 상태: maintained runtime Skill
- 핵심 모드: create, review-and-improve, tune
- 권위 구조: user instruction → project/repository authority와 durable baseline → implementation → upstream conventions
- maintainer docs: 필요할 때 repository 외부 asset-doc surface 사용
- 개선 루프 기본 상한: 3회

## Current Structure

- `SKILL.md`: 핵심 workflow와 mode
- `references/upstream-sources.md`: 공식 비교 출처와 repository-local deviation
- `references/quality-model.md`: 전체 품질 검증 기준
- `references/platform-compatibility.md`: 멀티환경과 packaging 분리 원칙
- `scripts/init_skill.py`: 새 Skill의 최소 runtime 구조 생성
- `scripts/validate_skill.py`: 구조·frontmatter·링크 정적 검증과 legacy `.docs` 경고
- `scripts/package_skill.py`: 명시적 non-runtime/development surface만 제외하는 runtime package 생성
- `assets/templates/`: 필요할 때 사용하는 Skill/maintainer 문서 template
- `evals/cases.json`: maintainer docs의 optional contract를 포함한 대표 회귀 사례
- `docs/skills/mols-skill-creator/baseline/DIRECTIVE.md`: 이 repository에서 별도 보존 가치가 있는 인간 기준선

## Current Documentation Rule

- 모든 Skill에 maintainer docs를 자동 생성하지 않는다.
- 복잡성, 훼손 위험, durable decision, maintenance/recovery 가치가 있을 때만 만든다.
- 이 repository의 asset-specific maintainer docs는 `docs/<asset-type>/<asset-name>/`에 둔다.
- runtime-required 지식은 Skill package 안에 남긴다.
- 특정 경로나 dot-prefix를 범용 runtime/non-runtime 판별 규칙으로 사용하지 않는다.

## Validation

- initializer는 `SKILL.md`만 기본 생성하며 생성 결과가 존재하지 않는 maintainer docs를 참조하지 않아야 한다.
- eval/reference/quality contract는 maintainer docs를 mandatory package requirement로 되돌리지 않아야 한다.
- validator는 legacy `.docs`가 있으면 project maintainer surface로 이전을 검토하도록 경고해야 한다.
- packager는 `.runtime/` 같은 target-owned dot resource를 prefix만으로 버리지 않고, `.docs`, `.evals`, `evals`처럼 명시적으로 non-runtime인 surface는 제외해야 한다.
- hosted-runtime source와 관련 maintainer/reference 변경은 `tests/scripts/asset_docs_placement/` regression에 연결되어야 한다.

## Promotion Candidates

현재 없음.

## Blockers

현재 없음.
