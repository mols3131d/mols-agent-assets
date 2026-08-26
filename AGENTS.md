# `AGENTS.md`

- VCS/Git 변경은 `docs/development/vcs-git.md`를 따릅니다. `main` 직접 수정 금지와 dedicated branch policy는 해당 문서가 소유합니다.
- Reusable Rulesync 자산은 `src/rulesync/.rulesync/`에서 author/edit합니다. 이 repository에서 직접 사용하는 Rulesync 자산은 실제 필요가 있을 때 root `.rulesync/`에 둡니다.
- Reusable vendor-native authored 자산은 `src/<vendor>/`에 둡니다. 이 repository에서 직접 사용하는 vendor-native 자산은 해당 vendor가 정의한 native project path에 둡니다.
- 같은 semantic asset에 Rulesync source와 vendor-native source를 이중 authority로 두지 않습니다. Source 선택은 `docs/development/source-authority.md`를 따릅니다.
- Generated vendor projection과 Rulesync lock state는 reusable authored source로 commit하지 않습니다.
- `skills-lock.json`의 외부 Skill dependency가 필요하거나 현재 설치가 lock 상태를 반영하는지 불명확하면 installer를 직접 조합하지 말고 `mise run skills-sync`를 사용합니다. 이 task는 lock의 source/revision을 읽되 lock을 수정하지 않으며, vendor별 payload·설치 방식은 해당 dependency의 native installer에 위임합니다.
- 이 repository 자체를 작업하는 agent의 routing entrypoint는 `.agents/route/ROUTE.md`입니다. `.agents/route/`는 이 repository가 사용하는 Agent Asset의 routing surface이며, 현재 generated Skill route의 family membership은 `.agents/route/families.json`이 소유합니다. `routes.jsonl`과 현재 Skill family `*.jsonl`은 lock/config와 family membership에서 생성되는 discovery data이므로 직접 편집하지 않습니다.
- 이 repository가 제공하는 Agent Asset의 cross-runtime discovery fallback은 `route/README.md`를 따릅니다.
- Repository 개발 규칙은 `docs/development/README.md`, 문서 규칙과 artifact lifecycle은 `docs/documentation/README.md`를 entrypoint로 사용합니다.
- Repository verification은 `docs/development/testing.md`를 따릅니다.
