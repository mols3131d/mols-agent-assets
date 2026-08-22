# `AGENTS.md`

- VCS/Git 변경은 `docs/development/vcs-git.md`를 따릅니다. `main` 직접 수정 금지와 dedicated branch policy는 해당 문서가 소유합니다.
- Reusable Rulesync 자산은 `src/rulesync/.rulesync/`에서 author/edit합니다. 이 repository에서 직접 사용하는 Rulesync 자산은 실제 필요가 있을 때 root `.rulesync/`에 둡니다.
- Reusable vendor-native authored 자산은 `src/<vendor>/`에 둡니다. 이 repository에서 직접 사용하는 vendor-native 자산은 해당 vendor가 정의한 native project path에 둡니다.
- 같은 semantic asset에 Rulesync source와 vendor-native source를 이중 authority로 두지 않습니다. Source 선택은 `docs/development/source-authority.md`를 따릅니다.
- Generated vendor projection과 Rulesync lock state는 reusable authored source로 commit하지 않습니다.
- Cross-runtime Skill discovery fallback은 `route/README.md`를 따릅니다.
- Repository 개발 규칙은 `docs/development/README.md`, 문서 규칙과 artifact lifecycle은 `docs/document/README.md`를 entrypoint로 사용합니다.
- Repository verification은 `docs/development/testing.md`를 따릅니다.
