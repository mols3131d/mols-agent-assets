from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar


@dataclass(frozen=True)
class ValidationResult:
    """검증 결과를 나타내는 데이터 모델."""

    level: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"level": self.level, "code": self.code, "message": self.message}


@dataclass(frozen=True)
class AssetInitOptions:
    """자산 초기화에 필요한 CLI 옵션 묶음."""

    resources: list[str]
    include_examples: bool
    description: str
    license_val: str | None
    compatibility: str | None
    metadata: dict[str, str]
    allowed_tools: str | None
    dry_run: bool
    routing_skill: bool = False


class Asset(ABC):
    """모든 에이전트 자산 클래스의 추상 베이스 클래스."""

    asset_type: ClassVar[str]
    config: ClassVar[Any]
    template: ClassVar[str]

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self._content_cache: dict[str, str] = {}
        self._frontmatter_cache: dict[str, tuple[dict[str, str], str]] = {}

    def read_text_file(self, filename: str) -> str | None:
        """자산 파일을 읽고 validator 실행 중 재사용한다."""
        if filename in self._content_cache:
            return self._content_cache[filename]

        filepath = self.path / filename
        if not filepath.exists():
            return None

        content = filepath.read_text(encoding="utf-8")
        self._content_cache[filename] = content
        return content

    def cache_frontmatter(
        self, filename: str, parsed: tuple[dict[str, str], str]
    ) -> None:
        """파싱된 frontmatter와 본문을 validator 사이에서 공유한다."""
        self._frontmatter_cache[filename] = parsed

    def select_template(self, options: AssetInitOptions) -> str:
        """초기화 옵션에 맞는 템플릿을 반환한다."""
        return self.template

    def get_cached_frontmatter(
        self, filename: str
    ) -> tuple[dict[str, str], str] | None:
        """캐시된 frontmatter 파싱 결과를 반환한다."""
        return self._frontmatter_cache.get(filename)

    @abstractmethod
    def get_filename(self) -> str:
        """자산 파일의 명칭을 얻는다 (예: SKILL.md)."""
        raise NotImplementedError

    @abstractmethod
    def get_validators(self) -> list[Validator]:
        """자산 검증에 바인딩되는 검증기 목록을 얻는다."""
        raise NotImplementedError

    @abstractmethod
    def initialize(self, options: AssetInitOptions) -> dict[str, Any]:
        """자산의 디렉터리 및 표준 템플릿 파일을 초기화 생성한다."""
        raise NotImplementedError


class Validator(ABC):
    """정적 유효성 검사기의 추상 베이스 클래스."""

    @abstractmethod
    def validate(self, asset: Asset) -> list[ValidationResult]:
        """자산을 대상으로 유효성 검사를 수행한다."""
        raise NotImplementedError
