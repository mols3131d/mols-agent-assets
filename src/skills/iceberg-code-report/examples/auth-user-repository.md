---
title: 'auth-user-repository'
description: '인증 service에 이메일 기반 사용자 조회 계약을 제공한다.'
type: 'code-report-component'
domain: 'auth'
---

- Location: [`src/auth/repository.py:11`](/src/auth/repository.py#L11)

## Summary

`UserRepository`는 인증 흐름의 persistence adapter다. DB row를 domain `User`로
변환하고 조회 결과가 없으면 `None`을 반환한다.

## Responsibility

**[auth] Persistence boundary**: 사용자 조회 query와 row mapping을 소유한다.

- Input: 정규화된 email
- Output: `User | None`
- Direct dependencies: application DB connection

## Execution Flow

1. **Start**: service가 `find_by_email(email)`을 호출한다.
2. **Calls**: email 조건 query를 실행하고 첫 row를 domain object로 변환한다.
3. **State**: users table을 읽으며 변경하지 않는다.
4. **Return**: 일치하는 `User` 또는 `None`을 반환한다.

## Boundaries

**Failure boundary**: DB 오류는 repository exception으로 감싸 상위 계층에 전달한다.

- External system: application DB
- Transaction / read-write boundary: read-only query, 명시적 transaction 없음
- Contract / invariant: email 조회는 최대 한 사용자를 반환한다.

## Evidence

- [`UserRepository.find_by_email`](/src/auth/repository.py#L11): query와 mapping을 수행한다.
- [`test_find_by_email`](/tests/auth/test_repository.py#L17): 사용자 존재·부재 결과를 확인한다.
- Unverified / inference: email unique constraint는 migration 확인이 필요하다.
