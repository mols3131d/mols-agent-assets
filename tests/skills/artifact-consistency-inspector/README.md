# Artifact Consistency Inspector 테스트

`artifact-consistency-inspector`의 저장소 소유 결정론적 계약 테스트입니다.

## 실행

```bash
uv run pytest tests/skills/artifact-consistency-inspector
```

## 검증 범위

- 배포 가능한 package 구조와 상대 reference
- `SKILL.md` front matter와 read-only runtime 계약
- 보고서 front matter, 간결한 heading template, Summary 상태와 파일명 규칙
- 순서가 있는 `rule_sources`와 제자리 `auto` 확장
- rule-source 충돌과 inferred-convention 동작
- result와 coverage 상태 결정
- omission 안전장치와 결정론적 scenario
- ZIP 구조와 verification surface 제외

`scenarios/`는 이 테스트 묶음이 소유하는 fixture 데이터입니다. 배포 가능한 Skill package에는 복사하지 않습니다.
