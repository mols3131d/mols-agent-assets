# Workflow and Review Contract

워크플로는 **단계 순서와 의존성**을 소유한다. Artifact Registry는 유형·파일명만 소유하며 workflow 순서나 단계 이동 정책을 포함하지 않는다.

## Definition

[Default workflow](../assets/workflows/default.json)은 다음 8단계로 구성된다.

```text
proposal → research → plan → specification → test-design
         → test-implementation → code-implementation → review
```

[Focused workflow](../assets/workflows/focused.json)은 기존 문서·테스트가 충분하거나 단일 변경이 한정된 상황에서 `specification → code-implementation → review`만 사용한다. 선택적인 단계도 필요해지면 전체 흐름으로 전환하거나 프로젝트가 정의한 workflow를 사용한다. 기본 test-first 순서가 모든 변경에서 최적이라는 주장은 아니다.

Workflow JSON의 `steps[]` 요소는 `id`(단계 ID), `artifacts`(참조하는 Registry ID 목록), `after`(선행 단계 ID 목록)를 가진다. 배열의 순서는 진행 순서이며 `after`는 특정 단계의 결과를 바꾼 경우 **재확인을 고려할 downstream 의존 관계**를 표시한다. `after`가 없는 뒤 단계는 단순히 순서상 뒤라는 이유로 자동 재검토 후보가 되지는 않는다. `review`는 반드시 마지막에 두고 Artifact를 직접 생산하지 않는다.

`after`는 데이터 영향의 **보수적 추정**이다. 미세한 의미적 의존성까지 코드를 통해 확정할 수는 없다. 프로젝트별 workflow는 표준 위치에 복제할 필요 없이 그 프로젝트의 규칙에 따라 구성할 수 있다. 새로운 파일이 없으면 bundled preset을 선택한다.

## Review Outcomes

- **PASS:** 수락 조건과 실제 검증 근거를 점검했고 미해결 중요한 finding이 없다는 후보 판정이다. 코드 실행·CI 근거가 필요한데 수행하지 않았다면 완료를 선언하지 않는다.
- **REWORK:** finding마다 원인·근거와 수정할 **가장 적절한 단계**를 지정한다. 해당 단계 및 의존하는 downstream 단계만 재확인 후보로 표시하고, 실제 영향 없는 파일은 수정하지 않는다. 여러 finding이면 workflow 순서상 가장 이른 대상부터 검토한다.
- **BLOCKED:** 필요한 권한·환경·외부 사실 등으로 현재 수행할 수 없는 경우. 누락된 근거를 PASS로 바꾸지 않고 인계한다.

실행 가능한 환경에서 다음과 같이 읽기 전용 검사를 할 수 있다.

```bash
python scripts/flow.py validate
python scripts/flow.py --workflow assets/workflows/focused.json validate
python scripts/flow.py route --review review.json
```

경로는 **Skill 패키지 디렉터리를 기준으로 한 예시**이며 상대 경로 CLI 옵션은 호출하는 쉘의 작업 디렉터리를 따른다. Script는 workflow/registry의 구조만 확인하며 파일 수정·도구 설치·테스트 실행·원격 쓰기를 하지 않는다.

Review report JSON 예시:

```json
{
  "result": "rework",
  "findings": [
    {
      "target": "specification",
      "issue": "동시성 요구 동작이 빠짐",
      "evidence": ["specification.md#concurrent-writes"]
    }
  ]
}
```

`route` 출력의 `return_to`는 복귀 지점, `recheck_steps`는 **재확인 후보**다. 예컨대 Specification 결함은 테스트 설계·테스트 코드·제품 코드·Review의 재확인으로 이어질 수 있다. 반면 테스트 코드 assertion 오류는 Specification 자체를 불필요하게 수정할 이유가 없다.

PASS 입력은 `{"result":"pass","evidence":["실제 검증 링크"],"findings":[]}` 형태이며, script는 `candidate_complete`만 반환한다. BLOCKED는 `{"result":"blocked","reason":"차단 원인"}`이다. 입력의 참조가 실제 유효하거나 테스트가 실행되었다는 것은 **스크립트가 검증하지 않는다**. Script가 없는 런타임에서도 같은 `after` 의존 관계와 finding 근거를 읽어 명시적으로 복귀·재확인을 수행한다. 자동 동등성을 주장하지 않는다.

## Return and Recheck

1. finding의 target이 현재 workflow 단계인지 확인한다. 명확하지 않으면 함부로 stage를 선택하지 않는다.
2. 명시한 `after` 관계를 따라 재확인 후보를 계산한다. 기계적 routing 결과는 **최대 검토 범위의 힌트**이지 수정 명령이 아니다.
3. 영향받은 명세·테스트·코드만 갱신하고, 원래 유지되는 계약과 회귀 조건을 검증한다.
4. 실제 근거를 확보한 뒤 다시 Review에 도달한다. 반복해도 수렴하지 않거나 권한·환경 한계가 있으면 차단·인계한다.

작업 우선순위·다른 Work Item의 진행·멀티태스크 스케줄은 이 워크플로가 소유하지 않는다.
