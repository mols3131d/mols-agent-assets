from __future__ import annotations

from pathlib import Path
from typing import Any

from core.utils import (
    format_yaml_list,
    parse_yaml_frontmatter,
)

class Frontmatter:
    """프론트매터 데이터를 캡슐화하고 다루는 모델 클래스."""
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self._data = data or {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        if key in self._data:
            del self._data[key]

    @property
    def id(self) -> str | None:
        return self.get("id")

    @property
    def title(self) -> str | None:
        return self.get("title")

    @property
    def status(self) -> str | None:
        return self.get("status")

    @property
    def priority(self) -> str | None:
        return self.get("priority")

    @property
    def assignee(self) -> str | None:
        return self.get("assignee")

    @property
    def description(self) -> str | None:
        return self.get("description")

    @property
    def tags(self) -> list[str]:
        val = self.get("tags")
        if isinstance(val, list):
            return val
        return []

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Frontmatter:
        return cls(data)

    def serialize(self) -> str:
        """프론트매터 데이터를 YAML 형식 문자열로 시리얼라이즈한다."""
        lines = []
        for k, v in self._data.items():
            if isinstance(v, list):
                lines.append(f"{k}: {format_yaml_list(v)}")
            elif isinstance(v, (int, float, bool)):
                lines.append(f"{k}: {str(v).lower() if isinstance(v, bool) else v}")
            elif v is None:
                lines.append(f"{k}: \"\"")
            else:
                val_str = str(v)
                if '"' in val_str:
                    lines.append(f"{k}: '{val_str}'")
                else:
                    lines.append(f"{k}: \"{val_str}\"")
        return "\n".join(lines)


class Document:
    """마크다운 문서를 나타내는 도메인 모델 클래스."""
    def __init__(self, path: Path | None = None, frontmatter: Frontmatter | None = None, body: str = "") -> None:
        self.path = path
        self.frontmatter = frontmatter or Frontmatter()
        self.body = body

    @classmethod
    def load(cls, path: Path) -> Document:
        """파일시스템에서 문서를 로드한다."""
        content = path.read_text(encoding="utf-8")
        fm_data, body = parse_yaml_frontmatter(content)
        return cls(path=path, frontmatter=Frontmatter.from_dict(fm_data), body=body)

    def save(self, path: Path | None = None) -> None:
        """문서를 파일시스템에 저장한다."""
        target_path = path or self.path
        if not target_path:
            raise ValueError("문서를 저장할 경로가 지정되지 않았습니다.")
        
        serialized_fm = self.frontmatter.serialize()
        lines = ["---", serialized_fm, "---", self.body.lstrip()]
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text("\n".join(lines), encoding="utf-8")
        self.path = target_path

    def to_csv_row(self, relative_to: Path) -> dict[str, str]:
        """문서 프론트매터를 CSV 저장 형식의 플랫한 dictionary로 변환한다."""
        row = {}
        if self.path:
            row["file"] = self.path.relative_to(relative_to).as_posix()
        else:
            row["file"] = ""
            
        for k, v in self.frontmatter.to_dict().items():
            if isinstance(v, list):
                row[k] = "; ".join(v)
            else:
                row[k] = str(v)
        return row
