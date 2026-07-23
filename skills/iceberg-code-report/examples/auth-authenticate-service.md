---
title: 'auth-authenticate-service'
description: '사용자 조회, password 검증, token 발급을 하나의 인증 흐름으로 조정한다.'
type: 'code-report-component'
domain: 'auth'
---

- Location: [`src/auth/service.py:24`](/src/auth/service.py#L24)

## Summary

`AuthenticateService`는 login use case의 중심이다. 저장소나 암호화 구현을 직접
수행하지 않고 각 dependency를 정해진 순서로 호출한다.

## Responsibility

**[auth] Use-case orchestration**: 인증 순서와 성공·실패 계약을 소유한다.

- Input: email과 평문 password
- Output: access token 또는 `AuthenticationFailed`
- Direct dependencies: `UserRepository`, `PasswordHasher`, `TokenIssuer`

## Execution Flow

1. **Start**: endpoint가 `authenticate(email, password)`를 호출한다.
2. **Calls**: 사용자 조회, password 검증, token 발급 순서로 진행한다.
3. **State**: repository를 통해 사용자 정보를 읽으며 직접 쓰기는 없다.
4. **Return**: 검증 성공 시 issuer가 만든 access token을 반환한다.

## Boundaries

**Failure boundary**: 사용자 부재와 password 불일치는 같은 `AuthenticationFailed`로
정규화된다.

- External system: dependency를 통해서만 DB와 signing 기능에 접근한다.
- Transaction / read-write boundary: 단일 사용자 read, transaction 없음
- Contract / invariant: token 발급은 password 검증 성공 뒤에만 실행된다.

## Evidence

- [`AuthenticateService.authenticate`](/src/auth/service.py#L24): dependency 호출 순서를 정의한다.
- [`test_authenticate`](/tests/auth/test_service.py#L30): 성공과 인증 실패 계약을 확인한다.
- Unverified / inference: dependency instance의 lifecycle은 composition root 확인이 필요하다.
