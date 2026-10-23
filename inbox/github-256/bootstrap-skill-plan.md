# Bootstrap Design Skill — Plan

> PR #256 · 2026-10-24 · independent **Plan Run**. 선행 Research: [bootstrap-skill-research.md](bootstrap-skill-research.md). 본 문서는 이 PR의 Skill 초안 변경 계획이며 실제 bootstrap 실행·업데이트 구현 완료를 뜻하지 않는다.

## 목표 / 완료 조건

`mols-dev-env-bootstrap-design`을 재사용 가능한 canonical Skill로 정리한다. 기존 `mols-dev-bootstrap-design`의 이름·경로·탐색 항목을 완전히 이관하고, 대응하는 maintainer docs와 PR 명세를 갱신한다.

완료 판정:
- Skill package directory와 frontmatter `name`, 배포용 `route/skills.jsonl` row, PR 명세, PR title/body에 **동일한 이름**.
- `docs/skills/mols-dev-env-bootstrap-design/README.md`가 독립 이식 가능한 유지보수 맥락·경계·검증 전략을 제공한다.
- 구 `mols-dev-bootstrap-design` 패키지와 배포 route row는 제거하며, 동일 trigger의 alias를 두지 않는다.
- 기존 setup/update/version/permissions/failure/recovery 계약은 보존한다. 근거 없는 vendor-specific 명령·version constraint를 Skill에 추가하지 않는다.
- Route drift, 구조/문서 품질 검사, PR Gate/Branch Check를 가능한 범위에서 확인하고 미실행 runtime eval은 명시한다.

## Plan Run — Research → Plan → Review (Loop 1)

**Research.** Repository는 `src/rulesync/.rulesync/skills/<name>/SKILL.md`를 reusable authored source로 사용한다. `route/skills.jsonl`은 source를 바탕으로 생성되는 배포 metadata다. `docs/<asset-type>/<asset>/`은 함께 이관할 수 있는 maintainer docs 위치이며 `INDEX.tsv` 자동 생성의 예외다. [Skill authoring conventions](../../docs/references/agent-assets/skills/skill-authoring-conventions.md), [maintainer documentation](../../docs/documentation/asset-maintainer-documentation.md).

**Plan.**
1. 신규 canonical `SKILL.md`에 이름을 변경하면서 유지할 책임(설계/리뷰/handoff)을 명시한다. 기본 동작은 기존 초안을 보존한다.
2. `docs/skills/mols-dev-env-bootstrap-design/README.md`에 목적, non-obvious rationale, scope, update-safe invariants, 검증 방법을 기록한다.
3. 구 `SKILL.md`를 삭제한다. 동일 identity를 두 path에서 운영하지 않는다.
4. 정본을 따라 `route/skills.jsonl`의 기존 entry를 새 이름·URL로 갱신한다. 가능하면 generator와 바이트 동일성 확인.
5. `inbox/github-256/development-environment-bootstrap-spec.md` 내 이름/링크를 갱신하고 작업 상태를 반영한다.
6. PR 설명과 revision metadata를 최신 head 기준으로 갱신한다.

**Review 1 — 결함 탐색.** 새 README를 Skill package 안에 추가하면 runtime context가 불필요하게 커진다. `docs/skills/` placement를 지켜 분리한다. 이름을 path만 바꾸면 frontmatter, route, PR 명세가 stale 상태가 된다. 따라서 identity는 원자적으로 확인하며 rollback 대신 이후 revision에서 부족분을 보완한다.

## Plan Run — Plan refinement → Review (Loop 2)

**재평가 입력.** 연구 Loop 2는 tool-manager user cache와 OS-global installer를 동일시하지 않으면서, 어느 쪽도 무조건적인 설치 권한으로 해석하지 말 것을 요구한다. 또한 `setup`과 `update`가 서로 다른 lock mutation boundary를 가지며 현재 PR은 초기 Skill 단계다.

**수정된 계획과 자산별 owner.**

| 결과물 | Source / write scope | 유지할 책임 | 검증 |
| --- | --- | --- | --- |
| Skill | `src/rulesync/.rulesync/skills/mols-dev-env-bootstrap-design/SKILL.md` | generic bootstrap design, safe install & update boundary, handoff | frontmatter/name/description, structural, scope/near-miss |
| Maintainer docs | `docs/skills/mols-dev-env-bootstrap-design/README.md` | why, invariants, troubleshooting of instruction, long-term maintenance | portable, no runtime instruction duplication, frontmatter |
| Generated distribution | `route/skills.jsonl` | name+description+canonical URL from source | regenerated content equality; no old row |
| PR plan evidence | `inbox/github-256/*` | repo-specific spec/research/plan & decisions | path resolution, state separation |
| PR description | GitHub PR #256 | two deliverables and current progress | exact base/head revision metadata |

**Review 2 — 경계 반증.**
- OS별 설치 예시는 이 Skill의 책임이 아니다. 공식 tool documentation을 실무 적용 시 참조한다.
- Setup command와 Skill 설계를 강하게 결합하지 않는다; scripts/mise 작업은 아직 별도 구현 항목.
- `mols-ci-design`과의 중복은 CI-only case를 description의 negative boundary로 제한한다.
- 세부 참조 파일이나 custom YAML schema를 새로 만들지 않는다. 실제 conditional loading 가치가 나타나면 다음 PR에서 검토한다.
- `route/skills.jsonl`은 직접 authoring 원본으로 취급하지 않는다. GitHub-only 환경에서 generator를 실행할 수 없는 경우, source-derived row를 최소 대체 생성하고 CI drift 결과를 **실제 generator 검증**으로 확인한다.
- 기존 Skill 삭제는 이번 PR이 소유하는 초기 초안에 한정한다. 다른 사용자/branch 상태를 정리하지 않는다.

## Work sequence / Validation

1. 새 Skill 작성 → old Skill 삭제(단일 active source 유지) → generated route 갱신.
2. Maintainer README 작성 → 기존 PR spec 이름/링크 갱신 → 조사 문서의 구 path 근거를 불변 commit URL로 보정.
3. 정적 검토: frontmatter syntax, name consistency, route old/new 개수와 정렬, 변경 파일의 상대 링크, README portability.
4. GitHub API에서 head SHA, PR changed files, branch check/PR Gate workflow runs 확인; failures는 surface별로 구분.
5. PR title/body/revision 갱신. Draft 유지; 실제 `mise run setup` / `mise run update` 구현은 이 단계에 포함하지 않는다.

## 구현 준비 인계

다음 독립 Workstream은 [개발환경 부트스트랩 명세](development-environment-bootstrap-spec.md)에 따라 local `mise.toml`, uv/Rulesync/skills lock owner, shared-state installer safety와 검증을 실제 구현할 것. 이 Skill은 **그 구현의 판단에 사용 가능**해야 하지만 구현이 존재해야만 작동해서는 안 된다.

**Plan Run exit:** 이름/문서/route/spec의 정합성을 실현할 수 있는 bounded plan이 수립되었다. Repository-specific bootstrap runtime correctness는 미검증이며 이후 구현·테스트 Run으로 인계한다.
