# Adding Skills Support to Clients

이 문서는 [Agent Skills client implementation guide](https://agentskills.io/client-implementation/adding-skills-support)의
핵심 구현 선택지를 요약한다. Strict `SKILL.md` format과 front matter 규격은
[Specification](agent-skills-io-specification.md)이 소유한다.

## Core Lifecycle

Discover → Parse → Disclose → Activate → Preserve.

Metadata를 먼저 공개하고 body와 resource는 필요할 때 로드한다. Discovery와
activation 방식은 local, cloud, sandbox 등 client architecture에 맞춘다.

## Discover

- Local client는 보통 project-level과 user-level scope를 모두 검토한다.
- 각 scope에서 client-native path와 `.agents/skills/` interoperability path를 함께
  지원할 수 있다. Specification 자체는 discovery path를 강제하지 않는다.
- Cloud/sandbox client는 filesystem 대신 API, registry, uploaded/bundled assets 같은
  provisioning 방식을 사용할 수 있다.
- Skill directory는 정확히 `SKILL.md`를 포함하는지 확인한다.
- `.git`, `node_modules`처럼 명백한 비대상은 건너뛰고 scan depth/count에 합리적인
  bound를 둔다.
- 이름 충돌은 deterministic precedence로 처리한다. 일반적으로 project scope가
  user scope보다 우선하며 shadowing을 진단 가능하게 남긴다.
- Project Skill은 untrusted repository에서 올 수 있으므로 product trust model에 맞는
  gating을 검토한다.

## Parse

YAML front matter와 Markdown body를 분리하고 최소한 `name`, `description`,
`location`을 보존한다.

Specification은 strict contract를 정의하지만 client interoperability를 위해
lenient parsing을 선택할 수 있다.

- parent directory와 `name` 불일치 같은 recoverable issue → warn 후 load 가능
- missing/empty `description` → disclosure가 불가능하므로 skip
- 완전히 parse할 수 없는 YAML → skip하고 diagnostic 기록
- 다른 client가 허용한 unquoted colon 같은 흔한 malformed YAML → 제한적인 fallback
  parsing을 검토할 수 있음

Lenient client behavior를 portable Skill authoring 규격으로 역수입하지 않는다.

## Disclose

Model에는 전체 body 대신 compact catalog를 먼저 제공한다.

- 기본 정보: `name`, `description`
- 필요 시: `location`
- 표현 형식: XML, JSON, list 등 client stack에 맞는 구조
- disabled/unauthorized Skill은 catalog에서 제외
- 유효 Skill이 없으면 빈 catalog나 빈 activation tool을 만들지 않음

Catalog는 system instructions에 넣거나 dedicated activation tool과 결합할 수 있다.

## Activate

Model-driven activation은 두 가지 기본 경로가 있다.

- file-read capability가 있으면 해당 `SKILL.md`를 직접 읽는다.
- 그렇지 않거나 더 강한 control/telemetry가 필요하면 dedicated activation tool을
  제공한다.

User-explicit activation syntax는 harness가 정한다. `/skill`, `$skill`, mention 같은
특정 syntax를 portable contract로 고정하지 않는다.

Dedicated tool은 다음을 선택적으로 제공할 수 있다.

- body only 또는 full `SKILL.md`
- Skill identity와 root path를 담은 structured wrapper
- bundled resource 목록 — 내용은 eager-load하지 않음
- permission enforcement와 activation telemetry

## Preserve Context

활성화된 Skill의 효과가 session 중 사라지지 않게 관리한다.

- compaction/pruning에서 active Skill instructions 보호
- 같은 Skill의 불필요한 중복 injection 방지
- 복잡한 작업은 client가 지원할 때 별도 subagent execution을 선택할 수 있음

## Boundary

이 문서는 **client implementation guidance**다. 다음을 정의하지 않는다.

- portable front matter와 directory format
- 특정 vendor/harness의 mandatory discovery path
- repository-local Personal Skill Standard

Client 구현 선택을 Skill authoring requirement처럼 일반화하지 않는다.
