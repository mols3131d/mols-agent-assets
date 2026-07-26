# Decisions

## Proposed

## Accepted

### **[책임 범위] 리뷰 문서 포맷에 집중**

- DECISION | **문서 포맷 전담** - 리뷰 결과 표현·문서 구조만 담당. 코드 수정 없음.
- REASON | **관점과 형식 분리** - 방향성·고도화 판단은 다른 전문성/스킬에 위임.
- IMPACT | **조합 전제** - 리뷰 전략을 이 스킬에 중복 정의하지 않음.

### **[문서 작성] 템플릿 주도**

- DECISION | **templates가 작성 정본** - placeholder·HTML 주석으로 작성 절차 제공.
- REASON | **단일 출처** - 작성 규칙을 템플릿과 함께 관리.
- IMPACT | **workflow 최소화** - 문서 종류별 작성 workflow를 늘리지 않음.

### **[스크립트] 결정적 작업만 자동화**

- DECISION | **스크립트 = 결정적 작업** - 경로·생성·구조 검증 등 반복 가능 작업만 스크립트.
- REASON | **모델 비용·편차 감소** - 추론과 기계 작업을 분리.
- IMPACT | **최소 자동화** - 의미 판단은 모델. 유지비 > 이득이면 자동화 안 함. 계약 세부 = [spec.md](spec.md).

### **[검증] 주석 검사 범위**

- DECISION | **본문 HTML 주석만 검사** - 잔여 템플릿 지침 차단. FM YAML `#` 주석은 검사하지 않음.
- REASON | **HTML 경계 안정 / YAML `#` 모호** - 값 내부 `#`과 주석 구분 비용 큼.
- IMPACT | **validator 범위** - HTML 남으면 fail. YAML 주석 정책은 Deprecated 이력 참고.

### **[Config] 스킬 본체와 설정 분리**

- DECISION | **동작 조절은 config** - 저장 경로·검증 엄격도 등을 설정으로 변경.
- REASON | **환경별 요구** - 공통 스킬 수정 없이 프로젝트/사용자 맞춤.
- IMPACT | **키·경로는 spec/configure** - 계층 구현은 skill 정책. 공통 권장과 다르면 skill이 우선.

### **[포맷] rumdl 실패 비차단**

- DECISION | **검증 후 포맷 시도, 실패 무시 가능** - rumdl은 품질 보조.
- REASON | **리뷰 산출 차단 금지** - 도구 부재가 문서 확정을 막으면 안 됨.
- IMPACT | **경고만** - 성공 시에만 파일 포맷. 세부 = [spec.md](spec.md).

## Superseded

## Deprecated

### **[검증] 프론트 매터 YAML 주석 검사 중단**

- DECISION | **YAML 주석 미검사** - FM 주석 검증 제거.
- REASON | **주석 모호성** - `#` 파싱 불안정.
- IMPACT | **Accepted [검증] 주석 검사 범위**로 흡수. 이력 보존용.
