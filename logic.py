from models import Transaction
from storage import save_data, get_all_transactions
from utils import logger

# 1. 새로운 거래를 추가하는 기능
@logger
def add_transaction(date: str, type: str, category: str, amount: int, memo: str):
    transactions = get_all_transactions()
    
    # 새로운 ID 생성 (마지막 ID + 1)
    new_id = len(transactions) + 1 if transactions else 1
    
    new_item: Transaction = {
        "id": new_id,
        "date": date,
        "type": type,
        "category": category,
        "amount": amount,
        "memo": memo
    }
    
    transactions.append(new_item)
    save_data(transactions)
    print(f"✅ [{category}] 내역이 성공적으로 저장되었습니다!")

# 2. 전체 요약(수입/지출 합계)을 계산하는 기능
@logger
def get_summary():
    transactions = get_all_transactions()
    
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense
    
    return total_income, total_expense, balance

# 3. 카테고리로 검색하는 기능
@logger
def search_by_category(category: str):
    transactions = get_all_transactions()
    results = [t for t in transactions if category in t['category']]
    return results