from typing import TypedDict, Literal

# 가계부의 한 줄 내역(거래)을 정의하는 설계도입니다.
class Transaction(TypedDict):
    id: int          # 고유 번호
    date: str        # 날짜 (예: 2024-03-20)
    type: Literal["income", "expense"]  # 수입 또는 지출만 가능
    category: str    # 카테고리 (식비, 월급 등)
    amount: int      # 금액
    memo: str        # 메모

# 한 달 예산을 정의하는 설계도입니다.
class Budget(TypedDict):
    month: str       # 해당 월 (예: 2024-03)
    amount: int      # 예산 금액