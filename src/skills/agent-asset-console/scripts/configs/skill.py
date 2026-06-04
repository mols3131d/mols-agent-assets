from typing import Final

from core.schema import FrontmatterSchema

from .common import (
    COMMON_DESCRIPTION_FIELD,
    COMMON_NAME_FIELD,
    DEFAULT_SKILL_DESCRIPTION,
)

DEFAULT_DESCRIPTION: Final[str] = DEFAULT_SKILL_DESCRIPTION

# Configuration for init_skill.py
EXAMPLE_ASSET: Final[str] = """이 파일은 실제 템플릿, 이미지, 설정 예시 같은
정적 자산으로 교체한다. 사용하지 않으면 `assets/`와 함께 삭제한다.
"""

# Configuration for validate_skill.py
FRONTMATTER_SCHEMA: Final[FrontmatterSchema] = FrontmatterSchema([
    COMMON_NAME_FIELD,
    COMMON_DESCRIPTION_FIELD,
])
TRIGGER_WORDS: Final[tuple[str, ...]] = (
    "trigger",
    "use when",
    "사용",
    "트리거",
    "invoke",
    "when",
    "/",
)
