from enum import Enum


class FilterPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class FilterCompleted(Enum):
    not_completed = "not_completed"
    completed = "completed"
