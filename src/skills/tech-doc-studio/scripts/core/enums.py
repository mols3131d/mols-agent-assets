from enum import Enum


class DocType(str, Enum):
    ADR = "adr"
    PRD = "prd"
    SPEC = "spec"
    KANBAN = "kanban"


class DocStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    DONE = "done"
    BACKLOG = "backlog"
    TODO = "todo"
    APPROVED = "approved"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
