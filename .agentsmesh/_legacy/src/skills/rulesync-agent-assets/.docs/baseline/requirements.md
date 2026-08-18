# Requirements

이 문서는 `rulesync-agent-assets`가 계속 만족해야 하는 normative invariant를 정의한다.
Rulesync의 현재 CLI option, target identifier, harness별 파일 경로처럼 upstream 변화에 민감한
정보는 baseline requirement가 아니다.

## Functional Requirements

### R1. Source authority

각 작업은 하나의 authoritative source를 식별해야 한다.

Source는 다음 precedence를 따른다.

1. Repository 또는 project authority가 허용 가능한 source 선택을 제한한다.
2. 그 범위 안에서 caller가 source를 명시하면 그 선택을 따른다.
3. Caller가 source를 생략하면 확립된 ownership 또는 명시된 project default를 사용한다.
4. 충돌하거나 모호한 authority를 임의로 해석하지 않고 mutation 전에 중단한다.

Asset port 요청만으로 source-of-truth policy를 변경하거나 ownership migration을 암묵적으로
수행하지 않는다.

### R2. Evidence-based reuse

Target이 기존 source를 직접 소비할 수 있으면 새 asset을 생성하지 않는다. 단, reuse는
다음 중 하나 이상의 신뢰 가능한 evidence로 target discovery와 필요한 semantic support가
확인된 경우에만 선택한다.

- target의 native contract 또는 공식 documentation
- discovery를 명시적으로 활성화하는 project configuration
- target environment에서의 직접 validation

Path, filename, extension, Markdown/frontmatter shape 또는 format similarity만으로 reuse를
추론하지 않는다.

### R3. Canonical fan-out

Rulesync canonical source가 authoritative한 경우 하나의 source에서 하나 이상의 target
harness용 native asset을 생성할 수 있어야 한다.

### R4. Native bridge

하나의 harness native asset이 authoritative한 경우 그 source를 유지하면서 하나 이상의
다른 harness용 asset을 생성할 수 있어야 한다. 단순 bridge를 위해 canonical source
채택을 강제하지 않는다.

### R5. Minimal scope

Target, asset category와 project/global scope는 요청과 project authority가 요구하는 최소
범위로 제한한다. 명시적 이유 없이 all-target, all-feature 또는 global mutation으로
확장하지 않는다.

### R6. Preview before mutation

Rulesync가 파일을 변경하는 경로는 backend가 제공하는 dry-run 또는 preview를 먼저 사용한다.
예상 밖 output, 누락 source, warning, simulation 또는 unsupported behavior를 확인한 뒤에만
실제 write를 수행한다.

Backend operation에 preview가 없다면 동등한 pre-mutation safety boundary를 명시적으로
확보하지 않은 상태에서 write를 진행하지 않는다.

### R7. Source preservation

Compatibility를 만들기 위해 authoritative source를 암묵적으로 rename, copy, relocate,
normalize 또는 rewrite하지 않는다. Source layout 변경이 필요하면 별도 의도된 변경으로
취급한다.

### R8. Compatibility transparency

File generation 성공을 semantic parity의 증거로 취급하지 않는다. Omitted, approximated,
simulated, unsupported 또는 undiscovered behavior는 caller가 판단할 수 있게 드러낸다.

### R9. Backend delegation

Parsing, normalization, harness mapping과 serialization은 가능한 한 Rulesync에 위임한다.
Concrete하고 반복되는 backend gap이 확인되기 전에는 parallel schema, custom adapter 또는
wrapper compiler를 추가하지 않는다.

### R10. Validation evidence

작업 결과에는 실제 route, authoritative source, target, 생성 결과, compatibility gap과
실제로 수행한 validation evidence가 구분되어야 한다. 실행하지 않은 검증을 성공한 것처럼
보고하지 않는다.

Reuse 결과에서는 target discovery와 요청에 필요한 semantics를 확인한 evidence가 반드시
validation에 포함되어야 한다.

### R11. Generated output is derived

변환으로 생성된 target asset은 authoritative source가 아니라 derived artifact로 취급한다.
Ownership transfer가 필요하면 별도 migration으로 명시해야 하며 ordinary conversion의
부수 효과로 source authority를 옮기지 않는다.

## Quality Requirements

### Q1. KISS

가장 작은 유효 route를 선택한다. Evidence가 있는 direct reuse, 이미 authoritative한
canonical source의 fan-out, native source를 유지하는 bridge 순으로 필요한 만큼만 수행한다.
새 abstraction은 실제 반복 문제가 확인된 뒤에만 추가한다.

### Q2. DRY

- Normative invariant는 이 `requirements.md`가 소유한다.
- Purpose와 scope는 `intent.md`가 소유한다.
- Design rationale와 재검토 조건은 `decisions.md`가 소유한다.
- Runtime routing과 safety instruction은 `SKILL.md`가 소유한다.
- Rulesync CLI와 volatile capability 정보는 backend reference가 소유한다.
- Project-specific default와 gap은 generic core 밖의 project-owned policy/reference가 소유한다.

같은 규범을 여러 문서에서 독립적으로 재정의하지 않는다.

### Q3. SRP

Skill은 source resolution, route, scope, safety, compatibility evidence와 completion contract만
소유한다. Rulesync는 translation mechanics를 소유한다. Caller README는 호출 계약만,
maintainer baseline은 durable product contract만 소유한다.

### Q4. Progressive disclosure

Skill activation과 실행에 필요한 핵심만 `SKILL.md`에 둔다. Backend detail은 필요한 경우에만
reference에서 읽는다. Caller README와 maintainer baseline을 runtime instruction으로 사용하지
않는다.

### Q5. Portability

Generic Skill은 특정 harness나 특정 프로젝트를 source of truth로 가정하지 않는다. 지원
harness 목록과 세부 capability는 installed Rulesync version에 따라 변할 수 있어야 한다.

## Change Rule

R1–R11 또는 Q1–Q5를 의도적으로 깨는 변경은 refactor가 아니라 product contract change다.
같은 변경에서 `intent.md`와 `decisions.md`, caller-visible 영향과 migration 필요성을 함께
검토한다.
