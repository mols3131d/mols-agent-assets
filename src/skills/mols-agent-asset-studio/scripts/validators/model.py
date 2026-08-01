from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def extend(self, other: "ValidationResult", prefix: str | None = None) -> None:
        if prefix:
            self.errors.extend(f"{prefix}: {item}" for item in other.errors)
            self.warnings.extend(f"{prefix}: {item}" for item in other.warnings)
        else:
            self.errors.extend(other.errors)
            self.warnings.extend(other.warnings)
