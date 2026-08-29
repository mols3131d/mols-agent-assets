# Clarify Code — Enhancement Research

이 문서는 `clarify-code`를 **실행 코드를 바꾸지 않고 code-adjacent explanation으로 이해 비용을 줄이는 Skill**로 고도화하기 위한 조사 기록입니다.

초안을 먼저 작성한 뒤, program comprehension·code comment quality·rationale·API documentation 연구와 repository 원칙을 추가로 조사해 갱신했습니다.

## 결론

`clarify-code`의 다음 개선은 comment/docstring을 더 많이 생성하는 방향이 아니라, **설명이 실제로 제거하는 comprehension cost를 먼저 확인하고 그 의미를 가장 적절한 source surface에 최소한으로 남기는 방향**이 적합합니다.

핵심 판단은 다음과 같습니다.

> 설명은 무료 정보가 아니다. Reader의 attention과 유지보수 비용을 소비하므로, code만으로 안정적으로 복원하기 어려운 contract·constraint·rationale·consequence를 전달해 추론·탐색·오해 비용을 실질적으로 줄일 때만 가치가 있다.

`code-comprehension-refactor`와의 책임은 다음처럼 대칭적으로 유지하는 것이 가장 명확합니다.

```text
code-comprehension-refactor
→ executable code에서 불필요한 mental reconstruction을 제거한다.

clarify-code
→ code 자체를 바꾸지 않아야 하거나 바꿀 필요가 없는 상황에서,
  code만으로 안정적으로 복원하기 어려운 의미를 가까운 explanation surface에서 제거한다.
```

새로운 comment framework나 점수 모델은 필요하지 않습니다. 현재 `clarify-code`의 `SKILL.md`와 `references/documentation.md`를 작은 local delta로 고도화하고 capability eval을 보강하는 것이 충분합니다.

## 무엇이 새롭게 확인되었나

### Comment는 context에 따라 이해를 돕기도, 방해하기도 한다

2026년 Empirical Software Engineering의 eye-tracking 연구는 Java snippet 12개를 comment 유무로 비교했습니다. Comment가 있는 경우 comprehension performance의 변화는 snippet에 따라 **약 30% 감소부터 34% 증가까지** 넓게 나타났습니다. Comment는 visual attention의 최대 약 23%를 차지했고 reading order에도 영향을 주었지만, 참가자가 comment를 유용하다고 평가한 것과 실제 performance 향상이 항상 일치하지는 않았습니다.

참가자들은 대체로 code-first 전략을 사용했고, comment가 복잡한 부분의 context와 intention을 설명할 때 유용하다고 평가한 반면 쉽게 이해되는 line을 다시 말하는 comment는 도움이 되지 않는다고 보았습니다.

이 연구는 학생 20명과 짧은 snippet을 대상으로 했고 실험상 매우 높은 comment density를 사용했으므로 실제 대형 codebase에 그대로 일반화해서는 안 됩니다. 그럼에도 **comment의 존재 자체가 comprehension improvement가 아니며 relevance·quality·context가 중요하다**는 방향은 강하게 지지합니다.

Source: Abdelsalam et al., *The Effect of Comments on Program Comprehension: An Eye-tracking Study*, Empirical Software Engineering, 2026.
https://link.springer.com/article/10.1007/s10664-025-10721-2

### “Right information, right time, right place”는 탐색 비용을 줄인다

Adeli et al.의 VL/HCC 2020 연구는 code, documentation 등 관련 정보가 여러 interface에 흩어질 때 developer가 정보를 찾고 관계를 연결하면서 mental model을 구성해야 한다는 점에 주목했습니다. 22명의 newcomer를 대상으로 한 study에서는 필요한 정보를 관련 위치와 시점에 제공하는 annotation interaction이 traditional IDE 대비 comprehension accuracy를 높이고 cognitive load를 낮췄습니다.

이 결과가 inline comment placement 규칙을 직접 검증한 것은 아닙니다. 하지만 `clarify-code`에서 **독자가 explanation과 적용 대상을 다시 연결하기 위해 별도 탐색을 하지 않도록 locality를 고려해야 한다**는 근거가 됩니다.

Source: Adeli et al., *Supporting Code Comprehension via Annotations: Right Information at the Right Time and Place*, VL/HCC 2020.
https://austinhenley.com/pubs/Adeli2020VLHCC_Annotations.pdf

