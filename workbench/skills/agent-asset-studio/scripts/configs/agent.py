from typing import Final

from core.schema import FrontmatterSchema

from .common import (  # ty: ignore[unresolved-import]
    COMMON_DESCRIPTION_FIELD,
    COMMON_NAME_FIELD,
    DEFAULT_AGENT_DESCRIPTION,
)

DEFAULT_DESCRIPTION: Final[str] = DEFAULT_AGENT_DESCRIPTION

# Configuration for Agent Validation
FRONTMATTER_SCHEMA: Final[FrontmatterSchema] = FrontmatterSchema(
    [
        COMMON_NAME_FIELD,
        COMMON_DESCRIPTION_FIELD,
    ]
)
