# Document Consistency Audit and Remediation — PR #253

## Result

**PR 목표는 조사와 실제 정합성 수정까지**다. 최초 조사 기준은 [`23d649b2eac6e9115ce0e97a823d59de4d37b3c5`](https://github.com/mols3131d/mols-agent-assets/commit/23d649b2eac6e9115ce0e97a823d59de4d37b3c5)이며, 수정 결과는 이 PR의 head에서 검증한다. 최초 보고서는 표본 조사였으므로 저장소 전체 의미 정합성이 증명됐다고 주장하지 않는다.

**제목 언어 정책 불일치 6개 그룹(DOC-001–006), 활성 문서 9개 수정.** 초기 DOC-001–004와 확장 조사에서 확인한 DOC-005–006은 모두 [Language 정책](../../docs/language.md)의 H1–H3 영어 규칙을 기준으로 다뤘다. 이 그룹 안에서 추가로 확인된 같은 유형의 파일도 함께 수정했다.

## Applied Fixes

| 그룹 | 변경 대상 | 결과 |
| --- | --- | --- |
| DOC-001 | [`docs/using-this-repository.md`](../../docs/using-this-repository.md) | H1–H2 제목 8개 수정 |
| DOC-002 | [`docs/development/source-authority.md`](../../docs/development/source-authority.md), [`evaluation.md`](../../docs/development/evaluation.md) | 제목 9개 + 4개 수정 |
| DOC-003 | [`chatbot-driven-development.md`](../../catalog/patterns/workflow/chatbot-driven-development.md), [`executable-output-checks.md`](../../catalog/patterns/software-engineering/executable-output-checks.md), [`durable-progress-handoff.md`](../../catalog/patterns/workflow/durable-progress-handoff.md) | 제목 7개 + 14개 + 13개 수정 |
| DOC-004 | [`evals/README.md`](../../evals/README.md) | H1 수정 |
| DOC-005 | [`design-principles.md`](../../docs/references/agent-assets/common/design-principles.md) | H2 수정 |
| DOC-006 | [GitHub 민감정보 제거 런북](../../docs/references/tooling/github-sensitive-data-removal-runbook.md) | 제목 44개 수정; 명령과 본문 보존 |

삭제·개명 자산의 참조는 [retired-assets.md](retired-assets.md)에 분리했다. 유효한 family와 migration 설명은 보존하고, 현재형으로 오인할 수 있는 두 역사 문서에는 현행 source로 연결하는 안내를 추가했다.

- [Documentation principles research plan](../2026-08-31/documentation-principles-research-plan.md): 제거된 `mols-markdown-for-human`의 과거 owner 진술에 역사적 시점 안내
- [Docs frontmatter audit](../2026-08-22/docs-frontmatter-audit.md): 제거된 validator 경로와 과거 inventory에 역사적 시점 안내

## Directory Reports

| 범위 | 보고서 | 판정 |
| --- | --- | --- |
| 루트 | [root.md](root.md) | 기존 표본에서 추가 이슈 없음 |
| `docs/` | [docs.md](docs.md) | DOC-001 수정 |
| `docs/development/` | [docs-development.md](docs-development.md) | DOC-002 수정 및 같은 유형 확장 |
| `docs/documentation/` | [docs-documentation.md](docs-documentation.md) | 기존 표본에서 추가 이슈 없음 |
| `docs/references/` | [docs-references.md](docs-references.md) | DOC-005–006 수정 |
| `docs/skills/` | [docs-skills.md](docs-skills.md) | 기존 표본에서 추가 이슈 없음 |
| `docs/subagents/` | [docs-subagents.md](docs-subagents.md) | 기존 표본에서 추가 이슈 없음 |
| `catalog/` | [catalog.md](catalog.md) | DOC-003 수정 및 같은 유형 확장 |
| `src/` | [src.md](src.md) | 기존 표본에서 추가 이슈 없음 |
| `route/` | [route.md](route.md) | 기존 표본에서 추가 이슈 없음 |
| `.agents/` | [agents.md](agents.md) | 기존 표본에서 추가 이슈 없음 |
| `.github/` | [github.md](github.md) | 기존 표본에서 추가 이슈 없음 |
| `scripts/` | [scripts.md](scripts.md) | 기존 표본에서 추가 이슈 없음 |
| `tests/` | [tests.md](tests.md) | 기존 표본에서 추가 이슈 없음 |
| `evals/` | [evals.md](evals.md) | DOC-004 수정 |
| `inbox/` | [inbox.md](inbox.md) | 역사적 기록과 현행 정본 분리 |

## Method and Limits

최초 각 디렉터리별 비교에 더해, PR head의 Git tree에서 일반 활성 Markdown 72개와 `docs/skills/`·`docs/subagents/` 유지보수 문서 27개를 대상으로 fenced code를 제외한 H1–H3 제목에서 한글을 점검했다. 관리용 `CHATBOT.md`의 제목과 보존용 `docs/skills/mols-clarify-code/baseline/decisions.md`는 [Language 정책](../../docs/language.md)의 Agent Asset 지원 자료·preserved text 경계를 고려하여 일괄 번역하지 않았다. 이 검사는 완전한 Markdown parser나 repository-wide semantic audit가 아니다.

변경된 활성 문서의 본문·명령·코드 블록은 보존했다. 기존 heading fragment를 사용하는 repository-local 명시적 참조는 검색에서 확인되지 않았으나 외부 deep link의 영향은 미검증이다. 모든 링크의 도달성, 삭제된 자산의 모든 역사적 이름, 전체 문서 관계, runtime eval을 전수 검사하지 않았다. PR Gate는 최종 head의 결과로 별도 판단한다.

**완료 범위:** 확인된 활성 문서 heading 불일치 수정, 대표적인 역사적 현재형 오인 2건의 안내, 디렉터리별 근거 및 후속 위험 기록. 병합은 별도 승인과 required checks를 따른다.