### Non-local comment는 실제 comment smell로 관찰되지만 절대 규칙은 아니다

2024년 Empirical Software Engineering의 inline comment smell 연구는 8개 project의 comment를 수작업 분석하고 practitioner survey를 수행했습니다. Taxonomy에는 다음 smell이 포함됩니다.

- obvious — code를 다시 말함
- irrelevant — code/project 이해에 정보를 주지 않음
- too much information — history나 과도한 detail이 많음
- non-local — 가까운 code가 아니라 멀리 떨어진 부분이나 system-wide detail을 설명함
- vague — comment 자체가 이해하기 어려움
- misleading — code와 모순되거나 잘못된 의미를 전달함

특히 obvious comment가 가장 자주 관찰됐고, survey에서는 misleading comment가 maintainability/comprehension에 가장 부정적이라는 응답이 높았습니다. 연구팀은 non-local smell fix에서 comment를 실제 관련 code 위치로 옮기는 PR을 만들기도 했습니다.

다만 practitioner 중 일부는 큰 codebase에서 non-local information이나 긴 explanation이 unfamiliar developer에게 도움이 될 수 있다고 답했습니다. 따라서 `clarify-code`는 **“comment는 항상 바로 옆이어야 한다” 또는 “긴 comment는 항상 나쁘다”로 규칙화하면 안 됩니다.**

적절한 판단은 다음에 가깝습니다.

> 의미가 local하다면 가까운 surface를 선호하되, 여러 symbol에 걸친 stable context라면 더 넓은 owner가 더 적절할 수 있다. 위치는 거리 자체가 아니라 reader가 관계를 다시 복원해야 하는 비용과 ownership 안정성으로 판단한다.

Source: Jabrayilzade et al., *Taxonomy of inline code comment smells*, Empirical Software Engineering, 2024.
https://link.springer.com/article/10.1007/s10664-023-10425-5

### Comment quality를 하나의 단일 metric으로 환원하기 어렵다

2023년 systematic literature review는 2011–2020년 comment quality 연구 47편을 분석해 21개의 quality attribute를 확인했습니다. 가장 자주 다뤄진 속성은 consistency, completeness, readability였으며, 연구의 상당수가 특정 언어나 특정 comment type에 제한됐습니다.

이는 comment density, comment coverage, 길이 같은 하나의 proxy로 `clarify-code` behavior를 결정하는 접근이 약하다는 근거입니다.

Source: Rani et al., *A decade of code comment quality assessment: A systematic literature review*, Journal of Systems and Software, 2023.
https://www.sciencedirect.com/science/article/pii/S0164121222001911

### Stale comment는 단순 readability 문제가 아니라 잘못된 evidence가 된다

Code-comment consistency 연구는 code 변경 시 comment가 같이 갱신되지 않아 obsolete/misleading comment가 생기는 문제를 반복적으로 다뤄 왔습니다. 2024/2025 CoCC 연구는 outdated comment detection을 다루며 inconsistent comment가 후속 developer를 오도할 수 있음을 문제로 정의했습니다. 2025년 SEOCD 연구도 obsolete comment를 독립적인 maintenance problem으로 다룹니다.

2017년 fragile comment 연구는 rename refactoring 이후 comment 안의 textual identifier reference가 자동으로 안전하게 갱신되지 않는 문제를 분석했습니다. 즉 comment가 code detail에 강하게 결합될수록 future refactor에서 쉽게 깨질 수 있습니다.

이 근거를 `clarify-code`에 그대로 automated consistency checker로 옮길 필요는 없습니다. 대신 **comment가 implementation wording, identifier spelling, 일시적인 구조에 불필요하게 결합되어 stale risk를 높이지 않는지**를 판단하도록 하는 정도가 적절합니다.

Sources:

- Huang et al., *Are your comments outdated? Toward automatically detecting code-comment consistency*, Journal of Software: Evolution and Process, 2025.
  https://onlinelibrary.wiley.com/doi/10.1002/smr.2718
- Cui et al., *SEOCD: Detecting obsolete code comments by fusing semantic features and expert features*, Expert Systems with Applications, 2025.
  https://www.sciencedirect.com/science/article/pii/S0957417425010929
- Ratol & Robillard, *Detecting Fragile Comments*, ASE 2017.
  https://www.cs.mcgill.ca/~martin/papers/ase2017.pdf

### Rationale는 단순한 “why”보다 훨씬 구체적인 정보 요구다

