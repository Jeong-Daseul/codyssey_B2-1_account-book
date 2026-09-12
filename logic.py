from storage import save_data, load_data
from datetime import datetime

TRANSACTIONS_FILE = 'transactions.json'

def add_transaction(date, type, category, amount, memo):
    transactions = load_data(TRANSACTIONS_FILE)
    
    # 새 거래 생성 (ID는 리스트 길이에 1을 더함)
    new_id = len(transactions) + 1
    new_item = {
        "id": new_id,
        "date": date,
        "type": type,
        "category": category,
        "amount": int(amount),
        "memo": memo
    }
    
    transactions.append(new_item)
    save_data(TRANSACTIONS_FILE, transactions)
    return new_id

def get_transactions(limit=None):
    transactions = load_data(TRANSACTIONS_FILE)
    
    # 날짜 기준 최신순 정렬 (내림차순)
    # 날짜 문자열(YYYY-MM-DD)을 비교하여 정렬합니다.
    sorted_list = sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    # limit이 있으면 그 개수만큼만 자르기
    if limit:
        return sorted_list[:limit]
    return sorted_list