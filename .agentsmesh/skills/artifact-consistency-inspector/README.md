# Artifact Consistency Inspector

원격 software 또는 data repository를 읽기 전용으로 검사하고, 서로 일치하거나 추적되어야 하는 artifact 사이의 gap을 evidence와 함께 Markdown report로 반환하는 ChatGPT Skill입니다.

```text
intent, rule, or contract ↔ implementation ↔ validation
```

## 주요 특성

- repository 구조, 언어, framework, host에 고정되지 않음
- repository·PR·revision·file·symbol·feature·rule·guideline 입력 지원
- 문서, 정책, ADR, schema, configuration, code, migration, test, operational validation 관계 검사
- `rule_sources`를 저장소별 순서형 목록으로 해석
- 모든 주요 control이 `auto`를 지원
- source repository와 repository-host state를 수정하지 않음
- 결과를 timestamp가 붙은 Markdown 하나 또는 필요한 경우 ZIP 하나로 반환

## 패키지 구조

```text
artifact-consistency-inspector/
├── SKILL.md
├── README.md
└── references/
    ├── inspection-rules.md
    ├── rule-sources.md
    ├── report-format.md
    └── example-report.md
```

`references/`는 runtime에서 조건부로 읽는 resource입니다. Repository-owned deterministic tests와 scenarios는 deployable package 밖 `tests/skills/artifact-consistency-inspector/`에서 관리합니다.

ChatGPT 설치 시 ZIP 내부의 `artifact-consistency-inspector/SKILL.md` 이름과 위치를 유지하는 것이 안전합니다. 외부 ZIP 파일명은 자유롭게 변경할 수 있습니다.

## 입력 예시

```text
이 repository에서 API 문서, 구현, 테스트가 일치하는지 검사해줘:
https://github.com/example/project
```

```text
이 PR에서 CONTRIBUTING 규칙과 구현·검증 사이 gap을 찾아줘:
https://github.com/example/project/pull/123
```

```yaml
repository: https://github.com/example/project
target: refund-processing-v2
rule_sources:
  - docs/team-api-policy.md
  - auto
  - baseline:release-2026.07
loops: 2
```

`rule_sources`의 배열 순서는 authority precedence입니다. `auto`는 그 위치에서 실제 repository에 적용되는 source locator 목록으로 확장됩니다.

## 출력

기본 파일명:

```text
<repository-name>-artifact-consistency-report[-<target>]-<yyyyMMddHHmm>.md
```

보고서에는 YAML front matter, compact Summary table, Findings, Coverage가 포함됩니다. 각 finding은 `Observed difference`, `References`, `Potential impact` heading을 사용하며, unresolved finding에만 `Why unresolved`를 추가합니다. `author`는 사용자가 지정하지 않으면 `<author>` placeholder로 유지됩니다.

## Source-repository verification

```bash
uv run pytest tests/skills/artifact-consistency-inspector
```

테스트는 package contract와 deterministic scenario를 검증합니다. 실제 모델의 원격 저장소 탐색·추론 품질은 별도 live evaluation 대상입니다.

## Runtime references

- `references/inspection-rules.md` — gap 분류와 adversarial verification
- `references/rule-sources.md` — ordered `rule_sources`, `auto` expansion, conflict handling
- `references/report-format.md` — filename, front matter, report body
- `references/example-report.md` — 허구 evidence 기반 출력 예시
