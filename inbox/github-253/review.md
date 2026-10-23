# PR #253 — Review Report

## Summary

**Decision: Changes needed before declaring the original goal complete.** PR #253은 실제 문서 9개의 영어 heading 불일치를 바로잡고 대표적인 역사 문서 두 곳을 보완했지만, 저장소의 문서 정합성 전체가 해소되었다고 결론 내릴 만큼의 관계 검증과 잔존 문서 점검은 갖추지 못했다. 검증 가능한 표본 성과와 완료 범위를 구분해야 한다.

- PR: https://github.com/mols3131d/mols-agent-assets/pull/253
- Review comparison: base `23d649b2eac6e9115ce0e97a823d59de4d37b3c5`, initial head `ff86e43b782e4fb24055b90d34275d425c66db0f`.
- 작업 계획을 추가한 스냅샷: `80d4c8e16ea05c21229c1200cda6787a46f4069a`. 이하 새 수정 결과는 [remediation-log.md](remediation-log.md)와 [validation.md](validation.md)에서 독립적으로 확인한다.

## Scope

- 실제 PR 변경 29개 파일: 활성 Markdown 9개, 과거 `inbox/` 2개, `inbox/github-253/` 보고서 18개.
- 근거: [Language policy](../../docs/language.md), [Documentation Principles](../../docs/documentation/principles.md), [Asset Maintainer Documentation](../../docs/documentation/asset-maintainer-documentation.md), [audit index](README.md) 및 실제 변경 diff.
- 제목 스타일 변경의 의미 보존, 역사 기록의 현재형 오인, 문서 ↔ 현행 자산/명령 ↔ 링크 관계, 완료 선언의 근거를 검토했다.

## Findings

### 🟡 Medium · F1 — Missing sufficient completion coverage

**Impact:** PR의 목표는 문서 정합성 조사와 수정인데, 현재 결과는 정책상 heading 검사와 일부 역사 문서만 구체적으로 수정했다. 디렉터리별 보고서 다수는 명시적으로 표본이며, `README.md`도 전체 경로 존재 확인, 문서 의미 관계, 역사적 잔존 이름 조사는 완료되지 않았다고 명시한다. CI 통과를 의미 정합성의 완료 근거로 오용하면 실제 stale guidance를 놓칠 수 있다.

**Required Change**
- 현재 PR head에서 high-signal 문서·정본·route·실행 경로의 직접 관계를 검증하고, 정정 가능한 실제 불일치는 같은 PR에서 수정한다.
- 명시적으로 조사한 범위, 반례 확인, 미검증 영역과 실제 수정 범위를 [consistency-evidence.md](consistency-evidence.md)에 기록한다.
- 미검증 범위가 남는다면 최종 결과를 ‘전수 완료’가 아닌 검증된 부분 완료/인계로 표시한다.

**Evidence**
- [기존 audit README — Method and Limits](README.md#method-and-limits)는 의미 정합성/링크 전수를 확인하지 않았음을 명시한다.
- [Retired asset audit](retired-assets.md#evidence-limits)에도 GitHub 검색·표본 한계가 있다.
- [Validation policy](../../docs/development/validation.md)는 PR Gate의 구조 검사와 의미 정합성 판단을 구분한다.

**Location:** `inbox/github-253/README.md`, `inbox/github-253/retired-assets.md`, 이 PR의 변경 범위 전체.

### 🟡 Medium · F2 — Security runbook heading lost important scope

**Impact:** `docs/references/tooling/github-sensitive-data-removal-runbook.md`의 이전 H1은 **회전·폐기할 수 없는 정보**의 **최대한 제거**를 명시했으나, 새 H1 `GitHub Sensitive Data Removal Runbook`은 일반적인 민감정보 삭제로 읽힌다. 런북 설명·서두가 강하게 한정한 대상이 최상위 탐색 제목에서 사라졌다.

**Required Change**
- H1에 `non-rotatable` 및 `maximum removal`에 해당하는 대상과 목적을 되살리되 H1 영어 정책을 유지한다.
- 본문 명령, 조건과 보안 주장은 변경하지 않는다.

**Evidence**
- [Runbook frontmatter와 첫 heading](../../docs/references/tooling/github-sensitive-data-removal-runbook.md)은 같은 파일 안에서 다른 범위를 표현한다.
- PR diff에서 기존 H1 `GitHub에 노출된 회전 불가능한 민감정보 최대 제거 런북`이 범위를 잃은 영어 제목으로 치환되었다.

**Location:** `docs/references/tooling/github-sensitive-data-removal-runbook.md` H1.

## Validation

- ⚪ Not Verified — `repository-wide-semantic-consistency`: 관계별 전수 검증이 수행되지 않았다.
- ⚪ Not Verified — `old-heading-external-fragments`: 외부에서 과거 제목을 fragment로 참조하는지 확인할 수 없다.
- ✅ Pass — `active-doc-relative-path-existence`: `80d4c8e16ea05c21229c1200cda6787a46f4069a` Git tree 기준 `docs/`의 61개 Markdown과 `catalog/`의 32개 Markdown에서 확인한 표준 `] (relative)` 형식의 링크 대상이 트리에 모두 존재했다(문법 전체를 해석한 완전한 Markdown link parser는 아님).
- ✅ Pass — `prior-PR-gate`: 기존 head `ff86e43b782e4fb24055b90d34275d425c66db0f`에 대한 GitHub Actions PR Gate [run #40020033915](https://github.com/mols3131d/mols-agent-assets/actions/runs/40020033915)이 성공했다. 이후 변경에는 별도 gate 확인 필요.

## Remaining Risks

- `inbox/`는 당시에 사실이었던 계획·리뷰도 포함하므로 옛 이름이 보인다는 이유로 자동 삭제하거나 현행 오류라고 단정하면 역사성과 provenance를 훼손한다.
- Heading의 영어 변경은 GitHub 자동 fragment slug를 바꾼다. 현재 저장소 내 참조는 탐색 가능하나 외부 사용자는 별도 위험이다.
- 형식 검증이나 CI가 성공해도 이 리뷰의 F1은 해소되지 않는다. 검증 범위·증거가 필요하다.

```yaml
author:
  - mols3131d:openai-chatgpt
revision:
  base: 23d649b2eac6e9115ce0e97a823d59de4d37b3c5
  head: ff86e43b782e4fb24055b90d34275d425c66db0f
```
