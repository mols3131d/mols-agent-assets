# Handoff — PR #262 code-flow-map

## 목표와 경계

- 첨부 `code-flow-map-skill.zip`을 재사용 가능한 Agent Skill 작성 원본으로 흡수한 뒤 확인된 문제만 최소 수정한다.
- 기존 모델 행동 규칙, 증거 등급, 템플릿·예제의 의미를 보존한다.
- 새로운 엔진·서버·별도 CI·eval 프레임워크, 무관한 Skill 변경은 범위 밖이다.
- Draft PR 상태를 유지한다. Merge는 별도의 명시적 승인 이후에만 검토한다.

## 현재 결과

- PR: <https://github.com/mols3131d/mols-agent-assets/pull/262>
- Branch: `mols/feat/code-flow-map` (base: `main`, base snapshot: `b29aa490d0c251d5ca478fa5c787b90258f09d79`)
- Canonical source: `src/rulesync/.rulesync/skills/code-flow-map/`
- Maintainer docs: `docs/skills/code-flow-map/README.md`, `docs/skills/code-flow-map/spec.md`
- 커밋 내역:
  - `626c350` — 네 개의 Skill 패키지 파일을 변경 없이 이식.
  - `40f8000` — README와 명세의 배치·경로·frontmatter 수정.
  - `32d0320` — PR 인계 기록 작성.
  - `992672e` — `route/skills.jsonl` discovery route 갱신.

## 검증 근거

- 첨부 ZIP 원본과 신규 Git blob SHA가 **정확히 일치**:
  - `SKILL.md`: `37049f19406c6b826146857d34c85e9d19b59ac8`
  - `templates/report.md`: `faf7e2d088e4d5dbc28f531911f5331cd0de81a9`
  - `examples/demo-code.ts`: `5c406dc170e396405fdba73f94b30681f3c071ee`
  - `examples/demo-report.md`: `d8738b54e900da37740379b71058098fe18c5e0d`
- 신규 패키지·문서 6개 파일의 내부 상대 링크 18개 점검: 모두 해당 이식 파일을 참조.
- 합성 코드의 라인 10과 14가 예제 보고서의 근거 위치와 일치.
- 문서 2개에 `description` frontmatter 존재 (`docs_frontmatter_validate.py` 통과).
- **결정론적 검증 및 CI 통과:**
  - `pytest -q tests`: 263개 테스트 통과.
  - `npm run rulesync:validate`: config 및 configured-projection 통과.
  - `rulesync doctor --strict`: 0 error, 0 warning.
  - `python -m scripts.generated_artifacts_validate --local-only --all`: PASS.
  - GitHub Actions CI: `Branch Check` 및 `PR Gate` 성공 (Run 41202387564, 41202391810).
  - Rulesync dry-run 생성 검증: 4개 리소스가 런타임 프로젝션 디렉터리에 온전히 매핑됨.
  - Mermaid/Markdown: 기본 구문 검증 완료.
- **잔여 미검증 (의도된 경계):** 실제 대상 코딩 에이전트의 런타임 프롬프트 실행 (spec.md 비목표 및 경계 준수).

## 리뷰 레디 상태 및 다음 작업

- 유지보수 명세(spec.md)의 모든 수용 기준(AC-01 ~ AC-08) 충족 확인.
- CI Gate 및 결정론적 검증 전체 통과.
- 리뷰어 검토 후 Draft 해제 (Ready for review) 전환. 임의 Merge 금지.

## 참고

- 초안의 `.github/skills/code-flow-map/`은 ZIP 내부 경로이며, 저장소 작성 원본은 `src/rulesync/.rulesync/skills/code-flow-map/`이다.
- `docs/spec.md`는 `docs/skills/code-flow-map/spec.md`로 이관했다.
- 검증 수준: 원본 동일성·기본 정적 정합성만 확인됨. 모델 행동 및 실제 renderer 호환성을 검증했다고 주장하지 않는다.