2022년 Journal of Systems and Software 연구는 developer가 code commit rationale을 찾을 때 필요로 하는 정보를 15개 component로 분해했습니다. 여기에는 goal, need, benefits, **constraints, alternatives, selected alternative, dependencies, validation, side effects** 등이 포함됩니다.

연구 참여자들은 rationale을 자주 찾았고 어려운 경우 찾는 데 20분 이상을 쓰기도 했습니다. 특히 side effects와 alternatives는 찾기 어려운 정보였고, alternatives·selected alternative·constraints는 필요한데도 잘 기록되지 않는 경향이 있었습니다.

이 연구는 commit rationale에 대한 것이므로 “모든 rationale를 source comment에 적어라”는 근거가 아닙니다. 오히려 반대입니다. `clarify-code`에서는 **현재 code를 안전하게 이해하거나 변경하는 데 반복적으로 필요한 durable rationale만 local explanation 후보**로 삼아야 합니다.

특히 다음은 높은 가치의 code-local explanation 후보가 될 수 있습니다.

- 현재도 유효한 constraint
- observable side effect 또는 caller consequence
- statement/order가 달라지면 깨지는 invariant
- maintainer가 자연스럽게 선택할 법하지만 현재 constraint 때문에 잘못된 alternative

반면 committer, time, 과거 discussion처럼 Git history가 더 적절한 정보는 source comment로 복제하지 않습니다.

Source: Al Safwan et al., *Developers’ need for the rationale of code commits: An in-breadth and in-depth study*, Journal of Systems and Software, 2022.
https://www.sciencedirect.com/science/article/pii/S0164121222000668

### Negative knowledge는 가치가 있지만 “history dump”와 구분해야 한다

Design rationale literature에서도 rationale는 최종 decision뿐 아니라 justification과 alternatives considered를 포함하는 정보로 다뤄집니다. Maintenance에서는 “왜 이렇게 했는가?”뿐 아니라 “왜 obvious alternative를 사용하지 않았는가?”가 미래 변경에서 중요할 수 있습니다.

하지만 source comment가 과거의 모든 대안을 기록하는 log가 되면 too-much-information과 staleness 문제가 생깁니다.

따라서 `clarify-code`에서 rejected alternative를 다룰 때는 다음 boundary가 필요합니다.

> 과거에 검토했다는 사실이 아니라, 미래 maintainer가 다시 선택할 가능성이 높고 현재도 유효한 constraint 때문에 그 선택이 잘못되는 경우에만 그 이유를 남긴다.

이것을 **negative knowledge**로 볼 수 있습니다.

### API docstring은 implementation 설명보다 caller contract를 소유하는 것이 자연스럽다

Oracle의 Javadoc guidance는 API specification을 caller와 implementation 사이의 contract로 설명하고, caller가 의존할 수 있는 behavior를 기술하되 implementation detail을 피하도록 안내합니다. Boundary condition, argument range, corner case, exception, thread-safety 같은 내용이 대표적인 contract 정보입니다.

Python PEP 257도 function/method docstring이 behavior뿐 아니라 applicable한 arguments, return values, side effects, exceptions, call restrictions를 설명할 수 있다고 안내합니다.

이는 현재 `clarify-code`의 caller/maintainer 분리가 적절하다는 근거입니다.

- caller-visible semantics → docstring
- maintainer-only implementation rationale → inline/local comment

다만 모든 public symbol에 docstring을 강제하는 규칙을 가져올 필요는 없습니다. Repository/user convention이 우선이며, `clarify-code`는 **non-obvious information need가 있을 때의 content judgment**를 소유하면 충분합니다.

Sources:

- Oracle, *How to Write Doc Comments for the Javadoc Tool*.
  https://www.oracle.com/java/technologies/javase/writing-doc-comments.html
- PEP 257 — Docstring Conventions.
  https://peps.python.org/pep-0257/

## 최종 판단 모델

심층 조사 후 `clarify-code`에 가장 적합한 모델은 복잡한 taxonomy가 아니라 다음 세 질문입니다.

### 1. Explanation Value — 이 설명이 어떤 비용을 제거하는가?

설명이 없으면 reader가 해야 하는 작업을 먼저 찾습니다.

- 다른 symbol/file/document/history 탐색
- hidden caller semantics 추론
- ordering/exception/side-effect consequence 추론
- unusual implementation의 constraint 추측
- 자연스럽지만 잘못된 alternative 검토

