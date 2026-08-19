# `AGENTS.md`

## Working Rules

- `main`을 직접 수정하지 말고 작업 branch에서 변경합니다.
- 재사용 Rulesync 자산은 `src/rulesync/.rulesync/`에서만 author/edit합니다.
- 이 repository 자체를 위한 Rulesync 자산은 실제 필요가 있을 때만 root `.rulesync/` workspace에 둡니다. Reusable library를 root에 mirror하지 않습니다.
- Rulesync-managed schema, feature, target namespace와 projection behavior는 current Rulesync를 따릅니다. Repository-local superset schema나 manual projection layer를 만들지 않습니다.
- 이 저장소는 vendor/target support matrix를 정의하지 않습니다. Target은 구체적인 projection 또는 검증 작업에서만 선택합니다.
- Generated vendor projection과 Rulesync lock state를 reusable library source로 commit하지 않습니다.
- Repository verification은 `tests/`, `evals/`가 소유합니다. Runtime-required resource만 deployable asset package 안에 둡니다.
- `route/`는 derived discovery metadata입니다. Canonical asset body나 policy를 복제하지 않습니다.
- Maintainer docs는 durable decision, recovery knowledge 또는 실제 maintenance value가 있을 때만 만듭니다. 작업 로그와 쉽게 재생성되는 상태는 Git history에 맡깁니다.
- 변경 후 가장 작은 관련 test/eval을 우선 실행합니다. Target-specific runtime claim이 성공 조건일 때만 해당 usage surface의 evidence를 요구합니다.

## References

- Rulesync integration boundary → `docs/references/common/conventions/rulesync-repository-conventions.md`
- Skill authoring → `docs/references/skills/skill-authoring-conventions.md`
- Development workflow → `docs/development.md`
- Testing → `docs/testing.md`
- Cross-runtime routing → `route/README.md`
