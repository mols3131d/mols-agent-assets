# User Profile

Profile은 반복 상담에서 다시 측정할 필요가 없는 사용자 설정을 보존하는 선택적 JSON context다. 실제 파일의 위치와 lifecycle은 사용자 또는 workspace가 소유한다.

## Shape

기본 예시는 `../assets/profile.example.json`을 사용한다. 필드는 필요한 것만 채우며 알 수 없는 값을 추측하지 않는다. Example은 최소 shape만 보여 주며 모든 게임에 공통 schema를 강제하지 않는다.

## Semantics

- `version`: profile shape의 revision. 현재 초안은 `1`이다.
- `mouse.dpi`: 현재 기본 DPI/CPI. 감도 계산에 사용할 실제 값만 기록한다.
- `os.platform`: pointer 설정을 해석하는 데 필요한 OS 식별자다.
- `os.pointer_speed`: 해당 OS가 노출하는 native pointer-speed 값이다. 다른 OS의 같은 숫자와 직접 비교하지 않는다.
- `os.acceleration`: OS pointer acceleration/enhancement의 사용 여부다. 플랫폼이 단순 boolean으로 표현되지 않으면 실제 의미를 보존할 수 있는 형태를 사용한다.
- `displays[].name`: 사용자가 구분하기 위한 local label이다.
- `displays[].resolution`: `[width, height]` 물리 픽셀 해상도다.
- `displays[].scale`: OS display scale multiplier다. 예: `1.75`는 175% scaling을 뜻한다.
- `displays[].primary`: primary display 여부다.
- `mousepad.width_mm`, `mousepad.height_mm`: 실제 마우스 이동 공간의 물리적 상한을 판단하기 위한 패드 크기(mm)다.
- `games.<id>.type`: 현재 주로 다루는 입력 맥락. 초안에서는 `first-person` 또는 `third-person`을 사용한다.
- `games.<id>.sensitivity`: 해당 게임이 노출하는 native sensitivity 값이다. 같은 field 이름을 사용해도 서로 다른 게임의 숫자는 직접 비교하지 않는다.

게임 변환에 FOV, ADS multiplier, scope 값처럼 추가 설정이 실제로 필요하면 해당 game entry에 현재 게임의 의미를 보존한 필드로 기록할 수 있다. 모든 게임의 서로 다른 설정을 억지로 하나의 universal schema로 정규화하지 않는다.

## Use

- Profile 값은 현재 상태에 대한 evidence다. 사용자가 현재 설정이 다르다고 말하면 profile보다 현재 정보를 우선한다.
- 사무/코딩 작업에서는 필요한 `os`, `displays`, `mouse` context만 읽는다.
- 게임 작업에서는 필요한 `mouse`, `mousepad`, 해당 `games` entry만 우선 읽는다. OS pointer 설정은 게임 입력 모델에 실제로 적용될 때만 사용한다.
- 게임 간 변환에서는 각 game entry의 native sensitivity를 원본 값으로 보존하고, 변환 결과나 공통 `cm/360`을 원래 숫자의 의미처럼 덮어쓰지 않는다.
- Profile을 갱신할 때는 확인된 값만 바꾸고 다른 게임이나 알 수 없는 extension을 정리하지 않는다.
- Schema validation이나 자동 migration이 실제로 필요해질 때만 별도 schema/validator를 추가한다.
