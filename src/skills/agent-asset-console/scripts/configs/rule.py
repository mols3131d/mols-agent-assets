from typing import Final

from core.schema import FrontmatterSchema

from .common import (
    COMMON_DESCRIPTION_FIELD,
    COMMON_NAME_FIELD,
    DEFAULT_RULE_DESCRIPTION,
)

DEFAULT_DESCRIPTION: Final[str] = DEFAULT_RULE_DESCRIPTION

# Configuration for Rule Validation
FRONTMATTER_SCHEMA: Final[FrontmatterSchema] = FrontmatterSchema([
    COMMON_NAME_FIELD,
    COMMON_DESCRIPTION_FIELD,
])
