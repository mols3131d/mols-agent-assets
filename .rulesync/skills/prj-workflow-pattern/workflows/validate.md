# Validate Pattern

**When:** 패턴 문서·링크·frontmatter·생성 인덱스의 정합성을 확인할 때.

1. 변경된 범위와 저장소 `docs/development/validation.md`, `docs/development/formatting.md` 및 필요한 도구 계약을 확인한다. 패턴 자체의 의미 리뷰와 기계적 검사를 구별한다.
2. `mols-markdown-maintenance`와 저장소 기본 도구로 Markdown·frontmatter·내부 링크를 검사한다. 외부 링크의 의미·최신성은 포맷터 성공으로 입증할 수 없다.
3. **패턴 원본에 변경이 있다면** `mise run generated sync`로 `catalog/INDEX.tsv`를 재생성하고 `mise run generated validate`로 drift를 검사한다. 인덱스를 직접 수정하거나 생성기를 임의로 대체하지 않는다.
4. 실제 실행된 검사·미실행·실패를 구분한다. PR Gate 성공을 수행하지 않은 로컬 명령이나 실제 적용 성능의 증거로 확대 해석하지 않는다.

**Result:** 검사와 근거, 생성물 정합성, 남은 미검증·실패 범위.
