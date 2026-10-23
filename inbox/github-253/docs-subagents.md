# Docs Subagents — Consistency Findings

## Inspected

[`docs/subagents/mols-review-dualvantage/maintenance.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/subagents/mols-review-dualvantage/maintenance.md)의 caller / Root / Verifier / Challenger 책임 구분과 [`docs/references/agent-assets/README.md`](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/references/agent-assets/README.md)의 reference/maintainer boundary를 읽었다.

## Result

**확인된 이슈 없음(제한적 검토).** maintainer 문서는 과거 `review-lead` consumer를 설명하면서도 과거 명칭을 현재 canonical subagent라고 주장하지 않는다.

## Coverage Limits

`src/rulesync/.rulesync/subagents/` 개별 prompt와의 전문 비교 및 delegation runtime 검증은 수행하지 않았다. 이 결과를 Subagent 전체의 의미 일치로 일반화할 수 없다.

## Retired Subagent Names

[별도 조사](retired-assets.md)에서는 이전 `review-lead`·`review-quality`·`review-adversarial` 원본이 없음을 확인했다. 현행 [DualVantage maintainer](https://github.com/mols3131d/mols-agent-assets/blob/23d649b2eac6e9115ce0e97a823d59de4d37b3c5/docs/subagents/mols-review-dualvantage/maintenance.md)의 `Legacy review callers`는 이관을 위한 설명이며 지우면 오히려 호환성 맥락이 유실된다. 과거 `inbox/2026-08-22/` 연구·계획·리뷰는 당시 자산 상태를 기록한다.
