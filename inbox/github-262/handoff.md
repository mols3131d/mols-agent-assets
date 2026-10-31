# Handoff — PR #262 code-flow-map

## 목표와 경계

- 첨부 `code-flow-map-skill.zip`을 재사용 가능한 Agent Skill 작성 원본으로 흡수한 뒤 확인된 문제만 최소 수정한다.
- 기존 모델 행동 규칙, 증거 등급, 템플릿·예제의 의미를 보존한다.
- 새로운 엔진·서버·별도 CI·eval 프레임워크, 무관한 Skill 변경은 범위 밖이다.
- Ready for review 상태를 유지한다. Merge는 별도의 명시적 승인 이후에만 검토한다.

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
  - `1297abb` — PR #262 검증 결과 및 리뷰 레디 상태 갱신.
  - `ca12ae9` — 1차 리뷰 피드백(Review #5722871862) 반영 (targets 선언, secret 마스킹, UNRESOLVED 간선 규칙 보완).
  - 후속 커밋 — 2차 리뷰 피드백(Review #5722916809) 반영 (템플릿 코드 펜스 언어 표기 복원, 수용 기준 판정 범위 명확화, handoff 상태 정합).

## 검증 근거

- 첨부 ZIP 원본과 초기 Git blob SHA 일치 확인 후, 리뷰 피드백에 따른 최소 계약·안전 지침 보강.
- 신규 패키지·문서 파일의 내부 상대 링크 점검 완료.
- 합성 코드의 라인 10과 14가 예제 보고서의 근거 위치와 일치.
- 문서 2개에 `description` frontmatter 존재 (`docs_frontmatter_validate.py` 통과).
- **리뷰 피드백 반영 사항 (Review #5722871862, #5722916809):**
  - `SKILL.md`: `targets` 명시 (6개 타깃 지원 선언).
  - `SKILL.md`: 보고서 스니펫/로그에서 secret·민감정보 제외 및 마스킹 지침 추가.
  - `SKILL.md` / `spec.md` / `templates/report.md`: `UNRESOLVED` 연결 시 대상·방향 미확정 건 다이어그램 생략 및 미해결 항목 기록 분리.
  - `templates/report.md`: 코드 펜스 `{{LANGUAGE}}` 표기 복원 및 `SKILL.md`에 언어 식별자 치환 지침 명시.
- **결정론적 검증 및 CI 통과:**
  - `pytest -q tests`: 263개 테스트 통과.
  - `npm run rulesync:validate`: config 및 configured-projection 통과.
  - `rulesync doctor --strict`: 0 error, 0 warning.
  - `python -m scripts.generated_artifacts_validate --local-only --all`: PASS.
  - GitHub Actions CI: `Branch Check` 및 `PR Gate` 성공.
  - Rulesync dry-run 생성 검증: 4개 리소스가 런타임 프로젝션 디렉터리에 온전히 매핑됨.
  - Mermaid/Markdown: 기본 구문 검증 완료 (`rumdl check` 0 issues).
- **잔여 미검증 (의도된 경계):** 실제 대상 코딩 에이전트의 런타임 프롬프트 실행 및 렌더러별 시각적 렌더링 (spec.md 비목표 및 경계 준수).

## 리뷰 레디 상태 및 수용 기준 판정 수준

- **정적 규격 및 계약 수준 충족:** 유지보수 명세(spec.md)의 계약 규격, 합성 예제, 템플릿 구조 및 안전 경계(AC-01 ~ AC-08)가 정적 파일 수준에서 정의 및 일치함을 확인.
- **결정론적 검증 및 CI Gate 통과:** 저장소 네이티브 검증(`rulesync:validate`, `pytest`, `generated-validate`, `rumdl check`) 및 GitHub Actions(`Branch Check`, `PR Gate`) 전체 통과.
- **실제 동작 미검증 경계 보존:** 실제 코딩 에이전트의 런타임 보고서 생성 품질, 런타임 추적 정확도 및 각 렌더러별 Markdown/Mermaid/HTML 시각적 렌더링은 이번 이식 범위 밖(비목표)으로 미검증 상태를 명확히 유지.
- **다음 작업:** Owner 1차·2차 리뷰 지적 사항 조치 완료 및 Ready for review 상태 유지. 승인 후 Merge 진행.

## 참고

- 초안의 `.github/skills/code-flow-map/`은 ZIP 내부 경로이며, 저장소 작성 원본은 `src/rulesync/.rulesync/skills/code-flow-map/`이다.
- `docs/spec.md`는 `docs/skills/code-flow-map/spec.md`로 이관했다.
- 검증 수준: 원본 동일성·기본 정적 정합성만 확인됨. 모델 행동 및 실제 renderer 호환성을 검증했다고 주장하지 않는다.
