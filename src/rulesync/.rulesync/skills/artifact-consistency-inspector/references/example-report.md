---
title: "Artifact Consistency Report — refund-processing-v2"
description: "Consistency differences observed across the refund API contract, implementation, and validation scope."
created: "2026-08-04T23:55:00+09:00"
updated: "2026-08-04T23:55:00+09:00"
author: "<author>"
type: "artifact-consistency-report"
repository: "acme-example/refund-service"
target: "refund-processing-v2"
coverage: "bounded-complete"
snapshot: "4f8a1c2d96c0e40a8d77f51b326d9481ccbe129a"
---

# Artifact Consistency Report

> Repository, revision, locators, source content, and observations in this document are fictional test data.

## Summary

| Item | Value |
| --- | --- |
| Repository | `acme-example/refund-service` |
| Target | `refund-processing-v2` |
| Scope | API contract, refund handler, routes, integration tests, retry instrumentation |
| Snapshot | `4f8a1c2d96c0e40a8d77f51b326d9481ccbe129a` |
| Result | `findings` |
| Coverage | `bounded-complete` |
| Confirmed observations | `2` |
| Unresolved observations | `1` |
| Verification loops | `2/2` |

API 계약, 구현, 검증 사이에서 확인이 필요한 차이 3건을 발견했습니다.

## Findings

### CON-001 — Integration test uses an older request contract

- **Status:** `verified`
- **Type:** `validation-gap`
- **Relation:** OpenAPI ↔ Integration Test

#### Observed difference

OpenAPI에서는 `reason` 필드를 필수로 정의하지만, integration test는 해당 필드 없이 성공 응답을 기대합니다.

#### References

- `api/openapi.yaml:118-137` — `reason`이 필수 필드로 정의되어 있습니다.
- `src/http/refunds/create-refund.ts:72-84` — 누락된 `reason`에 대해 `400`을 반환합니다.
- `tests/integration/refunds/create-refund.test.ts:39-55` — `reason` 없이 `201`을 기대합니다.

#### Potential impact

현재 API 요청 계약이 integration test에서 정확히 검증되지 않을 수 있습니다.

### CON-002 — Documentation references an inactive route

- **Status:** `verified`
- **Type:** `stale-reference`
- **Relation:** Documentation ↔ HTTP Router

#### Observed difference

사용자 문서는 `/v1/refunds/{id}/cancel`을 안내하지만, 현재 router에는 `/v2/refunds/{id}/void`만 등록되어 있습니다.

#### References

- `docs/refunds.md:88-102` — v1 cancellation route를 안내합니다.
- `src/http/router.ts:44-51` — v2 void route만 등록합니다.
- `api/openapi.yaml:241-274` — v2 void operation만 정의합니다.

#### Potential impact

문서를 따르는 사용자가 현재 등록되지 않은 endpoint를 호출할 수 있습니다.

### CON-003 — Retry metric producer was not located

- **Status:** `unresolved`
- **Type:** `omission`
- **Relation:** Observability Guideline ↔ Retry Instrumentation

#### Observed difference

운영 가이드와 dashboard는 `refund_retry_exhausted_total` metric을 참조하지만, 확인한 application code에서는 metric을 발생시키는 위치를 찾지 못했습니다.

#### References

- `docs/operations/refund-monitoring.md:41-49` — metric emission을 요구합니다.
- `ops/dashboards/refunds.json:310-329` — 해당 metric을 조회합니다.
- `src/workers/refund-retry-worker.ts:1-146` — 확인한 retry path에 emission이 없습니다.

#### Why unresolved

외부 observability package에 접근할 수 없어 producer 부재를 확정하지 못했습니다.

#### Potential impact

Dashboard query에 대응하는 metric producer가 없을 가능성이 있습니다.

## Coverage

- **Checked:** API contract, refund handler, route registration, integration tests, retry worker, dashboard definition
- **Resolved rule sources:** `api/openapi.yaml`, `docs/operations/refund-monitoring.md`, repository configuration
- **Rule-source conflicts:** 없음
- **Excluded:** 폐기된 v1 설계 제안서
- **Limitations:** 외부 observability package에 접근할 수 없었음
- **Assessment boundary:** `refund-processing-v2`와 직접 연결된 artifact 관계만 검사함
