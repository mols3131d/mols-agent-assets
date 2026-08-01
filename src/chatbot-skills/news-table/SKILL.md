---
name: news-table
description: >
  This skill helps users quickly discover important and recent trends on multiple topics by researching news and information. Use it when you want curated, up-to-date insights on specific subjects, with the option to specify the number of articles and relevant sources.
---

## Purpose

사용자가 원하는 여러 주제의 중요한 최신 동향을 빠르게 파악할 수 있도록 뉴스와 새로운 정보를 조사한다.

## Input

사용자는 하나 이상의 주제와 각 결과 개수를 함께 지정할 수 있다.

예:

```text
에이전트 활용 개발 효율성 향상 팁 및 관련 뉴스 10개
데이터 엔지니어링·인공지능 관련 뉴스 5개
기타 개발 기술 뉴스 5개
```

필요한 입력:

1. **Topics**: 하나 이상의 조사 주제
1. **Count**: 주제별 결과 개수
1. **Freshness**: 검색 기간
1. **Source Policy**: 허용하거나 제외할 출처
1. **Format**: 출력 형식

## Defaults

* Freshness: 최근 2주
* Region / Language: 주제에 따라 자동 결정
* Count: 사용자 지정
* Tone: 간결한 분석형
* Exclude: 개인 블로그, SNS, 홍보성 게시글
* Deduplication: 동일 사건은 하나로 통합
* Verification: 가능한 경우 독립적인 출처 2개 이상으로 교차검증

## Research Workflow

1. 입력에서 주제와 주제별 결과 개수를 식별한다.
1. 각 주제를 독립적으로 조사한다.
1. 공식 발표, 원문, 주요 언론, 전문 매체를 우선한다.
1. 동일 사건을 하나의 항목으로 통합한다.
1. 핵심 주장과 시점을 출처 간 비교한다.
1. 추천도가 높은 순서로 주제별 결과를 정리한다.
1. 모든 출처를 문서 최하단에 모아 나열한다.

## Source Fallback

신뢰할 수 있는 자료만으로 요청 개수를 충족하지 못하면 낮은 신뢰도의 출처를 제한적으로 포함한다.

* 해당 뉴스에 `검증 제한`을 표시한다.
* 확인되지 않은 내용을 사실처럼 표현하지 않는다.
* 단독 SNS 주장과 출처 없는 재인용은 제외한다.
* 출처가 약한 이유를 Sources에 표시한다.
* Score를 보수적으로 평가한다.

## Output

각 주제마다 별도의 `##` 섹션을 만든다.

```markdown
## 에이전트 활용 개발 효율성

| <yyyy> | News | Score |
|---|---|---:|
| 07-31 | **핵심 소식¹** — 무엇이 달라졌으며 왜 주목할 만한지 설명한다. | 5 |

## 데이터 엔지니어링·인공지능

| <yyyy> | News | Score |
|---|---|---:|
| 07-30 | **핵심 소식²** — 새로운 변화와 실질적인 의미를 설명한다. | 4 |

---

## Sources

1. 출처명 — 핵심 근거  
   보조 출처명 — 교차검증 근거

2. 출처명 — 핵심 근거
```

## Field Rules

* `<yyyy>`: 실제 뉴스 연도로 치환하며 값은 `MM-DD`
* `News`: 핵심 소식, 새로운 변화, 주목할 이유를 하나의 셀에 작성
* `Score`: `1–5` 정수형 추천도

## Source Rules

* 각 뉴스에 위 첨자 번호를 붙인다.
* 번호는 주제마다 초기화하지 않고 문서 전체에서 연속으로 부여한다.
* 모든 출처는 마지막 주제 이후 구분선 아래 `## Sources`에 나열한다.
* 하나의 뉴스에 여러 출처가 있으면 같은 번호 아래 함께 기록한다.

## Quality Rules

* 각 결과는 가장 적합한 하나의 주제에만 배치한다.
* 주제 간 중복 뉴스는 반복하지 않는다.
* 실제로 새롭게 발생한 변화를 우선한다.
* 단순 재게시, 홍보성 발표, 내용 없는 예고는 제외한다.
* 사실, 분석, 추론을 구분한다.
* 충돌하는 보도가 있으면 차이를 명시한다.
* 근거가 부족하면 확정적으로 표현하지 않는다.
