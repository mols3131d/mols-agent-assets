from __future__ import annotations

import re
from typing import Any

from core.base import ValidationResult


class FrontmatterField:
    """프론트매터의 개별 키 명세와 제약 조건을 정의하는 필드 클래스."""

    def __init__(
        self,
        name: str,
        is_required: bool = False,
        type_class: type = str,
        max_length: int | None = None,
        regex_pattern: str | None = None,
        regex_message: str | None = None,
    ):
        self.name = name
        self.is_required = is_required
        self.type_class = type_class
        self.max_length = max_length
        self.regex_pattern = re.compile(regex_pattern) if regex_pattern else None
        self.regex_message = regex_message

    def validate(self, value: Any) -> list[str]:
        """필드값의 제약 조건을 유효성 검사한다."""
        errors: list[str] = []
        if not isinstance(value, self.type_class):
            errors.append(
                f"'{self.name}' 필드는 {self.type_class.__name__} 타입이어야 합니다. "
                f"현재: {type(value).__name__}"
            )
            return errors

        if self.type_class is str:
            if self.max_length and len(value) > self.max_length:
                errors.append(
                    f"'{self.name}'은(는) {self.max_length}자 이하여야 합니다. "
                    f"현재 {len(value)}자입니다."
                )
            if self.regex_pattern and not self.regex_pattern.fullmatch(value):
                msg = (
                    self.regex_message
                    if self.regex_message
                    else f"'{self.name}'의 형식이 올바르지 않습니다."
                )
                errors.append(msg)
        return errors


class FrontmatterSchema:
    """필드 명세 집합을 통해 일괄 유효성 검사를 처리하는 스키마 클래스."""

    def __init__(self, fields: list[FrontmatterField]):
        self.fields = {f.name: f for f in fields}

    def validate(
        self, data: dict[str, Any], expected_name: str
    ) -> list[ValidationResult]:
        """프론트매터 데이터 딕셔너리를 대상으로 전체 조건들을 일괄 검증한다."""
        results: list[ValidationResult] = []

        # 1. 허용되지 않은 키 검출
        unexpected_keys = set(data) - set(self.fields)
        if unexpected_keys:
            results.append(
                ValidationResult(
                    level="error",
                    code="unexpected_frontmatter",
                    message=(
                        "허용되지 않은 frontmatter 필드: "
                        f"{', '.join(sorted(unexpected_keys))}"
                    ),
                )
            )

        # 2. 필수 키 누락 및 제약 조건 검증
        for name, field in self.fields.items():
            if name not in data:
                if field.is_required:
                    results.append(
                        ValidationResult(
                            level="error",
                            code=f"missing_{name}",
                            message=f"frontmatter {name}이(가) 없습니다.",
                        )
                    )
                continue

            value = data[name]
            field_errors = field.validate(value)
            for err in field_errors:
                code = f"invalid_{name}"
                if "이하여야 합니다" in err:
                    code = f"{name}_too_long"

                results.append(
                    ValidationResult(
                        level="error",
                        code=code,
                        message=err,
                    )
                )

        # 3. 자산 고유 폴더 명칭과 일치성 검사
        actual_name = data.get("name")
        if actual_name is not None and actual_name != expected_name:
            results.append(
                ValidationResult(
                    level="error",
                    code="name_mismatch",
                    message=(
                        f"frontmatter name={actual_name!r}, "
                        f"folder={expected_name!r}"
                    ),
                )
            )

        return results
