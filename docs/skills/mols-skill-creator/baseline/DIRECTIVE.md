# Directive

이 문서는 `mols-skill-creator`의 인간 주도 규범적 기준선이다. 사용자의 명시적 요청 없이 핵심 요구사항과 불변조건을 임의 변경하지 않는다.

## Purpose

OpenAI, Microsoft, Anthropic 등 신뢰할 수 있는 상위 구현을 참고해 새 Skill을 만들고 기존 Skill을 지속적으로 개선·튜닝하는 범용 `mols-skill-creator`를 제공한다.

최우선 목적은 기존 Skill의 품질을 높이는 것이다. 개선 과정에서 핵심 의도가 훼손될 위험이 큰 Skill은 durable maintainer evidence를 통해 올바른 형태로 복구할 수 있어야 한다.

## Requirements

| ID | Requirement |
| --- | --- |
| R-01 | 새 Skill을 설계하고 생성할 수 있어야 한다. |
| R-02 | 기존 `SKILL.md`와 부속 자산을 리뷰하고 직접 개선해야 한다. |
| R-03 | 특정 프로젝트, AI 에이전트, 배포 환경에 맞게 튜닝해야 한다. |
| R-04 | OpenAI·Microsoft·Anthropic 구현을 비교하고 적합한 원칙을 재구성할 수 있어야 한다. |
| R-05 | runtime-required resource와 maintainer-only documentation을 구분해야 한다. |
| R-06 | 수정 후 가능한 deterministic validation을 실행하고 실패하면 원인을 수정·재검증해야 한다. |
| R-07 | maintainer docs는 복잡성·훼손 위험·durable decision·recovery 필요가 있을 때만 선택적으로 생성해야 한다. |
| R-08 | target project가 maintainer-doc placement를 정의하면 그 authority를 따라야 한다. |

## Invariants

| ID | Invariant |
| --- | --- |
| I-01 | 사용자의 현재 명시적 지시가 가장 높은 권위를 가진다. |
| I-02 | 기존 durable baseline이 있으면 의도 변경 없이 임의 수정하지 않는다. |
| I-03 | 기존 Skill 개선을 새 Skill 생성보다 우선한다. |
| I-04 | 검증 실패를 성공으로 축소 보고하지 않는다. |
| I-05 | 공통 원칙과 특정 벤더 전용 관례를 구분한다. |
| I-06 | maintainer-only documentation은 runtime package의 필수 의존성이 아니다. |
| I-07 | 단순한 Skill에 문서 구조를 기본 scaffold로 추가하지 않는다. |
| I-08 | runtime에 필요한 지식은 deployable Skill surface가 소유한다. |

## Allowed Scope

| Area | Allowed |
| --- | --- |
| Files | `SKILL.md`, runtime `references/`, `scripts/`, `assets/`, `templates/`, eval/test surface와 프로젝트가 허용한 maintainer docs 생성·수정·재구성 |
| Research | 최신 공식 문서, 저장소, SDK/API 원문 비교 |
| Execution | 대상 Skill 직접 수정, 정적 검증, 가능한 대표 실행·평가 |
| Refactoring | 구조 변경, 중복 제거, reference 분리, 환경별 adapter 설계 |
| Packaging | runtime-required surface만 포함하는 배포 번들 생성 |

## Boundaries

| Boundary | Rule |
| --- | --- |
| Human authority | durable baseline의 핵심 의도는 명시적 authority 없이 바꾸지 않는다. |
| Documentation | maintainer docs는 필요성 근거 없이 만들지 않고 target project의 external maintainer-doc convention을 따른다. |
| History | 작업 로그를 baseline으로 축적하지 않는다. 현재 판단에 필요 없는 임시 기록은 제거한다. |
| Evidence | 외부 사실과 최신 규칙은 공식·1차 자료를 우선한다. |
| Security | 사용자 기대를 벗어나는 은닉 동작, 권한 확대, 데이터 유출을 설계하지 않는다. |

## Adopted Decisions

| Decision | Rationale |
| --- | --- |
| 범용 멀티환경 Skill로 설계한다. | 개발자, AI 에이전트, Skill 배포 환경이 단일 벤더에 제한되지 않는다. |
| 생성·리뷰·튜닝을 하나의 Skill에서 지원한다. | 동일한 분석·설계·검증 자산을 공유하고 개선 흐름을 일관되게 유지할 수 있다. |
| 기존 Skill 개선을 핵심 기능으로 둔다. | 실제 사용과 dogfooding에서 축적되는 가치가 신규 생성보다 크다. |
| maintainer docs는 optional이다. | 단순 Skill까지 문서화하면 context·유지보수 비용만 늘어나며, 복잡하거나 fragile한 자산에서만 별도 보존 가치가 생긴다. |
| maintainer docs와 runtime package를 분리한다. | 실행 payload와 인간/maintainer 보존 지식의 책임을 혼합하지 않는다. |
| 필요한 Skill maintainer docs는 runtime package 밖의 하나의 asset-scoped capsule에 둔다. | Host project가 물리 경로를 선택해도 자산별 maintainer context를 함께 이동·복구할 수 있다. |
| 기본 initializer는 `SKILL.md`만 생성한다. | 필요하지 않은 문서·directory의 선제 생성을 막는다. |
| 자동 검증 → 자동 수정 → 재검증을 가능한 범위에서 적용한다. | 단발성 수정이 아니라 검증 가능한 품질 수렴을 목표로 한다. |

## Rejected Decisions

| Decision | Rationale |
| --- | --- |
| 모든 Skill에 `DIRECTIVE.md`와 `WORKING.md`를 강제한다. | 단순 Skill에 의례적 문서 구조와 유지보수 비용을 만든다. |
| package-local `.docs/`를 maintainer convention으로 사용한다. | maintainer docs를 package source와 섞고 target별 packaging 동작에 의존하게 만든다. |
| maintainer docs를 runtime package에 포함한다. | runtime contract와 유지보수 지식의 책임이 혼합된다. |
| 모든 과거 결정과 시행착오를 보존한다. | 현재 판단을 방해하고 토큰·인지 비용을 키운다. |
| 수정 전마다 사용자 승인을 기다린다. | 승인된 작업 범위 안의 자동 개선과 검증 흐름을 불필요하게 중단한다. |
