# budget_app/models.py
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Transaction:
    id: int
    type: str          # income / expense
    date: str          # YYYY-MM-DD
    amount: int        # 양수
    category: str
    memo: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

@dataclass
class Budget:
    month: str         # YYYY-MM
    amount: int