그 작업이 material하지 않거나 code가 이미 직접 표현한다면 comment/docstring을 추가하지 않는 것이 기본입니다.

이를 개념적으로는 다음처럼 볼 수 있습니다.

```text
explanation value
≈ removed inference/search/misunderstanding cost
  - reading/attention/maintenance/staleness cost
```

실제 점수를 계산하지 않습니다. Explanation을 추가할 가치가 있는지 판단하는 lens일 뿐입니다.

### 2. Information Type — 무엇을 설명해야 하는가?

`why`라는 넓은 표현보다 다음 정보가 더 operational합니다.

| Reader | High-value information |
| --- | --- |
| Caller | hidden contract, boundary condition, side effect, exception meaning, overwrite/idempotency/caching semantics, call restriction |
| Maintainer | invariant, constraint, ordering consequence, external system limitation, intentional unusual choice, durable rejected alternative |

Code가 직접 표현하는 control/action narration은 기본적으로 제외합니다.

### 3. Placement and Scope — 어디까지 적용되는 의미인가?

의미와 explanation의 scope를 맞춥니다.

| Meaning scope | Preferred owner |
| --- | --- |
| 한 API의 caller contract | 해당 docstring |
| 한 branch/operation/order의 local rationale | 해당 code 근처 comment |
| file 전체에 실제로 적용되는 local convention | module-level explanation |
| 여러 module에 걸친 architecture/domain policy | canonical documentation; source에는 필요한 projection만 |

가까운 위치는 default이지 절대 규칙이 아닙니다. 여러 symbol에 안정적으로 적용되는 context를 개별 comment에 반복하는 것보다 적절한 상위 owner가 낫습니다.

## 설명의 수명도 의미와 맞춰야 한다

설명이 얼마나 쉽게 stale 되는지는 **무엇에 결합되어 있는가**와 관련됩니다.

상대적으로 안정적인 설명:

- durable invariant
- external protocol constraint
- caller-visible contract
- 현재도 유효한 rejected alternative의 constraint

상대적으로 fragile한 설명:

- line-by-line implementation narration
- identifier spelling을 불필요하게 반복하는 prose
- temporary algorithm step
- issue/history 상태를 현재 behavior처럼 기술
- 넓은 policy를 local code 구조에 맞춰 복제

따라서 단순히 comment를 짧게 만드는 것보다 **stable semantic에 연결하는 것**이 더 중요합니다.

## 현재 `clarify-code` 평가

현재 branch의 Skill은 이미 다음을 잘 소유합니다.

- code-adjacent prose only라는 mutation boundary
- structural opacity → `code-comprehension-refactor`
- caller contract → docstring
- maintainer rationale → comment
- module-local explanation
- canonical policy의 local projection
- machine-consumed comment/docstring 구분
- code narration·stale explanation 억제

남은 gap은 주로 **설명을 추가하기 전 가치 판단과 위치/scope 판단을 명시적으로 operationalize하지 않은 것**입니다.

따라서 큰 rewrite는 필요하지 않습니다.

## 최종 개선 권고

### P1 — `Explanation Value`를 first-class judgment로 추가

설명 추가 전 다음을 묻게 합니다.

- 이 설명이 없으면 reader가 무엇을 추론하거나 찾아야 하는가?
- 그 비용이 material한가?
- explanation이 그 비용을 실제로 줄이는가?
- code/name/type이 이미 같은 의미를 충분히 전달하는가?

No-op이 정상적인 성공 결과가 될 수 있어야 합니다.

### P1 — `Placement and Scope`를 추가

의미가 적용되는 가장 좁고 안정적인 owner를 선택합니다.

Local meaning은 가까운 comment/docstring을 선호하되, 여러 symbol에 걸친 durable policy는 적절한 상위 owner로 보냅니다.

### P1 — Comment 대상의 표현을 `why`에서 constraint/consequence/rationale로 정교화

현재 comment section을 다음 중심으로 보강합니다.

- invariant / constraint
- ordering consequence
- external limitation
- intentional unusual choice
- durable rejected alternative

“왜”라는 단어를 없앨 필요는 없지만 행동 판단은 더 구체적인 information type을 사용합니다.

### P2 — stale-risk를 Final Pass에서 더 직접 확인

다음을 확인합니다.

- code와 현재 설명이 모순되는가?
- identifier/implementation detail에 필요 이상으로 결합됐는가?
- semantic보다 code structure가 먼저 바뀔 때 쉽게 거짓말이 되는가?

