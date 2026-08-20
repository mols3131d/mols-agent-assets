# `AGENTS.md`

- `main`을 직접 수정하지 말고 dedicated branch에서 작업합니다.
- Reusable Rulesync 자산은 `src/rulesync/.rulesync/`에서 author/edit합니다. Repository-specific Rulesync 자산은 실제 필요가 있을 때만 root `.rulesync/`에 둡니다.
- Generated vendor projection과 Rulesync lock state는 reusable source로 commit하지 않습니다.
- Task-relevant Skill은 runtime-native discovery를 우선합니다. Native discovery가 없을 때만 `route/ROUTE.md`를 bootstrap으로 사용하고 선택된 source만 로드합니다.
- Repository 개발 규칙은 `docs/development/README.md`, 문서 규칙과 artifact lifecycle은 `docs/document/README.md`를 entrypoint로 사용합니다.
- Repository verification은 `docs/testing.md`를 따릅니다.
