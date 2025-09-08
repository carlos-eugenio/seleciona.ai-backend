import strawberry
from typing import Optional

@strawberry.type
class StatisticsType:
    id: int
    total: int
    productive: int
    unproductive: int
    percentage_productive: float
    percentage_unproductive: float
