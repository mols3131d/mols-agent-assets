# Text Bars

Progress bar와 horizontal bar는 Markdown source에서도 빠르게 읽히는 compact visual이다.
정확한 수치와 같은 scale을 함께 표시한다.

## Progress Bars

현재값과 전체값이 명확한 완료율, 사용률, coverage 또는 목표 달성률에 사용한다.

```text
Overall    ████████░░  80%  8/10
Transform  ██████░░░░  60%  6/10
Load       ░░░░░░░░░░   0%  0/10
```

- 기본 width는 10칸이다.
- 채움은 `█`, 빈 영역은 `░`를 사용한다.
- `%`와 `current/total` 중 가능한 근거를 표시한다.
- 같은 block에서 width와 기준을 통일한다.
- 분모가 없으면 임의의 percentage를 만들지 않는다.

## Horizontal Bars

약 2~6개 category의 비교 가능한 단일 수치, 순위와 격차를 보여줄 때 사용한다.

```text
Python      ███████████████  48 jobs
TypeScript  ███████████      35 jobs
SQL         ██████           19 jobs
Rust        ███               8 jobs
```

- 0에서 시작하는 선형 scale을 사용한다.
- 가장 큰 값을 기본 최대 width 20칸에 맞춘다.
- 정확한 값, 단위와 집계 기준을 표시한다.
- 순위가 목적이면 내림차순으로 정렬한다.
- 음수, 양방향 변화, 불확실성 또는 서로 다른 단위에는 사용하지 않는다.

추세, 많은 category 또는 복잡한 축은 `mermaid-chart`를 사용한다.
동일 정보를 table이나 chart와 중복 표현하지 않는다.
