# `AGENTS.md`

- `main`을 직접 수정하지 말고 dedicated branch에서 작업합니다.
- Reusable Rulesync 자산은 `src/rulesync/.rulesync/`에서 author/edit합니다. Repository-specific Rulesync 자산은 실제 필요가 있을 때만 root `.rulesync/`에 둡니다.
- Generated vendor projection과 Rulesync lock state는 reusable source로 commit하지 않습니다.
- Task-relevant Skill은 runtime-native discovery를 우선합니다. Native discovery가 없을 때만 `route/ROUTE.md`를 bootstrap으로 사용하고 선택된 source만 로드합니다.
- 임시·전달용 artifact는 `inbox/YYYY-MM-DD/`에 두고, 보존 가치가 있지만 비정본인 artifact는 `inbox/archive/YYYY-MM-DD/`로 이동합니다. 상세 lifecycle은 `inbox/README.md`를 따릅니다.
- Maintainer docs는 durable decision, recovery knowledge 또는 실제 maintenance value가 있을 때만 만듭니다. Sibling 문서를 열거하기 위한 index-only entrypoint는 만들지 않습니다.
