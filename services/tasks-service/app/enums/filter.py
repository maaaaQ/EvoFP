from enum import Enum


class FilterPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class FilterCompleted(str, Enum):
    not_completed = "not_completed"
    completed = "completed"
