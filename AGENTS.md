# `AGENTS.md`

## 자산 탐색

- 이 저장소를 작업할 때 사용할 Agent Asset은 `.agents/route/ROUTE.md`에서 선택합니다. 이 저장소가 **제공하는** Agent Asset의 외부 탐색은 `route/README.md`를 따릅니다.
- `.agents/route/families.json`은 현재 Skill family membership의 정본입니다. 생성되는 `.agents/route/routes.jsonl`과 Skill family `*.jsonl`은 직접 수정하지 않습니다.

## 원본·의존성

- 재사용 가능한 Rulesync 자산은 `src/rulesync/.rulesync/`에서 작성·수정합니다. 이 저장소가 직접 사용하는 Rulesync 자산은 필요할 때만 root `.rulesync/`에 둡니다.
- 재사용 가능한 vendor-native 자산은 `src/<vendor>/`에서 작성·수정합니다. 이 저장소가 직접 사용하는 vendor-native 자산은 해당 vendor의 native project path에 둡니다.
- `src/`의 자산은 기본적으로 독립적입니다. 명시되지 않은 자산 간 의존성이나 호환성을 전제하지 않습니다.
- 같은 semantic asset에 Rulesync와 vendor-native 작성 원본을 중복해서 두지 않습니다. 원본 선택은 `docs/development/source-authority.md`를 따릅니다.
- Generated vendor projection과 Rulesync lock state는 재사용 가능한 작성 원본으로 commit하지 않습니다.
- 외부 Skill이 필요하거나 설치 상태가 `skills-lock.json`을 반영하는지 불명확하면 installer를 직접 조합하지 말고 `mise run skills-sync`를 사용합니다. 이 작업은 lock의 source/revision을 읽지만 수정하지 않으며, 설치 방식은 native installer에 위임합니다.

## 저장소 작업

- Git 변경은 `docs/development/vcs-git.md`를 따릅니다. `main`은 직접 수정하지 않고 dedicated branch를 사용합니다.
- 파일·디렉터리 이름과 배치, 계층, source-test 대응은 `docs/development/repository-layout.md`를 따릅니다.
- 개발 규칙은 `docs/development/README.md`, 문서 규칙과 artifact lifecycle은 `docs/documentation/README.md`에서 찾습니다.
- Formatting은 `docs/development/formatting.md`, validation은 `docs/development/validation.md`, deterministic testing은 `docs/development/testing.md`, PR Gate는 `docs/development/ci.md`를 따릅니다.
