# PR #261 — review-changes Skill import handoff

## Scope

- 원본: 사용자가 제공한 `review-changes-skill.zip` (SKILL.md, templates/review.md, README.md, docs/spec.md)
- 정본: `src/rulesync/.rulesync/skills/review-changes/SKILL.md`
- 실행 리소스: `src/rulesync/.rulesync/skills/review-changes/templates/review.md`
- 유지보수 문서: `docs/skills/review-changes/{README.md,spec.md}`
- 생성 경로: `route/skills.jsonl` (직접 편집할 정본 아님)

## Completed

- 초안의 리뷰 계약과 템플릿을 이식함.
- 프로젝트 정책에 맞게 `targets`와 문서 링크를 조정함.
- GitHub API-only 사용 시 로컬 worktree coverage를 주장하지 않도록 명확히 함.
- 원격 브랜치에서 5개 파일을 재조회해 frontmatter, route description/order, 템플릿 마커와 문서 경로를 정적으로 확인함.

## Checks before merge

1. `npm run rulesync:validate` — **Not run**. Rulesync CLI의 실제 structural/target 검증 필요.
2. `mise run generated-sync` (또는 공식 generator 검증 경로) — **Not run**. `route/skills.jsonl` 생성 결과 drift 여부 확인.
3. 필요한 경우 프로젝트 Markdown validation/formatting을 실행하고 실제 실패만 수정.
4. 명세의 RC-01–RC-09는 수용 시나리오이며 **실제 behavioral eval을 실행한 결과가 아님**.

## Boundary

이 PR에서는 임의의 심층 최적화, 자동 수정 능력 추가, 별도의 eval 시스템 신설, 병합을 하지 않는다. 테스트나 구조 검증에서 실제로 확인된 필수 문제만 후속 보완한다.
