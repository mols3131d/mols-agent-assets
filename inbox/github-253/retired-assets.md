# Retired Asset Documentation — Consistency Audit

## Scope

- 기준: `mols3131d/mols-agent-assets`의 `23d649b2eac6e9115ce0e97a823d59de4d37b3c5` (PR #253의 최초 비교 기준)
- 대상: [`route/skills.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/skills.jsonl), [`route/subagents.jsonl`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/subagents.jsonl), 현행 `src/rulesync/.rulesync/` 원본, `docs/skills/`·`docs/subagents/` 유지보수 문서, 과거 `inbox/` 기록의 관련 표본
- 방법: 삭제·개명된 식별자를 검색하고 정확한 원본 경로 유무와 유지보수 문서의 **현재 적용 여부**를 대조. GitHub 검색은 전수 디렉터리 열거가 아니므로 빠진 파일이 있을 수 있다.
- 결과: **삭제된 자산 이름이 남은 과거 기록을 여러 건 확인했다.** 그러나 조사한 현행 `docs/skills/`·`docs/subagents/` maintainer directory에서 **실제 소유 자산 또는 family가 사라진 orphan capsule은 검증되지 않았다.** 역사적 언급과 실행 지침을 혼동하지 않는다.

## Historical Residuals

| 분류 | 현재 원본 | 확인된 잔존 문서 | 판정 / 처리 |
| --- | --- | --- | --- |
| `mols-markdown-for-human` | Skill 경로 없음 | [documentation-principles-research-plan.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-31/documentation-principles-research-plan.md), [mols-text-optimizer-plan.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-31/mols-text-optimizer-plan.md) | **과거 서술 확인.** 첫 문서는 삭제된 Skill이 Markdown 표현의 현재 owner라는 현재형 설명을 포함한다. 역사 자료는 보존하되 현재 작업 가이드로 재사용하지 않는다. |
| `mols-agent-asset-validator` | Skill 경로 없음 | [review-subagents-modernization-research.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/review-subagents-modernization-research.md), [review-subagents-modernization-review.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/review-subagents-modernization-review.md), [docs-frontmatter-audit.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/docs-frontmatter-audit.md) | **과거 서술 및 사라진 경로 참조 확인.** `docs-frontmatter-audit.md`의 `docs/skills/mols-agent-asset-validator/baseline/DIRECTIVE.md`는 기준 revision에서 없음. 기록은 역사적 조사이며 현재 유효한 링크로 해석하지 않는다. |
| `review-lead`, `review-quality`, `review-adversarial` | 이전 Subagent 경로 없음 | [review-subagents-modernization-research.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/review-subagents-modernization-research.md), [plan.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/review-subagents-modernization-plan.md), [review.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/review-subagents-modernization-review.md), [legacy-audit.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/agent-assets-modernization-legacy-audit.md) | **이전 설계 및 검토 기록.** [DualVantage maintenance](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/subagents/mols-review-dualvantage/maintenance.md)의 `Legacy review callers`는 **현재형 지침이 아닌 이전 호출자 이관 설명**으로 보존할 이유가 있다. |
| `mols-rpi` | 이전 Skill 경로 없음 | [promptfoo-eval-adoption-plan.md](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-20/promptfoo-eval-adoption-plan.md), 기타 과거 RPI 관련 조사·리뷰 문서 | **개명 이력.** [mols-loops README](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-loops/README.md)의 `Public Rename Boundary`는 의도적으로 과거 이름을 설명한다. 제거 대상이 아니다. |

위 항목은 **삭제된 이름을 언급하는 문서**이지 전부 **현재 살아 있는 잘못된 문서**라는 뜻이 아니다. 검색에서 발견되지 않은 경우를 결함 없음으로 일반화하지 않는다.

## Additional Historical Usage Evidence

같은 기준 revision에서 옛 public Skill 이름 `mols-rpi`를 직접 호출·참조한 추가 기록도 확인했다.

- [Mermaid diagram examples review](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-29/mermaid-diagram-examples-review.md)는 당시 작업 지침과 체크리스트에 `mols-rpi`를 사용한다. 해당 작업 이력을 현재 사용 가능한 Skill 이름으로 오독하지 않는다.
- [Promptfoo eval adoption proposal](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-20/promptfoo-eval-adoption-proposal.md)은 `mols-rpi`를 초기 PoC 후보로 언급한다. 채택 당시 제안의 provenance이지 현재 route의 identity 선언이 아니다.
- [Caveman-ko RPI review](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-08-22/caveman-ko-rpi-review.md)는 이전 `mols-rpi` eval surface의 CI 판단을 기록한다. 과거 CI 설명으로 보존하고 현재 eval route를 증명하는 자료로 사용하지 않는다.

이 기록들은 구체적인 과거 소비 맥락을 추가하지만, 현행 active maintainer 문서의 orphan이 새로 확인됐다는 뜻은 아니다.

## Active Maintainer Documents Checked

| 문서 경로 | 현재 연결 | 판정 |
| --- | --- | --- |
| [`docs/skills/mols-markdown/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-markdown/README.md) | `mols-documentation`, `mols-markdown-dashboard`, `mols-markdown-maintenance` | **유효 family.** `mols-markdown` 단독 Skill이 없다는 사실만으로 orphan이 아니다. |
| [`docs/skills/mols-mermaid/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-mermaid/README.md) | `mols-mermaid-diagram`, `mols-mermaid-chart` | **유효 family.** 단독 `mols-mermaid` Skill 없음은 정상이다. |
| [`docs/skills/mols-loops/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/skills/mols-loops/README.md) | `mols-loops` | **유효 maintainer 문서.** 옛 `mols-rpi` 명칭은 migration 경계로 유지된다. |
| [`docs/subagents/mols-review-dualvantage/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/subagents/mols-review-dualvantage/README.md) | 현재 `mols-review-dualvantage`와 Verifier/Challenger | **유효 family.** 과거 `review-*` 이름은 구형 caller와 대응 관계를 설명한다. |
| `docs/skills/`에서 이번 검색으로 식별한 나머지 maintainer 디렉터리(예: `mols-agent-asset`, `mols-clarify-code`, `mols-markdown-dashboard`, `mols-text-optimizer`, `caveman-ko`) | 대응 `route/skills.jsonl` 원본 식별자가 존재 | **표본에서 orphan 확인 안 됨.** 모든 하위 파일을 전수 열거하지는 않았다. |

## Distinguish from an Unfinished Removal

[`inbox/2026-09-07/mols-coding-context/migration.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/inbox/2026-09-07/mols-coding-context/migration.md)는 `coding-context`의 교체·삭제를 *계획*하지만, [현재 원본](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/src/rulesync/.rulesync/skills/coding-context/SKILL.md)과 [route entry](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/route/skills.jsonl)는 여전히 존재한다. 이 항목은 **삭제된 자산의 orphan 문서가 아니며**, 별도의 완료/현재 지원 범위 확인 후보로 둔다. 계획 문서만으로 실제 삭제 완료를 주장하면 잘못이다.

## Applied Historical-Reference Corrections

- [Documentation principles research plan](../2026-08-31/documentation-principles-research-plan.md)에 현재는 삭제된 `mols-markdown-for-human`의 과거 owner 문구가 현행 계약이 아님을 알리는 **Historical snapshot** 안내를 추가했다.
- [Docs frontmatter audit](../2026-08-22/docs-frontmatter-audit.md)에 사라진 `mols-agent-asset-validator` 경로 및 시점이 지난 inventory를 현재 작업 지침으로 오독하지 않도록 안내를 추가했다.
- 두 문서의 당시 관찰·검토·수치·이력 원문은 수정하거나 삭제하지 않았다. 기타 과거 `review-*`, `mols-rpi` 기록 및 현행 migration 설명은 이력 보존 대상으로 유지했다.

## Disposition

1. **보존** — 현재 자산·family의 maintainer 문서와 migration 설명. `docs/skills/mols-markdown/`, `docs/skills/mols-mermaid/`, `docs/skills/mols-loops/`, `docs/subagents/mols-review-dualvantage/`를 이름만으로 삭제하지 않는다.
2. **역사 자료로만 취급** — `inbox/`의 과거 계획·리뷰에는 삭제 전 자산명이 남아도 당시 근거를 유지한다. 현재 운영 지침이나 링크라고 오독할 우려가 있으면 한곳에 superseded 안내를 연결할 수 있다.
3. **후속 정리 후보** — 역사적 문서 속 현재형 owner 서술과 존재하지 않는 경로를 현재 문서로 인용하는 경우를 우선 정리한다. 원문 훼손보다 별도 status/정본 링크 표시를 먼저 검토한다.
4. **추가 검증 필요** — repository 전체 파일 inventory 및 모든 `docs/skills/**`·`docs/subagents/**`에 대한 exact path 검사. 검색 결과 수만으로 orphan이 완전히 없다고 판정할 수 없다.

## Evidence Limits

`route/*.jsonl`이 제공하는 canonical 이름 목록과 개별 GitHub 원본 경로 조회로 현재 존재 여부를 확인했다. 검색은 index coverage 제한이 있고 `inbox/`의 모든 파일을 검사하지 않았다. 현재 live `main`은 조사 시작 기준 이후 별도로 진전될 수 있으므로 새 revision에 결론을 자동 승계하지 않는다. 이 조사의 역사적 자산 분석은 표본 기준이며, 이번 PR에서는 검증된 현재형 오인 위험 두 문서에 안내를 추가했다. 파일 삭제·이동과 대규모 이력 정리는 수행하지 않았다.
