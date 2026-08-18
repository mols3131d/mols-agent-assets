# writing skill

목적 중심 글쓰기의 기획, 작성, 재작성, 가독성 개선, 리뷰를 수행하는 Agent Skill 패키지다.

## 구성

- `./SKILL.md`: 라우터, 실행 계약, 공용 절차, 비용·중단 기준
- `./references/principles.md`: 공용 글쓰기 원칙
- `./references/workflows.md`: 하위 워크플로우
- `./references/review-rubric.md`: 목적 적합성 리뷰 기준
- `./references/examples.md`: 라우팅과 행동 예시
- `.agents/skills/writing/assets/`: 글쓰기 브리프와 리뷰 출력 템플릿
- `./scripts/validate.py`: deployable 패키지 구조와 메타데이터 검증

Trigger evaluation fixture는 deployable package 밖 `evals/skills/writing/`에서 관리한다.

## 검증

```bash
python3 scripts/validate.py
```

Repository eval fixture까지 검증하려면 저장소 루트에서 다음을 실행한다.

```bash
uv run pytest tests/skills/writing
```

Agent Skills 참조 도구가 설치되어 있다면 추가로 다음을 실행할 수 있다.

```bash
skills-ref validate ./writing
```

## 사용

스킬을 설치한 뒤 명시적으로 선택하거나, 이메일·문서·공지·보고서·게시물 등의 기획·작성·재작성·가독성 개선·리뷰 요청에서 자동 활성화되도록 사용한다.
