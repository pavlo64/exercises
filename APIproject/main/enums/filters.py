from enum import Enum

class SortField(str, Enum):
    name = "name"
    rate = "rate"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class RateOperation(str, Enum):
    plus = "+"
    minus = "-"