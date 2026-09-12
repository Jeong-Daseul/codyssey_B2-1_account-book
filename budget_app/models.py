from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Transaction:
    id: int
    type: str  # 수입 / 지출
    date: str  # YYYY-MM-DD
    amount: int
    category: str
    memo: str
    tags: List[str]

    def to_dict(self):
        return asdict(self)