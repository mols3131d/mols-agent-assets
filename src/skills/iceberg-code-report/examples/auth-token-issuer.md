---
title: 'auth-token-issuer'
description: '인증된 사용자 식별자와 현재 시각으로 signed access token을 만든다.'
type: 'code-report-component'
domain: 'auth'
---

- Location: [`src/auth/tokens.py:16`](/src/auth/tokens.py#L16)

## Summary

`TokenIssuer`는 인증 흐름의 signing boundary다. 사용자 ID, 발급 시각, 만료 시각을
claim으로 만들고 configured key로 JWT를 서명한다.

## Responsibility

**[auth] Token creation**: access token claim과 signing을 소유한다.

- Input: 인증된 user ID
- Output: signed JWT string
- Direct dependencies: signing key provider, clock

## Execution Flow

1. **Start**: service가 password 검증 성공 후 `issue(user.id)`를 호출한다.
2. **Calls**: clock에서 현재 시각을 읽고 claim을 구성한 뒤 JWT encoder를 호출한다.
3. **State**: key provider와 clock을 읽으며 application state는 변경하지 않는다.
4. **Return**: encoded JWT string을 반환한다.

## Boundaries

**Failure boundary**: signing key를 읽지 못하거나 encoder가 실패하면 token issuance
exception을 반환한다.

- External system: 배포 환경의 signing key provider
- Transaction / read-write boundary: 없음
- Contract / invariant: `exp`는 `iat`보다 뒤이며 subject는 인증된 user ID다.

## Evidence

- [`TokenIssuer.issue`](/src/auth/tokens.py#L16): claim 구성과 signing을 수행한다.
- [`test_issue_token`](/tests/auth/test_tokens.py#L14): subject와 expiration claim을 확인한다.
- Unverified / inference: 운영 key rotation 방식은 deployment 설정 확인이 필요하다.
