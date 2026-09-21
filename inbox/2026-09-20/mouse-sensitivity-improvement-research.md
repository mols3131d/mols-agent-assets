# `mouse-sensitivity` 개선 Run — Research

## Findings

### 1. Gaming scope가 metadata보다 좁다

`SKILL.md`는 `games` 전반을 activation 대상으로 삼지만 현재 `gaming.md`의 tuning 언어는 camera, turn, tracking, ADS를 중심으로 한다. MOBA/RTS/isometric처럼 pointer/cursor를 직접 쓰는 게임도 같은 Skill 책임 안에 들어오므로 generic gaming layer가 이를 수용해야 한다.

별도 `pointer-game.md`를 추가할 독립 loading 가치는 아직 없다. 일반 gaming reference 안에서 input context를 먼저 구분하면 충분하다.

### 2. `games.<id>.type`은 장르 enum처럼 읽힌다

현재 profile 문서는 `first-person` 또는 `third-person`을 사용한다고 적어 사실상 closed enum처럼 보인다. 그러나 이 필드의 역할은 게임 장르 분류가 아니라 어떤 mouse-input 판단을 우선할지 알려 주는 routing hint다.

따라서 `type`을 optional `input_context`로 바꾸고 `first-person`, `third-person`, `pointer` 같은 값은 예시일 뿐 exhaustive enum이 아니라고 명시한다. 한 label로 설명하기 어려운 mixed game은 필드를 생략할 수 있다.

### 3. Entrypoint에 conditional gaming detail이 남아 있다

`SKILL.md`의 `cm/360`, eDPI, mousepad, pro setting, cross-game research와 profile update detail은 모든 activation에 필요하지 않다. Agent Asset 설계 원칙에 따라 entrypoint에는 activation 이후 applicability와 다음 context를 좁히는 정보만 남기고, domain detail은 이미 존재하는 references로 이동하는 편이 낫다.

### 4. Example과 실제 profile ownership은 분리됐지만 concrete 값이 불필요하게 많다

Starter example은 shape와 default game list를 보여 주면 충분하다. OS pointer speed/acceleration처럼 사용자가 따로 확인해야 하는 optional 값까지 예제에 넣으면 example이 실제 profile처럼 보일 수 있다.

Default example에서는 확인이 필요한 optional 값과 game sensitivity를 생략한다. 사용자가 지정한 default game list인 Counter-Strike 2, Overwatch 2, Valorant는 유지한다.

### 5. Config order는 physical input → environment → workload가 자연스럽다

다음 순서를 사용한다.

```text
version
mouse
mousepad
os
displays
games
```

Display entry는 `name → primary → resolution → scale`, game entry는 routing hint인 `input_context`를 먼저 두고 실제 native setting은 확인된 경우에만 추가한다.

### 6. Conversion reference의 고정 URL은 runtime contract에 필수적이지 않다

사용자 요구는 converter/formula를 Skill에 내장하는 것이 아니라 변환 요청이 있을 때 외부를 조사하는 것이다. 고정 `Useful Sources` 목록은 stale maintenance surface가 되므로 제거하고 source selection 원칙만 남기는 편이 더 작고 오래 간다.

Current external converter/tool은 PR research evidence로는 유효하지만 canonical runtime instruction의 dependency일 필요는 없다.

### 7. Generated projection 실패는 source correctness와 별개인 deterministic blocker다

최근 PR Gate에서 frontmatter validation과 236 tests는 통과했고 `distribution-routes`만 `route/skills.jsonl` outdated로 실패했다. 공식 generator는 모든 `*/SKILL.md` frontmatter의 `name`, `description`을 name 기준 정렬해 route를 생성한다. 최종 description 변경 후 이 generator semantics로 projection을 다시 생성해야 한다.

## Decisions

1. Skill은 하나로 유지한다.
2. `gaming.md`가 `camera/aiming`, `pointer/cursor`, mixed input context를 구분한다.
3. FPS/TPS references는 조건부 detail로 유지한다.
4. `games.<id>.type` → `games.<id>.input_context`로 바꾼다.
5. `input_context`는 optional descriptive hint이며 closed enum으로 만들지 않는다.
6. `SKILL.md`는 Route + 최소 Core + 짧은 Procedure + Boundary로 축소한다.
7. Example은 neutral starter shape로 유지하고 개인 sensitivity/monitor/mousepad 값을 복제하지 않는다.
8. Conversion은 요청 시 current external research를 수행하고 repository에 converter DB, coefficient table, 고정 source list를 소유하지 않는다.
9. Text optimization은 위 의미 변경이 끝난 뒤 구조와 technical token을 보존하는 마지막 wording pass로 수행한다.
