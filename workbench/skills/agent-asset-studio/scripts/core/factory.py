from __future__ import annotations

import re
from pathlib import Path

from core.assets import AgentAsset, RuleAsset, SkillAsset
from core.base import Asset

ASSET_CLASSES = {
    "skill": SkillAsset,
    "rule": RuleAsset,
    "agent": AgentAsset,
}


class AssetFactory:
    """자산 타입 및 경로 속성을 기반으로 구체 자산 인스턴스를 반환하는 팩토리 클래스."""

    @staticmethod
    def create_asset(asset_type: str, name: str, parent_dir: Path) -> Asset:
        """새로 생성할 자산 이름을 정규화하고 해당 자산 인스턴스를 생성한다."""
        normalized = name.strip().lower()
        normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
        normalized = normalized.strip("-")
        normalized = re.sub(r"-{2,}", "-", normalized)

        asset_path = parent_dir.resolve() / normalized

        asset_class = ASSET_CLASSES.get(asset_type)
        if asset_class is None:
            raise ValueError(f"지원하지 않는 자산 유형입니다: {asset_type}")
        return asset_class(normalized, asset_path)

    @staticmethod
    def load_asset(asset_type: str, asset_dir: Path) -> Asset:
        """기존 자산 디렉터리 경로를 기반으로 자산 인스턴스를 적재한다."""
        resolved_path = asset_dir.resolve()
        name = resolved_path.name
        parent_dir = resolved_path.parent
        return AssetFactory.create_asset(asset_type, name, parent_dir)
