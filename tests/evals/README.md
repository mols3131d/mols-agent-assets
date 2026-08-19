# Eval 테스트

평가 fixture를 위한 저장소 소유의 결정론적 검사입니다.

- `evals/skills/**/*.json`은 유효한 JSON으로 파싱되어야 합니다.
- Skill별 결정론적 동작 검사는 `tests/skills/<skill-name>/`에 둡니다.
- 이 검사는 model 기반 평가를 수행하거나 보장한다는 뜻이 아닙니다.
