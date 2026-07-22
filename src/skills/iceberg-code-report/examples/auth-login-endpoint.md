---
title: 'auth-login-endpoint'
description: 'Login HTTP 요청을 인증 use case로 연결하고 결과를 응답으로 변환한다.'
type: 'code-report-component'
domain: 'auth'
---

- Location: [`src/auth/http.py:18`](/src/auth/http.py#L18)

## Summary

`login()`은 외부 JSON payload와 내부 인증 service 사이의 HTTP adapter다. 요청값을
검증한 뒤 service 결과를 성공 또는 인증 실패 응답으로 변환한다.

## Responsibility

**[auth] HTTP boundary**: transport 형식과 status code를 소유한다.

- Input: `POST /login`의 email과 password
- Output: access token을 담은 `200` 또는 인증 실패 `401`
- Direct dependencies: `AuthenticateService`, login request schema

## Execution Flow

1. **Start**: router가 `POST /login` 요청을 `login()`에 전달한다.
2. **Calls**: request schema 검증 후 `AuthenticateService.authenticate()`를 호출한다.
3. **State**: endpoint 자체는 상태를 읽거나 쓰지 않는다.
4. **Return**: service 결과를 JSON response와 HTTP status로 변환한다.

## Boundaries

**Failure boundary**: schema 오류는 `400`, 인증 실패는 `401`로 변환된다.

- External system: HTTP client
- Transaction / read-write boundary: 없음
- Contract / invariant: 인증 실패의 내부 원인을 response body에 노출하지 않는다.

## Evidence

- [`login`](/src/auth/http.py#L18): request parsing과 response mapping을 수행한다.
- [`test_login_success`](/tests/auth/test_http.py#L21): 성공 응답의 token 계약을 확인한다.
- Unverified / inference: reverse proxy의 rate limit 정책은 코드 범위 밖이다.
