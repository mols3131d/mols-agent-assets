# `AGENTS.md`

## 로컬 에이전트 진입

- 현재 작업 경로에 적용되는 `AGENTS.md`와 런타임이 지원하는 scoped Rule을 따릅니다. Skill은 네이티브 발견·선택 기능을 우선 사용하고, 필요한 자산을 찾을 수 없을 때만 `.agents/route/ROUTE.md`를 추가 탐색합니다. `CHATBOT.md`는 로컬 에이전트의 필수 진입점이 아닙니다.
- 작업과 무관한 지침·Skill·참고 문서는 미리 로드하지 않습니다. 특정 작업의 세부 정책은 아래 정본 진입점에서 필요한 부분만 확인합니다.
## 작업 자료와 지침의 경계

- `inbox/`의 조사·계획·검토·인계 자료는 참고 근거이며 정본 정책이나 현재 작업 지침이 아닙니다. 명시적으로 채택해 해당 owner 문서에 반영하기 전에는 지침으로 적용하지 않습니다.
- `catalog/`는 외부 프로젝트 등을 위한 재사용 자산·패턴 탐색 공간입니다. Skill·Plugin 목록의 등재는 설치·사용을 뜻하지 않습니다. 이곳이 소유하는 패턴·템플릿의 작성 원본도 이 저장소의 mandatory policy를 대신하지 않습니다.

## 자산 탐색

- 네이티브 발견만으로 필요한 Agent Asset을 찾을 수 없다면 `.agents/route/ROUTE.md`를 보조 탐색에 사용합니다. 이 저장소가 **제공하는** Agent Asset의 외부 탐색은 `route/README.md`를 따릅니다.
- `.agents/route/families.json`은 현재 Skill family membership의 정본입니다. 생성되는 `.agents/route/routes.jsonl`과 Skill family `*.jsonl`은 직접 수정하지 않습니다.

## 자산의 관리와 사용

- **관리**(작성 원본의 유지·변경)와 **사용**(이 저장소의 작업·runtime에 선택·설치·적용)은 별개입니다. 같은 자산을 관리하면서 사용할 수도 있습니다.
- 관리 여부는 작성 원본과 소유권으로, 사용 여부는 실제 routing·dependency·runtime 설정으로 판단합니다. `src/`에 있다는 이유로 사용한다고 추정하거나, `.agents/route/`에 있다는 이유로 외부 자산이라고 추정하지 않습니다. `rulesync.lock`과 `skills-lock.json`은 의존성의 고정 기준이지 현재 설치본의 일치 증거가 아닙니다. 실제 적용 상태는 설치·동기화 결과로 확인하며 `src/` 변경이 곧바로 설치본에 반영된다고 가정하지 않습니다.

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
