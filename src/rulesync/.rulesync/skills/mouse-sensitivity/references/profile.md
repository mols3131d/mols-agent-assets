# User Profile

Profile은 반복 상담에서 다시 확인할 필요가 없는 사용자 설정을 보존하는 선택적 JSON context다. 실제 파일과 lifecycle은 사용자 또는 workspace가 소유한다.

## Shape

`../assets/profile.example.json`은 starter shape와 기본 게임 목록만 보여 주는 예시다. 실제 사용자의 DPI, 모니터, 마우스패드와 감도를 대표하지 않는다.

모르는 값은 추측하거나 placeholder로 채우지 말고 생략한다. JSON field order는 의미 계약이 아니지만 사람이 읽기 쉽도록 example과 새 profile은 다음 순서를 권장한다.

```text
version → mouse → mousepad → os → displays → games
```

## Fields

- `version`: profile shape revision.
- `mouse.dpi`: 현재 기본 DPI/CPI.
- `mousepad.width_mm`, `mousepad.height_mm`: 패드의 물리 크기(mm).
- `os.platform`: pointer setting을 해석하는 데 필요한 OS 식별자.
- `os.pointer_speed`: optional. OS가 노출하는 native 값이나 사용자가 확인한 `default` 상태를 그대로 보존한다.
- `os.acceleration`: optional. OS pointer acceleration/enhancement 사용 여부. 단순 boolean으로 의미를 보존할 수 없으면 해당 플랫폼 의미를 유지할 수 있는 형태를 사용한다.
- `displays[].name`: 사용자가 구분하기 위한 local label.
- `displays[].primary`: primary display 여부.
- `displays[].resolution`: `[width, height]` 물리 픽셀 해상도.
- `displays[].scale`: OS display scale multiplier. 예: `1.75`는 175% scaling.
- `games.<id>.input_context`: optional routing hint. `first-person`, `third-person`, `pointer` 같은 descriptive label을 사용할 수 있지만 closed enum이 아니다. mixed/ambiguous game은 생략할 수 있다.
- `games.<id>.sensitivity`: optional. 단일 감도만 쓰면 해당 게임의 native sensitivity 숫자를 기록한다. 여러 감도 단계를 쓰면 object form을 사용할 수 있다. 같은 field 이름이라도 서로 다른 게임의 숫자는 직접 비교하지 않는다.
- `games.<id>.sensitivity.default`: object form의 기준 native sensitivity 숫자.
- `games.<id>.sensitivity.relative.<name>`: `default` 대비 변화량. `+15.4%`, `-7.7%`처럼 부호 있는 percentage string으로 기록한다. `slow`, `fast`, `very_fast` 같은 이름은 사용자 정의 label이며 closed enum이 아니다.
- `games.<id>.sensitivity.heroes.<hero>`: optional. 공통 relative 단계로 표현하지 않는 영웅별 native sensitivity 숫자.

Relative 값은 `default × (1 + percentage / 100)`으로 해석한다. relative 항목에 계산된 native sensitivity나 eDPI를 중복 저장하지 않는다.

FOV, ADS multiplier, scope처럼 추가 game setting이 실제로 필요하면 해당 game entry에 그 게임의 native 의미를 보존해 기록한다. 서로 다른 게임의 설정을 universal schema로 억지로 정규화하지 않는다.

## Use

- Profile은 현재 상태의 evidence다. 사용자가 더 최신 값을 말하면 그 값을 우선한다.
- 사무/코딩 작업에서는 필요한 `mouse`, `os`, `displays`만 읽는다.
- 게임 작업에서는 필요한 `mouse`, `mousepad`, 해당 game entry를 우선 읽고 OS setting은 실제 game input에 적용될 때만 사용한다.
- 게임 간 변환에서도 native sensitivity를 원본 값으로 보존한다. 환산값이나 `cm/360`으로 덮어쓰지 않는다.
- 갱신할 때는 확인된 값만 바꾸고 task와 무관한 필드나 알 수 없는 extension을 보존한다.
- Schema validation이나 migration이 실제로 필요해질 때만 별도 schema/validator를 추가한다.