별도 consistency analyzer나 automatic checker를 만들지는 않습니다.

### P2 — capability eval에 locality/scope와 negative knowledge를 추가

현재 eval은 obvious comment, caller contract, rationale, structural boundary와 machine-consumed text를 이미 다룹니다.

추가 가치가 큰 case는 다음 정도입니다.

- high-value rejected alternative
- local rationale를 먼 module comment에 쓰려는 request
- 실제 invariant보다 scope가 넓은 comment
- stale implementation narration을 현재 constraint 중심으로 교정
- information need가 없는 comment request에서 no-op

## 권고하지 않는 것

- `comment-design.md` 같은 새 reference 추가
- comment quality score 또는 formula
- comment density/coverage target
- 모든 public API docstring 강제
- 항상 comment를 짧게 만들기
- 항상 inline/local 위치 강제
- 모든 rejected alternative 기록
- Git history를 source comment로 복제
- automated stale-comment detector 구축
- `code-comprehension-refactor`의 executable-code 책임을 다시 가져오기

## Repository 원칙과의 정합성

Repository의 Agent Asset Design Principles는 context가 무료가 아니며 실제 failure를 막거나 invariant/boundary를 보존하거나 중요한 판단을 바꾸는 정보만 local context로 유지하도록 합니다. 이 원칙은 `clarify-code` 자체에도 그대로 적용할 수 있습니다.

즉 좋은 code comment는 일종의 **local context**이며, 다음 조건을 충족해야 합니다.

- 없으면 material한 comprehension cost가 발생함
- 가장 적절한 owner에 있음
- 같은 semantic concern을 다른 곳과 중복 소유하지 않음
- 실제 판단을 바꾸지 않는 prose가 아님

Instruction Design의 “서로 의존하는 condition, behavior, boundary를 가까이 둔다”는 원칙도 explanation locality와 자연스럽게 일치합니다.

## Research Limitations

- Comment comprehension 연구 중 상당수는 학생, 짧은 snippet, Java 중심입니다.
- Comment quality literature는 Java 및 특정 comment type에 편향되어 있습니다.
- Rationale 연구는 commit history를 대상으로 하므로 source comment placement의 직접 근거가 아닙니다.
- API documentation guidance는 언어별 ecosystem contract가 다르므로 universal formatting rule로 가져오면 안 됩니다.
- 따라서 이번 개선은 특정 syntax/style을 강제하지 않고 **value, information type, placement/scope라는 portable judgment**만 가져오는 것이 적절합니다.

## Sources

- Abdelsalam et al., *The Effect of Comments on Program Comprehension: An Eye-tracking Study*, 2026 — https://link.springer.com/article/10.1007/s10664-025-10721-2
- Adeli et al., *Supporting Code Comprehension via Annotations: Right Information at the Right Time and Place*, 2020 — https://austinhenley.com/pubs/Adeli2020VLHCC_Annotations.pdf
- Jabrayilzade et al., *Taxonomy of inline code comment smells*, 2024 — https://link.springer.com/article/10.1007/s10664-023-10425-5
- Rani et al., *A decade of code comment quality assessment: A systematic literature review*, 2023 — https://www.sciencedirect.com/science/article/pii/S0164121222001911
- Al Safwan et al., *Developers’ need for the rationale of code commits: An in-breadth and in-depth study*, 2022 — https://www.sciencedirect.com/science/article/pii/S0164121222000668
- Ratol & Robillard, *Detecting Fragile Comments*, 2017 — https://www.cs.mcgill.ca/~martin/papers/ase2017.pdf
- Huang et al., *Are your comments outdated? Toward automatically detecting code-comment consistency*, 2025 — https://onlinelibrary.wiley.com/doi/10.1002/smr.2718
- Cui et al., *SEOCD: Detecting obsolete code comments by fusing semantic features and expert features*, 2025 — https://www.sciencedirect.com/science/article/pii/S0957417425010929
- Oracle, *How to Write Doc Comments for the Javadoc Tool* — https://www.oracle.com/java/technologies/javase/writing-doc-comments.html
- PEP 257 — https://peps.python.org/pep-0257/

## Status

Deep research update complete. 이 문서는 구현 방향을 결정할 충분한 근거가 있으며, 추가 source가 현재 P1/P2 판단을 크게 바꿀 가능성은 낮습니다.
