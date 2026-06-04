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

    def validate(self, doc_type: DocType | str) -> list[str]:
        """문서의 프론트매터 유효성을 검증하고, 에러 메시지 리스트를 반환한다."""
        from core.enums import DocType, DocStatus, TaskPriority

        errors = []
        fm = self.frontmatter

        # 1. 필수 필드 존재성 검증
        if not fm.id:
            errors.append("id 필드가 누락되었거나 비어 있습니다.")
        if not fm.title:
            errors.append("title 필드가 누락되었거나 비어 있습니다.")
        
        status_val = fm.status
        if not status_val:
            errors.append("status 필드가 누락되었거나 비어 있습니다.")
        else:
            try:
                DocStatus(status_val)
            except ValueError:
                errors.append(f"유효하지 않은 status 값입니다: {status_val}")

        # 2. 타입별 필드 검증
        try:
            dtype = DocType(doc_type)
        except ValueError:
            errors.append(f"유효하지 않은 문서 유형(doc_type)입니다: {doc_type}")
            return errors

        if dtype == DocType.KANBAN:
            priority_val = fm.priority
            if priority_val:
                try:
                    TaskPriority(priority_val)
                except ValueError:
                    errors.append(f"유효하지 않은 priority 값입니다: {priority_val}")
            
            tags_val = fm.get("tags")
            if tags_val is not None and not isinstance(tags_val, list):
                errors.append("tags 필드는 리스트 형식이어야 합니다.")
                
        elif dtype == DocType.ADR:
            for field in ["categories", "tags", "related-files"]:
                val = fm.get(field)
                if val is not None and not isinstance(val, list):
                    errors.append(f"{field} 필드는 리스트 형식이어야 합니다.")
                    
        elif dtype in (DocType.PRD, DocType.SPEC):
            for field in ["categories", "tags"]:
                val = fm.get(field)
                if val is not None and not isinstance(val, list):
                    errors.append(f"{field} 필드는 리스트 형식이어야 합니다.")

        return errors


def validate_frontmatter(content: str, doc_type: DocType | str) -> list[str]:
    """마크다운 본문 문자열로부터 프론트매터를 추출하여 유효성을 검증한다."""
    fm_data, body = parse_yaml_frontmatter(content)
    doc = Document(frontmatter=Frontmatter(fm_data), body=body)
    return doc.validate(doc_type)
