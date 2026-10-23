# Document Consistency Audit — PR #253

## Result

기준 revision: [`23d649b2eac6e9115ce0e97a823d59de4d37b3c5`](https://github.com/mols3131d/mols-agent-assets/commit/23d649b2eac6e9115ce0e97a823d59de4d37b3c5). 대상은 각 보고서에 명시한 **표본 문서 및 직접 연결된 정본**이며, 저장소 전체 전수 검사는 아니다.

**확인된 finding 4개(동일한 제목 언어 정책 위반 유형):** [docs](docs.md), [docs/development](docs-development.md), [catalog](catalog.md), [evals](evals.md). 서로 다른 디렉터리의 관찰로 분리했으며 공통 원인은 [Language 정책](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/language.md)의 H1–H3 적용 불일치다. 문서 범위 내 기능·권한 충돌은 이번 표본에서 확인되지 않았다.

## Retired Asset Documentation

- [삭제·개명 자산 문서 잔존 조사](retired-assets.md): 과거 Skill/Subagent 이름과 남아 있는 문서를 원본·family·이력 기준으로 분리했다. 과거 `inbox/`에 현재형으로 남은 설명과 존재하지 않는 경로 참조가 확인됐지만, 이를 현행 maintainer capsule의 orphan으로 단정하지 않았다.
- 이전 `mols-rpi`와 `review-*` 언급 가운데 실제 migration/consumer 호환성 설명은 보존 대상이다. `mols-markdown`·`mols-mermaid`처럼 별도 Skill 없이 현재 family로 유지되는 디렉터리도 삭제 후보가 아니다.

## Disposition and Next Work

- **DOC-001–004:** 동일한 heading 언어 정책의 디렉터리별 사례다. 이 PR에서는 증거를 보존하고, 실제 제목 수정은 별도 문서 수정 PR에서 처리한다. Heading 변경 시 기존 anchor와 내부 참조 영향도 함께 확인한다.
- **삭제·개명 자산:** 현행 maintainer 문서의 orphan은 표본에서 검증되지 않았다. 발견된 `inbox/`의 오래된 public Skill·Subagent 이름은 당시 작업 기록으로 남긴다. 현재형으로 읽힐 우려가 있으면 역사적 원문을 일괄 삭제·치환하는 대신 현재 정본이나 superseded 상태를 연결하는 후속 작업을 검토한다.
- **미검증 범위:** 전체 파일 inventory, 이동·삭제된 모든 경로의 존재 확인, repository-wide link 검사와 runtime 검증은 수행하지 않았다. 추가 전수 검사는 별도 작업이며 이번 표본 결과의 merge 자체를 전체 저장소 정합성 인증으로 해석해서는 안 된다.

## Directory Reports

| 범위 | 보고서 | 확인된 이슈 |
| --- | --- | --- |
| 루트 | [root.md](root.md) | 없음 |
| `docs/` | [docs.md](docs.md) | DOC-001 |
| `docs/development/` | [docs-development.md](docs-development.md) | DOC-002 |
| `docs/documentation/` | [docs-documentation.md](docs-documentation.md) | 없음 |
| `docs/references/` | [docs-references.md](docs-references.md) | 없음 |
| `docs/skills/` | [docs-skills.md](docs-skills.md) | 없음 |
| `docs/subagents/` | [docs-subagents.md](docs-subagents.md) | 없음 |
| `catalog/` | [catalog.md](catalog.md) | DOC-003 |
| `src/` | [src.md](src.md) | 없음 |
| `route/` | [route.md](route.md) | 없음 |
| `.agents/` | [agents.md](agents.md) | 없음 |
| `.github/` | [github.md](github.md) | 없음 |
| `scripts/` | [scripts.md](scripts.md) | 없음 |
| `tests/` | [tests.md](tests.md) | 없음 |
| `evals/` | [evals.md](evals.md) | DOC-004 |
| `inbox/` | [inbox.md](inbox.md) | 삭제·개명 이름의 과거 기록 확인 (현행 결함과 구분) |

## Method and Limits

정본, 적용 범위와 실제 문서·자산을 같은 commit에서 비교했다. 확인됨/미해결/기각을 구분했고, 검색 결과가 없다는 이유만으로 누락을 확정하지 않았다. GitHub 파일 조회 및 검색으로 점검했으며, 로컬 checkout·스크립트 실행·링크 전체 크롤링·CI 실행·generated projection 재생성은 하지 않았다. 따라서 **보고서의 ‘확인된 이슈 없음’은 해당 표본에만 적용**한다.

이번 PR은 조사 결과를 기록한다. 정본 문서와 설정을 수정하거나 merge하지 않는다.
